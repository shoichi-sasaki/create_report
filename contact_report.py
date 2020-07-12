# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import const

def create_report(date_today):

    df = pd.read_csv(const.RAW_DATA_PATH + const.FILE_NAMES['contact'], usecols=['Initiation Timestamp','Customer Number'])
    df['Customer Number'] = df['Customer Number'].astype(str)
    contact_timezones = {}
    for index, row in df.iterrows():
        if not row['Customer Number'] in contact_timezones.keys():
            contact_timezones[row['Customer Number']] = [0]*24
        contact_hour = datetime.datetime.strptime(row['Initiation Timestamp'], '%y/%m/%d %H:%M').hour
        contact_timezones[row['Customer Number']][contact_hour] += 1

    contact_csv_dict = {
        '日付': [date_today.strftime('%Y/%m/%d')] + ['']*23,
        '時間/電話': [str(i)+':00' for i in range(24)],
        # 合計を挿入
        # 顧客電話の回数データを挿入

        # 最後の行に合計を挿入
    }
    contact_csv_dict.update(**contact_timezones)

    df2 = pd.DataFrame.from_dict(contact_csv_dict)
    df2['(合計)'] = sum([df2[contact_number] for contact_number in contact_timezones.keys()])
    # カラムの順番を整理
    df2 = df2.loc[:, ['日付', '時間/電話', '(合計)']+list(contact_timezones.keys())]
    df2.to_csv(path_or_buf='日次レポート_同一顧客_'+ date_today.strftime('%Y%m%d') +'.csv', sep=',',encoding='utf_8_sig', header=True, index=False)
    # groupbyで合計して、最後の行として追加する
    
if __name__ == '__main__':
    create_report(datetime.date(2020, 7, 8))