# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import const
from functools import reduce



def create_report(date_today):
    df = pd.read_csv(const.RAW_DATA_PATH + const.FILE_NAMES['queue'], names = ('キュー名', '開始時刻', '終了時間', '取得数' , '入電数', '放棄呼数', '通話時間(秒)'),header=None, skiprows=1)
    df = df.fillna(0)
    agent_timezones = {}
    contents = { 
        '入電数',
        '放棄呼数', 
        '取得数', 
        '通話時間(秒)', 
    }
    init_arr = {
        'キュー名':[],
        '日付':[],
        '時間':[],
        '入電数':[],
        '放棄呼数':[],
        '取得数':[],  
        '通話時間(秒)':[], 
    }

    for index, row in df.iterrows():
        start_time = datetime.datetime.fromisoformat(row['開始時刻'])
        start_hour = start_time.hour
        if row['キュー名'] not in agent_timezones.keys():
            agent_timezones[row['キュー名']] = {} 
            for content in contents:
                agent_timezones[row['キュー名']][content] = [0]*24
        for content in contents:
            agent_timezones[row['キュー名']][content][start_hour] += row[content]
    def restruct(acc, cur):
        acc['キュー名'].append(cur)
        acc['キュー名'].extend(['']*23)
        acc['日付'].append(date_today.strftime('%Y/%m/%d'))
        acc['日付'].extend(['']*23)
        acc['時間'].extend([str(i)+':00' for i in range(24)])
        for item in init_arr.keys():
            if item == 'キュー名' or item == '日付' or item == '時間':
                continue
            acc[item].extend(agent_timezones[cur][item])
        return acc

    metrics_report_agent_dict = reduce(restruct, agent_timezones, init_arr)
    df2 = pd.DataFrame.from_dict(metrics_report_agent_dict, orient='index').T
    
    save_path = const.FORMED_DATA_PATH + '日次レポート_履歴メトリクス_キュー単位'+ date_today.strftime('%Y%m%d') +'.csv'
    df2.to_csv(path_or_buf=save_path, sep=',',encoding='utf_8_sig', header=True, index=False)

if __name__ == '__main__':
    create_report(datetime.date(2020, 7, 8))