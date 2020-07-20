import login_report
import contact_report
import const
import datetime
import shutil

date_today = datetime.date(2020, 7, 18)

login_report.create_report(date_today)
contact_report.create_report(date_today)

# 同一顧客の無加工データ
origin_path = const.RAW_DATA_PATH + const.FILE_NAMES['contact']
dest_path = const.FORMED_DATA_PATH + '日次レポート_同一顧客(無加工)_' + date_today.strftime('%Y%m%d') +'.csv'
shutil.copy(origin_path, dest_path)


# backlogアップロード
# def upload_backlog_files():
