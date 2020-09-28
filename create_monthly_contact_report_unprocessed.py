# -*- coding: utf-8 -*-

import glob
import const
import pandas as pd
import datetime

def create_report():
    file_path = glob.glob(const.MONTHLY_RAW_DATA_PATH + const.FILE_NAMES['monthly_contact_unprocessed'])
    counter = 0
    col_list = [
        "Contact ID",
        "Channel",
        "Initiation Timestamp",
        "Phone Number",
        "Queue",
        "Agent",
        "Customer Number",
        "Disconnect Timestamp"
        ]
    report_dict = {
        "Contact ID":{},
        "Channel":{},
        "Initiation Timestamp":{},
        "Phone Number":{},
        "Queue":{},
        "Agent":{},
        "Customer Number":{},
        "Disconnect Timestamp":{}
    }
    for f in file_path:
        df = pd.read_csv(f, encoding="utf-8")
        for index, row in df.iterrows():
            for col in col_list:
                    report_dict[col][counter] = row[col]
            counter += 1
    month = datetime.datetime.strptime(report_dict['Initiation Timestamp'][0], '%y/%m/%d %H:%M')
    report_df = pd.DataFrame.from_dict(report_dict, orient='index').T

    save_path = const.CONVERTED_DATA_PATH + '月次レポート_同一顧客(無加工)_'+ month.strftime('%Y%m') +'.csv'
    report_df.to_csv(path_or_buf=save_path, sep=',',encoding='utf_8_sig', header=True, index=False)
