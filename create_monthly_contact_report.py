# -*- coding: utf-8 -*-

import glob
import const
import pandas as pd
import datetime

file_path = glob.glob(const.MONTHLY_RAW_DATA_PATH + const.FILE_NAMES['monthly_contact'])
col_list = []
report_dict ={}
counter = 0
for f in file_path:
    try:
        df = pd.read_csv(f, encoding="cp932")
    except Exception as e:
        df = pd.read_csv(f, encoding="utf-8")
        # print(e)
    cols = df.columns
    #カラムリストの作成
    for col in cols:
        if col not in col_list :
            col_list.append(col)
            report_dict[col] = {}
            
for f in file_path:
    try:
        df = pd.read_csv(f, encoding="cp932")
    except Exception as e:
        df = pd.read_csv(f, encoding="utf-8")
    cols = df.columns
    df_dict = df.to_dict()
    for index, row in df.iterrows():
        if index == 24:
            break
        for col in col_list:
             report_dict[col][counter] = 0
             if col in cols :
                 report_dict[col][counter] = row[col]
        counter += 1
report_df = pd.DataFrame.from_dict(report_dict, orient='index').T

save_path = const.CONVERTED_DATA_PATH + '月次レポート_同一顧客_'+ datetime.datetime.now().strftime('%Y%m') +'.csv'
report_df.to_csv(path_or_buf=save_path, sep=',',encoding='utf_8_sig', header=True, index=False)
