import csv
import datetime
import filecmp
import logging
import os
import urllib.request
from pathlib import Path

import requests

import pymysql
from config import configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

FILE_NAME = "all_items_%s.csv" % (datetime.date.today().strftime("%Y%m%d"))
FILE_KEY = FILE_NAME

BACKLOG_URL = os.environ["BACKLOG_URL"]
BACKLOG_USER = os.environ["BACKLOG_USER"]
BACKLOG_PASSWORD = os.environ["BACKLOG_PASSWORD"]


def lambda_handler(event, context):
    conn = None

    try:
        conn = db_connect()

        data = get_data(conn)

        uploading_filepath = create_file(data)

        upload_file(uploading_filepath)

        if is_file_uploaded(data, uploading_filepath):
            msg = "ファイルのアップロードが正常に終わりました。"
            result = True
        else:
            msg = "アップロードされたファイルとDBから読み込んだデータが異なる。"
            result = False

    except Exception as e:
        msg = "エラーが発生しました。エラーメッセージは次の通りです。\n" + str(e)
        result = False

    finally:
        if result:
            logging.info(msg)
        else:
            logging.error(msg)

        if conn is not None:
            conn.close()


def db_connect():
    conn = pymysql.connect(host=configs["db_host"],
                           user=configs["db_user"],
                           password=configs["db_password"],
                           charset=configs["db_charset"],
                           db=configs["db_name"],
                           port=configs["db_port"])

    return conn


def get_data(conn):
    curs = conn.cursor()

    sql_select = "SELECT ITEM_NUM, CLASS_TYPE, HEAD_WORD FROM SEARCH_ITEM_PUBLISH"
    curs.execute(sql_select)

    data = curs.fetchall()

    return data


def create_file(data):
    uploading_file = "/tmp/" + FILE_NAME
    
    with open(uploading_file, mode="w", encoding="UTF8",
              newline="") as csvfile:
        file_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        file_writer.writerows(data)

    return Path(uploading_file)


def upload_file(uploading_filepath):
    with open(uploading_filepath, 'rb') as file:
        res = requests.put('{}{}'.format(BACKLOG_URL, FILE_NAME),
                           data=file,
                           auth=(BACKLOG_USER, BACKLOG_PASSWORD))


def is_file_uploaded(data, uploading_filepath):

    r = requests.get('{}{}'.format(BACKLOG_URL, FILE_NAME),
                     auth=(BACKLOG_USER, BACKLOG_PASSWORD))
    uploaded_file = '{}.uploaded'.format(uploading_filepath)
    with open(uploaded_file, 'wb') as f:
        f.write(r.content)

    # アップロードされたファイルとDBから読み込んだファイルを比較する。
    if filecmp.cmp(uploading_filepath, uploaded_file):
        return True
    else:
        raise False
