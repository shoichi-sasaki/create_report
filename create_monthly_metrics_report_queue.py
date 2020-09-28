# -*- coding: utf-8 -*-

import glob
import const
import pandas as pd
import datetime
import pprint
from functools import reduce

def create_report():
    file_path = glob.glob(const.MONTHLY_RAW_DATA_PATH + const.FILE_NAMES['monthly_metrics_queue'])
    agent_list = []
    arr=[]
    for f in file_path:
        df = pd.read_csv(f, encoding="utf-8")
        df = df.fillna(0)
        d = df.to_dict()
        
        for index,row in df.iterrows():
            if index == 0:
                row["キュー名2"] = []
                row["日付2"] = []
            
            row["キュー名2"] = row["キュー名"]
            row["日付2"] = row["日付"]
            if row["キュー名"] == 0:
                row["キュー名2"] = agent
                row["日付2"] = day
                row["キュー名"] = ""
                row["日付"] = ""
            else:
                agent = row["キュー名"]
                day = row["日付"]
                if row["キュー名"] in agent_list:
                    row["キュー名"] = ""
                else:
                    agent_list.append(row["キュー名"])
            arr.append(row)
    
    sorted_items = sorted(
        arr,
        key = lambda x:(x['キュー名2'], datetime.datetime.strptime(x['日付2'] + " " + x["時間"],'%Y/%m/%d %H:%M'))
    )

    report = []
    for item in sorted_items:
        del item["キュー名2"],item["日付2"] 
        report.append(item)
        
    def converter(acc,cur):
        for key in acc.keys():
            acc[key].append(cur[key])
        return acc

    report_dict = reduce(converter,report,
        {"キュー名":[],
        "日付":[],
        "時間":[],
        "入電数":[],
        "放棄呼数":[],
        "取得数":[],
        "通話時間(秒)":[]})

    month = datetime.datetime.strptime(report_dict['日付'][0], '%Y/%m/%d')
    report_df = pd.DataFrame.from_dict(report_dict, orient='index').T
    save_path = const.CONVERTED_DATA_PATH + '月次レポート_履歴メトリクス_キュー単位_'+ month.strftime('%Y%m') +'.csv'
    report_df.to_csv(path_or_buf=save_path, sep=',',encoding='utf_8_sig', header=True, index=False)

