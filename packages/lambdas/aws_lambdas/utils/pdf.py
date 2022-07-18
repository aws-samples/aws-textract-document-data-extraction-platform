#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import boto3
from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileWriter


def read_pdf_from_s3(bucket: str, key: str) -> PdfFileReader:
    """
    Read a pdf file from s3 as a PyPDF2 PdfFileReader
    """
    s3 = boto3.resource("s3")
    pdf_content = s3.Object(bucket, key).get()["Body"].read()
    pdf = PdfFileReader(BytesIO(pdf_content))
    if pdf.isEncrypted:
        pdf.decrypt("")
    return pdf


def get_pdf_pages(
    input: PdfFileReader, start_index: int, end_index: int
) -> PdfFileWriter:
    """
    Return a PyPDF2 PdfFileWriter with pages from the input pdf between the start and end index (inclusive)
    """
    output = PdfFileWriter()
    for i in range(start_index, end_index + 1):
        output.addPage(input.getPage(i))
    return output


def write_pdf_to_s3(pdf: PdfFileWriter, bucket: str, key: str):
    """
    Write a PyPDF2 PdfFileWriter to s3
    """
    s3 = boto3.resource("s3")
    pdf_content = BytesIO()
    pdf.write(pdf_content)
    pdf_content.seek(0)
    s3.Bucket(bucket).upload_fileobj(
        pdf_content,
        key,
        {
            "ContentType": "application/pdf",
        },
    )
