import concurrent.futures
import datetime
import os
import time

import pendulum
import pytest
from dagster import RunRequest, daily_schedule, graph, in_process_executor, op, repository, sensor
from dagster.core.host_representation.origin import RegisteredRepositoryLocationOrigin
from dagster.core.host_representation.repository_location import GrpcServerRepositoryLocation
from dagster.core.launcher.base import LaunchRunContext
from dagster.core.test_utils import poll_for_finished_run, poll_for_step_start
from dagster.grpc.types import (
    ExecutionPlanSnapshotArgs,
    ExternalScheduleExecutionArgs,
    NotebookPathArgs,
    PartitionArgs,
    PartitionNamesArgs,
    PartitionSetExecutionParamArgs,
    PipelineSubsetSnapshotArgs,
    SensorExecutionArgs,
)
from dagster.serdes import deserialize_json_to_dagster_namedtuple, serialize_dagster_namedtuple
from dagster.utils import file_relative_path
from dagster.utils.error import SerializableErrorInfo
from dagster_cloud.agent.dagster_cloud_agent import DagsterCloudAgent, upload_api_response
from dagster_cloud.api.dagster_cloud_api import (
    CheckRunHealthArgs,
    DagsterCloudApi,
    DagsterCloudApiGrpcResponse,
    DagsterCloudApiSuccess,
    DagsterCloudApiUnknownCommandResponse,
    DagsterCloudUploadApiResponse,
    LaunchRunArgs,
    TerminateRunArgs,
)
from dagster_cloud.execution.watchful_run_launcher.process import PID_TAG
from dagster_cloud.workspace.origin import CodeDeploymentMetadata
from ursula.storage.host_cloud.cloud_storage.schema import (
    RepositoryLocationsDataTable,
    RepositoryLocationsTable,
)
from ursula.user_code.workspace import dagster_cloud_api_call


def _add_location(cloud_storage, location_name="location"):
    cloud_storage.add_location(
        location_name,
        deployment_metadata=CodeDeploymentMetadata(python_file=__file__),
    )

    return RegisteredRepositoryLocationOrigin(location_name)


@pytest.fixture(name="agent")
def agent_fixture(
    # Depends on cloud storage to ensure that we wait to delete the cloud storage data
    # until the agent has finished running
    cloud_storage,  # pylint: disable=unused-argument
):
    with DagsterCloudAgent() as agent:
        yield agent


@pytest.fixture(name="user_code_launcher")
def user_code_launcher_fixture(agent_instance):
    user_code_launcher = agent_instance.user_code_launcher
    user_code_launcher.start()

    yield user_code_launcher


@pytest.fixture(name="cloud_storage")
def cloud_storage_fixture(host_instance):
    cloud_storage = host_instance.cloud_storage

    yield cloud_storage

    with cloud_storage.transaction() as conn:
        conn.execute(RepositoryLocationsDataTable.delete())
        conn.execute(RepositoryLocationsTable.delete())


@pytest.fixture(name="user_cloud_agent_request_storage")
def user_agent_request_storage_fixture(host_instance):
    user_cloud_agent_request_storage = host_instance.user_cloud_agent_request_storage

    yield user_cloud_agent_request_storage

    user_cloud_agent_request_storage.wipe()


@pytest.fixture(name="repository_location")
def repository_location_fixture(agent, agent_instance, user_code_launcher, cloud_storage):
    repository_location_origin = _add_location(cloud_storage)

    next(agent.run_iteration(agent_instance, user_code_launcher))
    user_code_launcher.reconcile()

    endpoint = user_code_launcher.get_grpc_endpoint(repository_location_origin)

    with GrpcServerRepositoryLocation(
        origin=repository_location_origin,
        server_id=endpoint.server_id,
        port=endpoint.port,
        socket=endpoint.socket,
        host=endpoint.host,
        heartbeat=True,
        watch_server=False,
    ) as location:
        yield location


@op
def success():
    time.sleep(1)


@graph
def success_graph():
    success()


@op
def sleepy_op():
    start_time = time.time()
    while True:
        time.sleep(1)
        if time.time() - start_time > 120:
            raise Exception("Timed out")


@graph
def sleepy_graph():
    sleepy_op()


@daily_schedule(
    name="daily_success_job", pipeline_name="success_job", start_date=datetime.datetime(2020, 1, 1)
)
def daily_success_job(_):
    return {}


