#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from contextlib import contextmanager
from collections.abc import Generator
from typing import List, Union, Any, Tuple, Callable, Optional, no_type_check
import math

import boto3
from aws_document_extraction_platform_api_python_runtime import Configuration
from aws_document_extraction_platform_api_python_runtime.models.aggregate_metrics import (
    AggregateMetrics,
)
from aws_document_extraction_platform_api_python_runtime.models.status_transition import (
    StatusTransition,
)
from aws_document_extraction_platform_api_python_runtime.models.document_metadata import (
    DocumentMetadata,
)
from aws_document_extraction_platform_api_python_runtime.models.form_metadata import (
    FormMetadata,
)
import botocore

from aws_document_extraction_platform_lib.utils.time import (
    millis_between,
    utc_now_datetime,
    to_datetime,
)
from aws_document_extraction_platform_lib.utils.misc import only_defined_values

METRIC_NAMESPACE = "aws/disclosure-data-extraction"


@dataclass
class MetricDefinition:
    name: str
    unit: str


class Metric:
    ### Accuracy ###
    # The accuracy % of the original extracted data against the human reviewed data, with similarity measured by
    # Levenshtein distance
    EXTRACTION_ACCURACY_DISTANCE = MetricDefinition(
        name="extraction-accuracy-distance", unit="Percent"
    )
    # The accuracy % of the original extracted data against the human reviewed data, with similarity measured by
    # equality (ie % of fields that did not require manual edits)
    EXTRACTION_ACCURACY_CORRECTNESS = MetricDefinition(
        name="extraction-accuracy-correctness", unit="Percent"
    )

    ### Confidence ###
    # The average confidence of all fields reported by textract
    AVERAGE_CONFIDENCE = MetricDefinition(name="average-confidence", unit="Percent")

    ### Timing ###
    # The time taken for a document to be classified into its component forms
    CLASSIFICATION_TIME = MetricDefinition(
        name="classification-time", unit="Milliseconds"
    )
    # The time taken for data to be extracted from a form once classified
    EXTRACTION_TIME = MetricDefinition(name="extraction-time", unit="Milliseconds")
    # The total time from upload to ready for review (ie classification time + extraction time)
    PROCESSING_TIME = MetricDefinition(name="processing-time", unit="Milliseconds")
    # The time spent between a form being ready for review and the review being started
    WAIT_FOR_REVIEW_TIME = MetricDefinition(
        name="wait-for-review-time", unit="Milliseconds"
    )
    # The total time a form spent in review
    REVIEW_TIME = MetricDefinition(name="review-time", unit="Milliseconds")
    # The total time from document upload to review complete
    END_TO_END_TIME = MetricDefinition(name="end-to-end-time", unit="Milliseconds")

    ### Count ###
    DOCUMENT_COUNT = MetricDefinition(name="document-count", unit="Count")
    FORM_COUNT = MetricDefinition(name="form-count", unit="Count")


@dataclass
class MetricDimension:
    name: str
    value: str


@dataclass
class MetricToFetch:
    identifier: str
    metric: MetricDefinition
    start: str
    end: str
    statistic: str
    dimensions: List[MetricDimension]


@dataclass
class FetchedMetric:
    identifier: str
    value: Optional[Union[int, float]]


@dataclass
class StatusTransitionStates:
    from_statuses: List[str]
    to_statuses: List[str]


