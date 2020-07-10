import pandas as pd
import datetime

raw_data_path = 'resource/raw_datas/'
formed_data_path = 'resource/formed_datas/'
file_names = dict(
    contact='ContactTraceRecords_同一顧客.csv',
    login='ログイン_ログアウトレポート.csv',
    agent='履歴メトリクスレポート_エージェント.csv',
    queue='履歴メトリクスレポート_キュー.csv'
)
menber = {}



# ログインログアウトレポートの作成
df = pd.read_csv(raw_data_path + file_names['login'], usecols=['エージェント','名','姓','ログイン','ログアウト'])
print(df)

# いる情報…エージェントと姓名の対応表
for index, row in df.iterrows():
    print(index)
    print(row)
    menber[row['エージェント']] = row['姓'] + row['名']
    
# ログイン時間とログアウト時間を、時間帯の値として取得。
# これを
# ログインログアウト時間を渡したら、

# attend_array = []
# def attend_time(login, logout, attend_array):
#     for i in range(24):



# print(df.index)
# df.index = 
# print(df.groupby(lambda x:x.hour).count())

# 上記のログインファイルを解析する。
    # 1. 何人いるのか
    # 2. 0埋め
    # 3. どの時間にいたのかさらう



output_dict = {
    '日付': ['2020/07/08'] + ['']*23,
    '時間': [str(i)+':00' for i in range(24)],
    # 'ログイン人数':,
}

df2 = pd.DataFrame.from_dict(output_dict)
# print(df2)
df2.to_csv(path_or_buf='test_output', sep=',',header=True, index=False)

# time = datetime.datetime.strptime('20/07/08 10:01', '%y/%m/%d %H:%M')
# print(time)
