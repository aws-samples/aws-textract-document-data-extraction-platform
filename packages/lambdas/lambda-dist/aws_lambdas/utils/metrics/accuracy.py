#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import statistics
from typing import List

from aws_api_python_runtime.model.extraction_accuracy import ExtractionAccuracy
from thefuzz import fuzz
from aws_lambdas.utils.logger import get_logger

log = get_logger(__name__)


def _mean_accuracy(values: List) -> ExtractionAccuracy:
    """
    Return the mean of the given extraction accuracy values
    """
    if len(values) > 0:
        return ExtractionAccuracy(
            fieldDistancePercentage=statistics.mean(
                [float(value["fieldDistancePercentage"]) for value in values]
            ),
            fieldCorrectnessPercentage=statistics.mean(
                [float(value["fieldCorrectnessPercentage"]) for value in values]
            ),
        )

    # When there are no values (ie comparing two empty objects or empty lists), they are identically empty!
    return ExtractionAccuracy(
        fieldDistancePercentage=100.0,
        fieldCorrectnessPercentage=100.0,
    )


def _compute_extraction_accuracy_percentage(
    original_extracted_data, reviewed_extracted_data
) -> ExtractionAccuracy:
    """
    Return the extraction accuracy measures by comparing the data that was extracted by the system against the human
    reviewed data. Assumes the original and reviewed data are of the same "shape".
    :param original_extracted_data: form data that was originally extracted by the system
    :param reviewed_extracted_data: form data that has been reviewed and potentially edited by a human
    :return: the accuracy percentage
    """
    if isinstance(original_extracted_data, dict):
        return _mean_accuracy(
            [
                _compute_extraction_accuracy_percentage(
                    original_extracted_data[k], reviewed_extracted_data[k]
                )
                for k in original_extracted_data.keys()
            ]
        )
    elif isinstance(original_extracted_data, list):
        return _mean_accuracy(
            [
                _compute_extraction_accuracy_percentage(
                    original_extracted_data[i], reviewed_extracted_data[i]
                )
                for i in range(0, len(original_extracted_data))
            ]
        )

    # Primitive type, eg int/string/etc.
    return ExtractionAccuracy(
        fieldDistancePercentage=float(
            fuzz.ratio(str(original_extracted_data), str(reviewed_extracted_data))
        ),
        fieldCorrectnessPercentage=100.0
        if original_extracted_data == reviewed_extracted_data
        else 0.0,
    )


def compute_extraction_accuracy_percentage(form) -> ExtractionAccuracy:
    """
    Return the extraction accuracy percentage of a reviewed form
    """
    try:
        return _compute_extraction_accuracy_percentage(
            form["originalExtractedData"], form["extractedData"]
        )
    except Exception as e:
        log.exception(e)
        log.error("Failed to compute extraction accuracy for form: {}".format(form))
        return ExtractionAccuracy(
            fieldDistancePercentage=0.0,
            fieldCorrectnessPercentage=0.0,
        )
