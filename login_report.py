# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import const

def create_report(date_today):

    df = pd.read_csv(const.RAW_DATA_PATH + const.FILE_NAMES['login'], usecols=['エージェント','名','姓','ログイン','ログアウト'])
    df['名前'] = df['姓'].str.cat(df['名'], sep=' ')
    df.drop(['姓', '名'], axis=1)
    df = df[~df['名前'].isin(const.BLACK_LIST_AGENT)]

    # {'冨澤': [0]*24, '川島': [0]*24}
    agent_timezones = {}
    for index, row in df.iterrows():

        dt_login = datetime.datetime.strptime(row['ログイン'], '%Y/%m/%d %H:%M:%S')
        # まだログアウトされてなければ、一時的にログイン時間をログアウト時間として扱う
        dt_logout = datetime.datetime.strptime(row['ログアウト'], '%Y/%m/%d %H:%M:%S') if not row['ログアウト'] == '-' else dt_login
        
        # ログインが今日よりも前だったら、0にする
        login_hour = 0 if dt_login.date()<date_today else dt_login.hour
        logout_hour = dt_logout.hour
        timezones = [i for i in range(24)][login_hour:logout_hour+1]

        # エージェントが既存か
        if row['名前'] not in agent_timezones.keys():
            agent_timezones[row['名前']] = [0]*24
        for timezone in timezones:
            agent_timezones[row['名前']][timezone] = 1


    login_csv_dict = {
        '日付': [date_today.strftime('%Y/%m/%d')] + ['']*23,
        '時間': [str(i)+':00' for i in range(24)],
        # エージェントのログイン時間帯データを挿入
    }
    login_csv_dict.update(**agent_timezones)

    # 合計列の追加
    df2 = pd.DataFrame.from_dict(login_csv_dict)
    df2['ログイン人数'] = sum([df2[agent] for agent in agent_timezones.keys()])
    
    # カラムの順番を整理
    df2 = df2.loc[:, ['日付', '時間', 'ログイン人数']+list(agent_timezones.keys())]
    
    save_path = const.FORMED_DATA_PATH + '日次レポート_ログイン人数_'+ date_today.strftime('%Y%m%d') +'.csv'
    df2.to_csv(path_or_buf=save_path, sep=',',encoding='utf_8_sig', header=True, index=False)


if __name__ == '__main__':
    create_report(datetime.date(2020, 7, 8))