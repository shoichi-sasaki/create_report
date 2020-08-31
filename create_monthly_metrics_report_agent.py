# -*- coding: utf-8 -*-

import glob
import const
import pandas as pd
import datetime


file_path = glob.glob(const.MONTHLY_RAW_DATA_PATH + const.FILE_NAMES['monthly_metrics_agent'])
col_list = [
    "エージェント",
    "日付",
    "時間",
    "入電数",
    "放棄呼数",
    "取得数",
    "通話時間(秒)",
    "待機時間(秒)"
]
report_dict = {
    "エージェント":{},
    "日付":{},
    "時間":{},
    "入電数":{},
    "放棄呼数":{},
    "取得数":{},
    "通話時間(秒)":{},
    "待機時間(秒)":{}
}

for f in file_path:
    df = pd.read_csv(f, encoding="utf-8")
    