@sensor(name="success_job_sensor", pipeline_name="success_job")
def success_job_sensor():
    yield RunRequest(run_key=None)


success_job = success_graph.to_job(name="success_job", executor_def=in_process_executor)
sleepy_job = sleepy_graph.to_job(name="sleepy_job", executor_def=in_process_executor)


@repository
def repo():
    return [success_job, daily_success_job, success_job_sensor, sleepy_job]


def _assert_responses_for_requests(
    requests,
    num_requests,
    user_cloud_agent_request_storage,
    response_type=(DagsterCloudApiGrpcResponse, DagsterCloudApiSuccess),
):
    assert len(requests) == num_requests

    for request in requests:
        serialized_response = user_cloud_agent_request_storage.get_response(request.request_id)
        response = deserialize_json_to_dagster_namedtuple(serialized_response)
        print(response)
        assert isinstance(response, response_type)

        assert response.thread_telemetry


def _run_to_request_completion(agent, agent_instance, user_code_launcher):
    # Submit requests to thread pool
    next(agent.run_iteration(agent_instance, user_code_launcher))

    # Wait for all futures to return before processing
    futures = [
        future_context.future for future_context in agent.request_ids_to_future_context.values()
    ]
    _done, not_done = concurrent.futures.wait(futures, timeout=60)
    if not_done:
        raise Exception("Futures did not finish after 60 seconds: " + str(not_done))

    # Process all finished requests
    next(agent.run_iteration(agent_instance, user_code_launcher))

    # Assert that dictionary of future contexts is empty
    assert not agent.request_ids_to_future_context


def test_initial_run_iteration_populates_servers(
    agent,
    agent_instance,
    user_code_launcher,
    cloud_storage,
):
    repository_location_origin = _add_location(cloud_storage)

    with pytest.raises(Exception):
        user_code_launcher.get_grpc_endpoint(repository_location_origin)

    next(agent.run_iteration(agent_instance, user_code_launcher))
    user_code_launcher.reconcile()

    assert user_code_launcher.get_grpc_endpoint(repository_location_origin)


