from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    MonitorSchedule,
    CronTrigger,
    MonitorDefinition,
    ServerlessSparkCompute,
    MonitoringTarget,
    AlertNotification,
    GenerationSafetyQualityMonitoringMetricThreshold,
    GenerationSafetyQualitySignal,
    BaselineDataRange,
    LlmData,
)
from azure.ai.ml.entities._inputs_outputs import Input
from azure.ai.ml.constants import MonitorTargetTasks, MonitorDatasetContext
from azure.identity import DefaultAzureCredential
   
credential = DefaultAzureCredential()

# Update your Azure resources details
subscription_id = "fe38c376-b42a-4741-9e7c-f5d7c31e5873"
resource_group = "rg-ragprojectdev"
aoai_deployment_name = "gpt-4"
aoai_connection_name = "aoai-connection"
project_name = "ai-project-awcfxbntyqyle"  # Ex: ai-project-lh7b37cbhixdq
endpoint_name = "rag-1039-endpoint"  # Ex: rag-PCLN-endpoint
deployment_name = "rag-1039-deployment"  # Ex: rag-PCLN-deployment
   
# These variables can be renamed, but it's not necessary
app_trace_name = "app_traces"
app_trace_version = "1"
monitor_name = "gen_ai_monitor_generation_quality"
defaultgsqsignalname = "gsq-signal"
   
# Set the frequency and notification emails for the monitor
trigger_schedule = CronTrigger(expression="*/5 * * * *")
notification_emails_list = ["test@example.com", "def@example.com"]
   
ml_client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group,
    workspace_name=project_name,
)
   
spark_compute = ServerlessSparkCompute(instance_type="standard_e4s_v3", runtime_version="3.3")
monitoring_target = MonitoringTarget(
    ml_task=MonitorTargetTasks.QUESTION_ANSWERING,
    endpoint_deployment_id=f"azureml:{endpoint_name}:{deployment_name}",
)

# Set thresholds (0.7 = 70%)
aggregated_groundedness_pass_rate = 0.7
aggregated_relevance_pass_rate = 0.7
aggregated_coherence_pass_rate = 0.7
aggregated_fluency_pass_rate = 0.7
   
# Create a Generation Safety Quality (GSQ) signal
generation_quality_thresholds = GenerationSafetyQualityMonitoringMetricThreshold(
    groundedness={"aggregated_groundedness_pass_rate": aggregated_groundedness_pass_rate},
    relevance={"aggregated_relevance_pass_rate": aggregated_relevance_pass_rate},
    coherence={"aggregated_coherence_pass_rate": aggregated_coherence_pass_rate},
    fluency={"aggregated_fluency_pass_rate": aggregated_fluency_pass_rate},
)
input_data = Input(
    type="uri_folder",
    path=f"{endpoint_name}-{deployment_name}-{app_trace_name}:{app_trace_version}",
)
data_window = BaselineDataRange(lookback_window_size="P7D", lookback_window_offset="P0D")
production_data = LlmData(
    data_column_names={"prompt_column": "question", "completion_column": "answer", "context_column": "context"},
    input_data=input_data,
    data_window=data_window,
)
   
gsq_signal = GenerationSafetyQualitySignal(
    connection_id=f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{project_name}/connections/{aoai_connection_name}",
    metric_thresholds=generation_quality_thresholds,
    production_data=[production_data],
    sampling_rate=1.0,
    properties={
        "aoai_deployment_name": aoai_deployment_name,
        "enable_action_analyzer": "false",
        "azureml.modelmonitor.gsq_thresholds": '[{"metricName":"average_fluency","threshold":{"value":4}},{"metricName":"average_coherence","threshold":{"value":4}}]',
    },
)
   
monitoring_signals = {
    defaultgsqsignalname: gsq_signal,
}
   
monitor_settings = MonitorDefinition(
    compute=spark_compute,
    monitoring_target=monitoring_target,
    monitoring_signals=monitoring_signals,
    alert_notification=AlertNotification(emails=notification_emails_list),
)
   
model_monitor = MonitorSchedule(
    name=monitor_name,
    trigger=trigger_schedule,
    create_monitor=monitor_settings,
)
   
ml_client.schedules.begin_create_or_update(model_monitor)
