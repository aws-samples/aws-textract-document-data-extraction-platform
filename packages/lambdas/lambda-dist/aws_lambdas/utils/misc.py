#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import Mapping, List


def copy_defined_keys(dictionary: Mapping, keys: List[str]) -> Mapping:
    """
    Returns a new dictionary with all the keys from the given list that are present and defined in the dictionary
    """
    return {
        key: dictionary[key]
        for key in keys
        if key in dictionary and dictionary[key] is not None
    }


def only_defined_values(dictionary: Mapping) -> Mapping:
    """
    Returns only the defined values in a dictionary (ie filter out Nones)
    """
    return {
        key: dictionary[key] for key in dictionary.keys() if dictionary[key] is not None
    }