# A mapping of the status transitions for each timing metric
STATUS_TRANSITIONS_FOR_METRICS = {
    Metric.CLASSIFICATION_TIME.name: StatusTransitionStates(
        from_statuses=["START_CLASSIFICATION"],
        to_statuses=["CLASSIFICATION_SUCCEEDED"],
    ),
    Metric.EXTRACTION_TIME.name: StatusTransitionStates(
        from_statuses=["CLASSIFICATION_SUCCEEDED"],
        to_statuses=["READY_FOR_REVIEW"],
    ),
    Metric.PROCESSING_TIME.name: StatusTransitionStates(
        from_statuses=["START_CLASSIFICATION"],
        to_statuses=["READY_FOR_REVIEW"],
    ),
    Metric.WAIT_FOR_REVIEW_TIME.name: StatusTransitionStates(
        from_statuses=["READY_FOR_REVIEW"],
        to_statuses=["REVIEWING"],
    ),
    Metric.REVIEW_TIME.name: StatusTransitionStates(
        from_statuses=["REVIEWING"],
        to_statuses=["REVIEWED"],
    ),
    Metric.END_TO_END_TIME.name: StatusTransitionStates(
        from_statuses=["START_CLASSIFICATION"],
        to_statuses=["REVIEWED"],
    ),
}