def test_repeated_run_iteration_populates_servers_only_once(
    agent,
    agent_instance,
    user_code_launcher,
    cloud_storage,
):
    repository_location_origin_one = _add_location(cloud_storage, location_name="location1")

    next(agent.run_iteration(agent_instance, user_code_launcher))

    repository_location_origin_two = _add_location(cloud_storage, location_name="location2")

    next(agent.run_iteration(agent_instance, user_code_launcher))
    user_code_launcher.reconcile()

    assert user_code_launcher.get_grpc_endpoint(repository_location_origin_one)

    with pytest.raises(Exception):
        user_code_launcher.get_grpc_endpoint(repository_location_origin_two)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_check_for_workspace_updates(
    agent,
    user_code_launcher,
    agent_instance,
    cloud_storage,
    user_cloud_agent_request_storage,
    num_requests,
):
    repository_location_origin_one = _add_location(cloud_storage, location_name="location1")

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    repository_location_origin_two = _add_location(cloud_storage, location_name="location2")

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)
    user_code_launcher.reconcile()

    assert user_code_launcher.get_grpc_endpoint(repository_location_origin_one)
    assert user_code_launcher.get_grpc_endpoint(repository_location_origin_two)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_execution_plan(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    external_pipeline = repository_location.get_repository("repo").get_full_external_pipeline(
        "success_job"
    )

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_EXTERNAL_EXECUTION_PLAN,
            ExecutionPlanSnapshotArgs(
                pipeline_origin=external_pipeline.get_external_origin(),
                solid_selection=external_pipeline.solid_selection,
                run_config={},
                mode="default",
                step_keys_to_execute=None,
                pipeline_snapshot_id=external_pipeline.identifying_pipeline_snapshot_id,
                known_state=None,
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_subset_external_pipeline_result(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    external_pipeline = repository_location.get_repository("repo").get_full_external_pipeline(
        "success_job"
    )

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_SUBSET_EXTERNAL_PIPELINE_RESULT,
            PipelineSubsetSnapshotArgs(
                pipeline_origin=external_pipeline.get_external_origin(),
                solid_selection=None,
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_partition_config(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    external_repository = repository_location.get_repository("repo")

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_EXTERNAL_PARTITION_CONFIG,
            PartitionArgs(
                repository_origin=external_repository.get_external_origin(),
                partition_set_name="daily_success_job_partitions",
                partition_name="2020-01-01",
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_partition_tags(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    external_repository = repository_location.get_repository("repo")

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_EXTERNAL_PARTITION_TAGS,
            PartitionArgs(
                repository_origin=external_repository.get_external_origin(),
                partition_set_name="daily_success_job_partitions",
                partition_name="2020-01-01",
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_partition_names(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    external_repository = repository_location.get_repository("repo")

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_EXTERNAL_PARTITION_NAMES,
            PartitionNamesArgs(
                repository_origin=external_repository.get_external_origin(),
                partition_set_name="daily_success_job_partitions",
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_partition_set_execution_param_data(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    external_repository = repository_location.get_repository("repo")

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_EXTERNAL_PARTITION_SET_EXECUTION_PARAM_DATA,
            PartitionSetExecutionParamArgs(
                repository_origin=external_repository.get_external_origin(),
                partition_set_name="daily_success_job_partitions",
                partition_names=["2020-01-01"],
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_schedule_execution_data(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    external_repository = repository_location.get_repository("repo")

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_EXTERNAL_SCHEDULE_EXECUTION_DATA,
            ExternalScheduleExecutionArgs(
                repository_origin=external_repository.get_external_origin(),
                instance_ref=agent_instance.get_ref(),
                schedule_name="daily_success_job",
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_sensor_execution_data(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    external_repository = repository_location.get_repository("repo")

    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_EXTERNAL_SENSOR_EXECUTION_DATA,
            SensorExecutionArgs(
                repository_origin=external_repository.get_external_origin(),
                instance_ref=agent_instance.get_ref(),
                sensor_name="success_job_sensor",
                last_completion_time=None,
                last_run_key=None,
                cursor=None,
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


def _wait_for_run_process(host_instance, run_id):
    # Ensure that the pid used to launch this run has termianted
    run = host_instance.get_run_by_id(run_id)
    pid = int(run.tags[PID_TAG])
    start_time = time.time()
    while True:
        if time.time() - start_time > 60:
            raise Exception("Timed out waiting for process to finish")

        print(f"Waiting for process {str(pid)} to finish")
        try:
            os.kill(pid, 0)
        except OSError:
            # Error indicates the process has finished
            return

        time.sleep(1)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_notebook_data(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    num_requests,
):
    requests = []
    for _ in range(num_requests):
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.GET_EXTERNAL_NOTEBOOK_DATA,
            NotebookPathArgs(
                repository_location_origin=repository_location.origin,
                notebook_path=file_relative_path(__file__, "foo.ipynb"),
            ),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)


@pytest.mark.parametrize(
    "num_requests",
    [
        1,
        pytest.param(
            5,
            marks=pytest.mark.xfail(
                reason="https://linear.app/elementl/issue/COM-424/dagster-cloud-agent-launch-run-test-is-flaky"
            ),
        ),
    ],
)
def test_launch_run(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    host_instance,
    repository_location,
    num_requests,
):
    external_pipeline = repository_location.get_repository("repo").get_full_external_pipeline(
        "success_job"
    )

    runs = {}

    requests = []
    for _ in range(num_requests):

        pipeline_run = host_instance.create_run_for_pipeline(
            pipeline_def=success_job,
            external_pipeline_origin=external_pipeline.get_external_origin(),
            pipeline_code_origin=external_pipeline.get_python_origin(),
        )
        runs[pipeline_run.run_id] = pipeline_run
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.LAUNCH_RUN,
            LaunchRunArgs(pipeline_run=pipeline_run),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)

    for run_id in runs:
        poll_for_finished_run(host_instance, run_id)
        _wait_for_run_process(host_instance, run_id)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_terminate_run(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    host_instance,
    repository_location,
    num_requests,
):
    external_pipeline = repository_location.get_repository("repo").get_full_external_pipeline(
        "sleepy_job"
    )

    launcher = user_code_launcher.run_launcher()

    runs = {}

    for _ in range(num_requests):

        pipeline_run = host_instance.create_run_for_pipeline(
            pipeline_def=sleepy_job,
            external_pipeline_origin=external_pipeline.get_external_origin(),
            pipeline_code_origin=external_pipeline.get_python_origin(),
        )
        runs[pipeline_run.run_id] = pipeline_run

        launcher.launch_run(LaunchRunContext(pipeline_run=pipeline_run, workspace=None))

    for run_id in runs:
        poll_for_step_start(host_instance, run_id)

    check_run_health_requests = []
    for run_id in runs:
        check_run_health_requests.append(
            dagster_cloud_api_call(
                user_cloud_agent_request_storage,
                DagsterCloudApi.CHECK_RUN_HEALTH,
                CheckRunHealthArgs(runs[run_id]),
                wait_for_response=False,
            )
        )

    _run_to_request_completion(agent, agent_instance, user_code_launcher)
    _assert_responses_for_requests(
        check_run_health_requests,
        num_requests,
        user_cloud_agent_request_storage,
        DagsterCloudApiSuccess,
    )

    requests = []
    for run_id in runs:
        pipeline_run = runs[run_id]
        request = dagster_cloud_api_call(
            user_cloud_agent_request_storage,
            DagsterCloudApi.TERMINATE_RUN,
            TerminateRunArgs(pipeline_run=pipeline_run),
            wait_for_response=False,
        )

        requests.append(request)

    _run_to_request_completion(agent, agent_instance, user_code_launcher)

    _assert_responses_for_requests(requests, num_requests, user_cloud_agent_request_storage)

    for run_id in runs:
        poll_for_finished_run(host_instance, run_id)
        _wait_for_run_process(host_instance, run_id)

    # CHECK_RUN_HEALTH still succeeds after run is complete
    check_run_health_requests = []
    for run_id in runs:
        check_run_health_requests.append(
            dagster_cloud_api_call(
                user_cloud_agent_request_storage,
                DagsterCloudApi.CHECK_RUN_HEALTH,
                CheckRunHealthArgs(runs[run_id]),
                wait_for_response=False,
            )
        )

    _run_to_request_completion(agent, agent_instance, user_code_launcher)
    _assert_responses_for_requests(
        check_run_health_requests,
        num_requests,
        user_cloud_agent_request_storage,
        DagsterCloudApiSuccess,
    )


@pytest.mark.parametrize("exception", [concurrent.futures.TimeoutError(), Exception("Failure")])
def test_future_exception(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    repository_location,
    monkeypatch,
    exception,
):
    external_pipeline = repository_location.get_repository("repo").get_full_external_pipeline(
        "success_job"
    )

    original_submit = agent.executor.submit

    def submit(*args, **kwargs):
        future = original_submit(*args, **kwargs)
        future.set_exception(exception)

        return future

    monkeypatch.setattr(agent.executor, "submit", submit)

    dagster_cloud_api_call(
        user_cloud_agent_request_storage,
        DagsterCloudApi.GET_EXTERNAL_EXECUTION_PLAN,
        ExecutionPlanSnapshotArgs(
            pipeline_origin=external_pipeline.get_external_origin(),
            solid_selection=external_pipeline.solid_selection,
            run_config={},
            mode="default",
            step_keys_to_execute=None,
            pipeline_snapshot_id=external_pipeline.identifying_pipeline_snapshot_id,
            known_state=None,
        ),
        wait_for_response=False,
    )

    result = next(agent.run_iteration(agent_instance, user_code_launcher))

    assert isinstance(result, SerializableErrorInfo)
    assert result.cls_name == exception.__class__.__name__

    # loop recovers
    result = next(agent.run_iteration(agent_instance, user_code_launcher))
    assert not result


def test_unknown_api(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
):

    agent._process_api_request(  # pylint: disable=protected-access
        {"requestId": "foobar", "requestApi": "DO_THE_HOKEY_POKEY", "requestBody": ""},
        agent_instance,
        user_code_launcher,
        pendulum.now("UTC").timestamp(),
    )

    serialized_response = user_cloud_agent_request_storage.get_response("foobar")
    response = deserialize_json_to_dagster_namedtuple(serialized_response)
    assert isinstance(response, DagsterCloudApiUnknownCommandResponse)
    assert response.thread_telemetry


def test_upload_api_response(
    agent_instance,
    user_cloud_agent_request_storage,
):
    response_body = DagsterCloudApiSuccess()

    upload_response = DagsterCloudUploadApiResponse(
        request_id="my_request", request_api="my_api", response=response_body
    )

    upload_api_response(agent_instance, upload_response)

    response = user_cloud_agent_request_storage.get_response("my_request")
    assert response == serialize_dagster_namedtuple(response_body)
