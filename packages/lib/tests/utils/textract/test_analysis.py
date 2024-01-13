#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_lib.utils.textract.analysis import (
    find_blocks_in_hitbox,
    BoundingBox,
    Block,
)


def _block(box: BoundingBox) -> Block:
    return {
        "Geometry": {"BoundingBox": box},
    }


def test_find_blocks_in_hitbox():
    hitbox = {
        "Top": 0.1,
        "Height": 0.1,
        "Left": 0.4,
        "Width": 0.2,
    }
    block_outside = _block(
        {
            "Top": 0.3,
            "Height": 0.5,
            "Left": 0.4,
            "Width": 0.6,
        }
    )
    block_intersect = _block(
        {
            "Top": 0.05,
            "Height": 0.5,
            "Left": 0.4,
            "Width": 0.6,
        }
    )
    assert find_blocks_in_hitbox([block_outside, block_intersect], hitbox) == [
        block_intersect
    ]