class Metrics:
    """
    Class for managing publishing of metrics
    """

    def __init__(self):
        self.cloudwatch = boto3.client(
            "cloudwatch", config=botocore.client.Config(max_pool_connections=16)
        )
        self._metrics = []

    def publish(self):
        """
        Publish any collected metrics to cloudwatch
        """
        if len(self._metrics) > 0:
            self.cloudwatch.put_metric_data(
                Namespace=METRIC_NAMESPACE, MetricData=self._metrics
            )
            self._metrics = []

    def _serialize_dimensions(self, dimensions: List[MetricDimension]):
        return [{"Name": d.name, "Value": d.value} for d in dimensions]

    def _add_metric(
        self,
        metric: MetricDefinition,
        value: float,
        dimensions: List[MetricDimension],
    ):
        """
        Add a raw metric to be published
        """
        self._metrics.append(
            {
                "MetricName": metric.name,
                "Dimensions": self._serialize_dimensions(dimensions),
                "Timestamp": utc_now_datetime(),
                "Value": value,
                "Unit": metric.unit,
            }
        )

    def _add_count_metric(
        self, metric: MetricDefinition, dimensions: List[MetricDimension]
    ):
        self._add_metric(metric, 1, dimensions)

    def _add_duration_metric_if_present(
        self,
        metric: MetricDefinition,
        dimensions: List[MetricDimension],
        status_transition_log: List[StatusTransition],
        from_statuses: List[str],
        to_statuses: List[str],
        divide_duration: int = 1,
    ):
        """
        Add a metric for the duration between the from and to statuses in the status transition log
        """
        from_statuses_set = set(from_statuses)
        to_statuses_set = set(to_statuses)
        from_timestamp = next(
            (
                t.timestamp
                for t in status_transition_log
                if t.status in from_statuses_set
            ),
            None,
        )
        to_timestamp = next(
            (
                t.timestamp
                for t in reversed(status_transition_log)
                if t.status in to_statuses_set
            ),
            None,
        )

        if from_timestamp is not None and to_timestamp is not None:
            duration = millis_between(from_timestamp, to_timestamp)
            if duration > 0 and divide_duration > 0:
                self._add_metric(metric, duration / divide_duration, dimensions)

    def _per_page(self, metric: MetricDefinition) -> MetricDefinition:
        return MetricDefinition(
            name="{}-per-page".format(metric.name), unit=metric.unit
        )

    def _add_duration_metrics(
        self,
        metric: MetricDefinition,
        dimensions: List[MetricDimension],
        status_transition_log: List[StatusTransition],
        num_pages: int,
    ):
        """
        Add a total duration metric and a per-page duration metric for the duration between statuses defined in the
        map of metric to status transitions
        """
        statuses = STATUS_TRANSITIONS_FOR_METRICS[metric.name]
        # Add the duration metric
        self._add_duration_metric_if_present(
            metric,
            dimensions,
            status_transition_log,
            statuses.from_statuses,
            statuses.to_statuses,
        )
        # Add a per-page duration metric
        self._add_duration_metric_if_present(
            self._per_page(metric),
            dimensions,
            status_transition_log,
            statuses.from_statuses,
            statuses.to_statuses,
            num_pages,
        )

    def _dimensions_for_form(self, form: FormMetadata) -> List[List[MetricDimension]]:
        """
        Return the different dimensions for which to publish form metrics
        """
        # No dimensions, and by schema
        return [[], [MetricDimension(name="SchemaId", value=form.schema_id)]]

    def add_classification_time(self, document: DocumentMetadata):
        """
        Add a metric for the time taken to classify forms within the document
        """
        self._add_duration_metrics(
            Metric.CLASSIFICATION_TIME,
            [],
            document.status_transition_log,
            document.number_of_pages if document.number_of_pages is not None else 1,
        )

    def add_extraction_time(self, form: FormMetadata):
        """
        Add a metric for the time n to extract data from the form (once classified)
        """
        for dimensions in self._dimensions_for_form(form):
            self._add_duration_metrics(
                Metric.EXTRACTION_TIME,
                dimensions,
                form.status_transition_log,
                form.number_of_pages,
            )

    def add_processing_time(self, document: DocumentMetadata, form: FormMetadata):
        """
        Add a metric for the total time taken from the document upload to form data extraction
        """
        # Concatenate both status transition logs for a full timeline from the beginning of uploading the document to the form finishing extraction
        full_status_log = document.status_transition_log + form.status_transition_log
        for dimensions in self._dimensions_for_form(form):
            self._add_duration_metrics(
                Metric.PROCESSING_TIME,
                dimensions,
                full_status_log,
                form.number_of_pages,
            )

    def add_wait_time(self, form: FormMetadata):
        """
        Add a metric for the time a form has spent waiting for review
        """
        for dimensions in self._dimensions_for_form(form):
            self._add_duration_metrics(
                Metric.WAIT_FOR_REVIEW_TIME,
                dimensions,
                form.status_transition_log,
                form.number_of_pages,
            )

    def add_review_time(self, form: FormMetadata):
        """
        Add a metric for the time taken to review the form
        """
        for dimensions in self._dimensions_for_form(form):
            self._add_duration_metrics(
                Metric.REVIEW_TIME,
                dimensions,
                form.status_transition_log,
                form.number_of_pages,
            )

    def add_end_to_end_time(self, document: DocumentMetadata, form: FormMetadata):
        """
        Add a metric for the total time taken from the document upload to review completed
        """
        # Concatenate both status transition logs for a full timeline from the beginning of uploading the document to the form being reviewed
        full_status_log = document.status_transition_log + form.status_transition_log
        for dimensions in self._dimensions_for_form(form):
            self._add_duration_metrics(
                Metric.END_TO_END_TIME,
                dimensions,
                full_status_log,
                form.number_of_pages,
            )

    def add_document_count(self, document: DocumentMetadata):
        """
        Add a counter metric for the total number of documents processed, and the number of successful/failed documents
        depending on status
        """
        self._add_count_metric(Metric.DOCUMENT_COUNT, [])
        self._add_count_metric(
            Metric.DOCUMENT_COUNT,
            [
                MetricDimension(
                    name="Status",
                    value=document.ingestion_execution.status,
                )
            ],
        )

    def add_form_count(self, form: FormMetadata):
        """
        Add a counter metric for the total number of forms processed, and the number of successful/failed forms
        depending on status
        """
        # For consistency with the document count metrics we publish either success/failed for extraction.
        # In the success case here we would otherwise report "READY_FOR_REVIEW"
        status = "FAILED" if form.extraction_execution.status == "FAILED" else "SUCCESS"

        for dimensions in self._dimensions_for_form(form):
            self._add_count_metric(Metric.FORM_COUNT, dimensions)

            self._add_count_metric(
                Metric.FORM_COUNT,
                dimensions + [MetricDimension(name="Status", value=status)],
            )

    def add_extraction_accuracy(self, form: FormMetadata):
        """
        Adds metrics for the form data extraction accuracy
        """
        for dimensions in self._dimensions_for_form(form):
            self._add_metric(
                Metric.EXTRACTION_ACCURACY_DISTANCE,
                form.extraction_accuracy.field_distance_percentage,
                dimensions,
            )
            self._add_metric(
                Metric.EXTRACTION_ACCURACY_CORRECTNESS,
                form.extraction_accuracy.field_distance_percentage,
                dimensions,
            )

    def add_average_confidence(self, form: FormMetadata):
        """
        Adds a metric for the average confidence reported by textract
        """
        for dimensions in self._dimensions_for_form(form):
            self._add_metric(
                Metric.AVERAGE_CONFIDENCE,
                form.average_confidence,
                dimensions,
            )

    def _get_single_statistic_for_time_range(
        self,
        metric: MetricDefinition,
        start: str,
        end: str,
        statistic: str,
        dimensions: List[MetricDimension] = [],
    ):
        # Single period for the entire time range, as seconds rounded up to the nearest hour
        milliseconds_between = millis_between(start, end)
        if milliseconds_between <= 0:
            raise Exception("End timestamp must be after start timestamp")
        period = math.ceil(millis_between(start, end) / 1000 / 3600) * 3600
        result = self.cloudwatch.get_metric_statistics(
            Namespace=METRIC_NAMESPACE,
            MetricName=metric.name,
            Dimensions=self._serialize_dimensions(dimensions),
            StartTime=to_datetime(start),
            EndTime=to_datetime(end),
            Period=period,
            Statistics=[statistic],
            Unit=metric.unit,
        )
        if len(result["Datapoints"]) > 0 and statistic in result["Datapoints"][0]:
            return result["Datapoints"][0][statistic]
        return None

    def get_aggregate_metrics(
        self,
        start_timestamp: str,
        end_timestamp: str,
        schema_ids: List[str],
    ) -> AggregateMetrics:
        """
        Return all aggregate metrics between the start and end timestamps
        """

        # Define a helper method to make the below slightly less verbose
        def _get_stat(
            identifier: str,
            metric: MetricDefinition,
            statistic: str,
            type: Callable[[Any], Union[int, float]],
            dimensions: List[MetricDimension] = [],
        ) -> Tuple[Callable[[Any], Union[int, float]], MetricToFetch]:
            return (
                type,
                MetricToFetch(
                    identifier=identifier,
                    metric=metric,
                    start=start_timestamp,
                    end=end_timestamp,
                    statistic=statistic,
                    dimensions=dimensions,
                ),
            )

        def _fetch_stat(
            stat: Tuple[Callable[[Any], Union[int, float]], MetricToFetch]
        ) -> FetchedMetric:
            type, metric_to_fetch = stat
            value = self._get_single_statistic_for_time_range(
                metric_to_fetch.metric,
                metric_to_fetch.start,
                metric_to_fetch.end,
                metric_to_fetch.statistic,
                metric_to_fetch.dimensions,
            )
            return FetchedMetric(
                value=type(value) if value is not None else None,
                identifier=metric_to_fetch.identifier,
            )

        with ThreadPoolExecutor(max_workers=16) as executor:

            def _get_form_statistics(dimensions: List[MetricDimension]):
                return only_defined_values(
                    {
                        m.identifier: m.value
                        for m in executor.map(
                            _fetch_stat,
                            [
                                _get_stat(
                                    "averageExtractionAccuracyDistance",
                                    Metric.EXTRACTION_ACCURACY_DISTANCE,
                                    "Average",
                                    float,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageExtractionAccuracyCorrectness",
                                    Metric.EXTRACTION_ACCURACY_CORRECTNESS,
                                    "Average",
                                    float,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageConfidence",
                                    Metric.AVERAGE_CONFIDENCE,
                                    "Average",
                                    float,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageExtractionTimeMilliseconds",
                                    Metric.EXTRACTION_TIME,
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageExtractionAccuracyPerPageMilliseconds",
                                    self._per_page(Metric.EXTRACTION_TIME),
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageProcessingTimeMilliseconds",
                                    Metric.PROCESSING_TIME,
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageProcessingTimePerPageMilliseconds",
                                    self._per_page(Metric.PROCESSING_TIME),
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageWaitForReviewTimeMilliseconds",
                                    Metric.WAIT_FOR_REVIEW_TIME,
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageWaitForReviewTimePerPageMilliseconds",
                                    self._per_page(Metric.WAIT_FOR_REVIEW_TIME),
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageReviewTimeMilliseconds",
                                    Metric.REVIEW_TIME,
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageReviewTimePerPageMilliseconds",
                                    self._per_page(Metric.REVIEW_TIME),
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageEndToEndTimeMilliseconds",
                                    Metric.END_TO_END_TIME,
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                                _get_stat(
                                    "averageEndToEndTimePerPageMilliseconds",
                                    self._per_page(Metric.END_TO_END_TIME),
                                    "Average",
                                    int,
                                    dimensions,
                                ),
                            ],
                        )
                    }
                )

            @no_type_check  # mypy struggles to follow the types when using ** to combine dictionaries
            def _build_aggregate_metrics():
                return AggregateMetrics(
                    **{
                        **only_defined_values(
                            {
                                m.identifier: m.value
                                for m in executor.map(
                                    _fetch_stat,
                                    [
                                        _get_stat(
                                            "totalProcessedDocumentCount",
                                            Metric.DOCUMENT_COUNT,
                                            "Sum",
                                            int,
                                        ),
                                        _get_stat(
                                            "totalSuccessfulDocumentCount",
                                            Metric.DOCUMENT_COUNT,
                                            "Sum",
                                            int,
                                            [
                                                MetricDimension(
                                                    name="Status", value="SUCCESS"
                                                )
                                            ],
                                        ),
                                        _get_stat(
                                            "totalFailedDocumentCount",
                                            Metric.DOCUMENT_COUNT,
                                            "Sum",
                                            int,
                                            [
                                                MetricDimension(
                                                    name="Status", value="FAILED"
                                                )
                                            ],
                                        ),
                                        _get_stat(
                                            "totalProcessedFormCount",
                                            Metric.FORM_COUNT,
                                            "Sum",
                                            int,
                                        ),
                                        _get_stat(
                                            "totalSuccessfulFormCount",
                                            Metric.FORM_COUNT,
                                            "Sum",
                                            int,
                                            [
                                                MetricDimension(
                                                    name="Status", value="SUCCESS"
                                                )
                                            ],
                                        ),
                                        _get_stat(
                                            "totalFailedFormCount",
                                            Metric.FORM_COUNT,
                                            "Sum",
                                            int,
                                            [
                                                MetricDimension(
                                                    name="Status", value="FAILED"
                                                )
                                            ],
                                        ),
                                        _get_stat(
                                            "averageClassificationTimeMilliseconds",
                                            Metric.CLASSIFICATION_TIME,
                                            "Average",
                                            int,
                                        ),
                                        _get_stat(
                                            "averageClassificationTimePerPageMilliseconds",
                                            self._per_page(Metric.CLASSIFICATION_TIME),
                                            "Average",
                                            int,
                                        ),
                                    ],
                                )
                            }
                        ),
                        **_get_form_statistics([]),
                        "bySchemaId": only_defined_values(
                            {
                                schema_id: _get_form_statistics(
                                    [MetricDimension(name="SchemaId", value=schema_id)]
                                )
                                for schema_id in schema_ids
                            }
                        ),
                    },
                    _configuration=Configuration()
                )

            return _build_aggregate_metrics()


@contextmanager
def metric_publisher() -> Generator[Metrics, None, None]:
    """
    Helper for using 'with' syntax for publishing all added metrics in parallel
    """
    m = Metrics()
    try:
        yield m
    finally:
        m.publish()
