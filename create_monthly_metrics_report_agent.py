# -*- coding: utf-8 -*-

import glob
import const
import pandas as pd
import datetime
import pprint
from functools import reduce

def create_report():
    file_path = glob.glob(const.MONTHLY_RAW_DATA_PATH + const.FILE_NAMES['monthly_metrics_agent'])
    agent_list = []
    arr=[]
    for f in file_path:
        df = pd.read_csv(f, encoding="utf-8")
        df = df.fillna(0)
        d = df.to_dict()
        
        for index,row in df.iterrows():
            if index == 0:
                row["エージェント2"] = []
                row["日付2"] = []
            
            row["エージェント2"] = row["エージェント"]
            row["日付2"] = row["日付"]
            if row["エージェント"] == 0:
                row["エージェント2"] = agent
                row["日付2"] = day
                row["エージェント"] = ""
                row["日付"] = ""
            else:
                agent = row["エージェント"]
                day = row["日付"]
                if row["エージェント"] in agent_list:
                    row["エージェント"] = ""
                else:
                    agent_list.append(row["エージェント"])
            arr.append(row)
    
    sorted_items = sorted(
        arr,
        key = lambda x:(x['エージェント2'], datetime.datetime.strptime(x['日付2'] + " " + x["時間"],'%Y/%m/%d %H:%M'))
    )

    report = []
    for item in sorted_items:
        del item["エージェント2"],item["日付2"] 
        report.append(item)
        
    def converter(acc,cur):
        for key in acc.keys():
            acc[key].append(cur[key])
        return acc

    report_dict = reduce(converter,report,
        {"エージェント":[],
        "日付":[],
        "時間":[],
        "入電数":[],
        "放棄呼数":[],
        "取得数":[],
        "通話時間(秒)":[],
        "待機時間(秒)":[]})
    month = datetime.datetime.strptime(report_dict['日付'][0], '%Y/%m/%d')
    report_df = pd.DataFrame.from_dict(report_dict, orient='index').T
    save_path = const.CONVERTED_DATA_PATH + '月次レポート_履歴メトリクス_エージェント単位_'+ month.strftime('%Y%m') +'.csv'
    report_df.to_csv(path_or_buf=save_path, sep=',',encoding='utf_8_sig', header=True, index=False)

