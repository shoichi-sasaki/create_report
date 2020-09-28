# -*- coding: utf-8 -*-

import glob
import const
import pandas as pd
import datetime

file_path = glob.glob(const.MONTHLY_RAW_DATA_PATH + const.FILE_NAMES['monthly_contact'])
col_list = []
report_dict ={}
sum_dict = {}
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
            sum_dict[col] = 0
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

del col_list[:2]
for col in col_list:
    sum_dict[col] = report_df[col].sum()
sum_dict["日付"] = ""
sum_dict["時間/電話"] = "(合計)"
report_df = report_df.append(sum_dict,ignore_index=True)

save_path = const.CONVERTED_DATA_PATH + '月次レポート_同一顧客_'+ datetime.datetime.now().strftime('%Y%m') +'.csv'
report_df.to_csv(path_or_buf=save_path, sep=',',encoding='utf_8_sig', header=True, index=False)
