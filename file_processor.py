import json
import urllib.request
import logging

import time
import xlrd
import boto3
import config


def process_xls_url(url):
    logging.info("Processing of url : {}".format(url))
    key_name = "source_file/" + "source_file_" + str(time.time()) + ".xls"
    i_stream = urllib.request.urlopen(url).read()
    obj = save_stream_to_s3(config.BUCKET_NAME, key_name, i_stream)

    wb = xlrd.open_workbook(file_contents=obj.get()['Body'].read())
    sheet = wb.sheet_by_name("MICs List by CC")

    key_names = []
    for col in range(sheet.ncols):
        key_names.append(sheet.cell_value(0, col))

    MIC_by_CC_list = []

    logging.info("Traversing the rows")
    for row in range(1, sheet.nrows):
        row_dict = {}
        for col in range(sheet.ncols):
            value = sheet.cell_value(row, col)
            row_dict[key_names[col]] = value
        MIC_by_CC_list.append(row_dict)

    key_name = "MIC/MIC_by_CC_" + str(time.time()) + ".json"
    save_stream_to_s3(config.BUCKET_NAME, key_name, json.dumps(MIC_by_CC_list, indent=2))


def save_stream_to_s3(bucket_name, key, stream):
    logging.info("Writing file to s3 at : {}".format(key))
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, key)
    obj.put(Body=stream)
    return obj
