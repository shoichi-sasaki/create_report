import login_report
import contact_report
import metrics_report_agent
import metrics_report_queue
import create_monthly_contact_report
import create_monthly_contact_report_unprocessed
import create_monthly_login_report
import create_monthly_metrics_report_agent
import create_monthly_metrics_report_queue

import const
import datetime
import shutil

import subprocess
import PySimpleGUI as sg


# sg.theme('DarkAmber')   # デザインテーマの設定
# sg.theme('Reds')   # デザインテーマの設定
sg.theme('Reddit')


date_today = datetime.date(2020, 7, 20)
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

# ウィンドウに配置するコンポーネント
layout = [
    [sg.Text('<エクスプローラの表示>')],
    [sg.Button('元データ(日次)', size=(17,2)),sg.Button('加工済みデータ(日次)', size=(17,2)),sg.Button('元データ(月次)', size=(17,2)),sg.Button('加工済みデータ(月次)', size=(17,2))],
    # [sg.Button('元データ'),sg.Button('加工済みデータ'), sg.Button('元データの前処理')],
    [sg.Text('', size=(20,1))],
    [sg.Text('<実行オプション>')],
    [sg.Checkbox('ログイン', default=True),sg.Checkbox('履歴メトリクス(エージェント)', default=True),sg.Checkbox('履歴メトリクス(キュー)', default=True),sg.Checkbox('問い合わせ履歴', default=True),sg.Checkbox('問い合わせ履歴(無加工)',default=True)],
    [sg.Input(key='input1', default_text=yesterday.strftime("%Y/%m/%d")), sg.CalendarButton('対象の日時を入力してください', target='input1', key='date1', format='%Y/%m/%d')],
    [sg.Radio('日次レポート', "report", default=True), sg.Radio('月次レポート', "report")],
    [sg.Button('レポートの生成', size=(13,2)), sg.Button('キャンセル', size=(13,2))]
]

# values
# 0-4. オプションチェックボックス
# input1. 対象日
# 5-6. 生成レポート　日次/月次

# ウィンドウの生成
window = sg.Window('Pressio Create Report', layout)

# イベントループ
while True:
    try:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'キャンセル':
            break
        elif event == '元データ(日次)':
            subprocess.run('explorer {}'.format('resource\\raw_datas\\'))
        elif event == '加工済みデータ(日次)':
            subprocess.run('explorer {}'.format('resource\\formed_datas\\'))
        elif event == '元データ(月次)':
            subprocess.run('explorer {}'.format('resource\\monthly_report\\raw_datas\\'))
        elif event == '加工済みデータ(月次)':
            subprocess.run('explorer {}'.format('resource\\converted_monthly_report\\'))
        elif event ==  'レポートの生成':
            date_today = datetime.datetime.strptime(values['input1'], '%Y/%m/%d')
            if values[5] == True:
                login_report.create_report(date_today) if values[0] else ''
                metrics_report_agent.create_report(date_today) if values[1] else ''
                metrics_report_queue.create_report(date_today) if values[2] else ''
                contact_report.create_report(date_today) if values[3] else ''

                # 同一顧客の無加工データ
                if values[4]:
                    origin_path = const.RAW_DATA_PATH + const.FILE_NAMES['contact']
                    dest_path = const.FORMED_DATA_PATH + '日次レポート_同一顧客(無加工)_' + date_today.strftime('%Y%m%d') +'.csv'
                    shutil.copy(origin_path, dest_path)
            else:
                create_monthly_login_report.create_report() if values[0] else ''
                create_monthly_metrics_report_agent.create_report() if values[1] else ''
                create_monthly_metrics_report_queue.create_report() if values[2] else ''
                create_monthly_contact_report.create_report() if values[3] else ''
                create_monthly_contact_report_unprocessed.create_report() if values[4] else ''
    except Exception as e:
        print(e)
window.close()






# backlogアップロード
# def upload_backlog_files():






