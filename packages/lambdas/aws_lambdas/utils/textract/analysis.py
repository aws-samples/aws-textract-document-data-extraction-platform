#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import boto3
from typing import TypedDict, List, Tuple


class Point(TypedDict):
    X: float
    Y: float


class BoundingBox(TypedDict):
    Top: float
    Left: float
    Width: float
    Height: float


class Geometry(TypedDict):
    BoundingBox: BoundingBox
    Polygon: List[Point]


class Block(TypedDict):
    Id: str
    BlockType: str
    Confidence: float
    Text: str
    Geometry: Geometry
    Page: int


def get_full_textract_document_analysis(job_id: str):
    """
    Follow all pages of results from textract to get the complete analysis results for a job id
    """
    textract = boto3.client("textract")

    has_remaining_pages = True
    combined_response = None
    next_token = None

    while has_remaining_pages:
        response = textract.get_document_analysis(
            JobId=job_id, **({} if next_token is None else {"NextToken": next_token})
        )

        if combined_response is None:
            combined_response = response
        else:
            combined_response["Blocks"] += response["Blocks"]

        next_token = response.get("NextToken")
        has_remaining_pages = next_token is not None

    return combined_response


def _left_right_top_bottom(box: BoundingBox) -> Tuple[float, float, float, float]:
    """
    Helper method to return the the left and right x coordinates and top and bottom y coordinates of a bounding box
    """
    left = box["Left"]
    right = box["Left"] + box["Width"]
    top = box["Top"]
    bottom = box["Top"] + box["Height"]
    return left, right, top, bottom


def boxes_intersect(a: BoundingBox, b: BoundingBox):
    """
    Return whether or not two boxes intersect
    """
    a_left, a_right, a_top, a_bottom = _left_right_top_bottom(a)
    b_left, b_right, b_top, b_bottom = _left_right_top_bottom(b)
    return not (
        # Left edge of b is further right than right edge of a
        b_left > a_right
        or
        # Right edge of b is further left than left edge of a
        b_right < a_left
        or
        # Top edge of b is further down than bottom edge of a
        b_top > a_bottom
        or
        # Bottom edge of b is further up than top edge of a
        b_bottom < a_top
    )


def find_blocks_in_hitbox(blocks: List[Block], hitbox: BoundingBox) -> List[Block]:
    """
    Return the blocks which intersect (overlap) the given hitbox
    """
    return [
        block
        for block in blocks
        if boxes_intersect(block["Geometry"]["BoundingBox"], hitbox)
    ]
