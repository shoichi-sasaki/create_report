"""
Constant types in Python.
"""
class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value

import sys
sys.modules[__name__]=_const()


import const

const.RAW_DATA_PATH = 'resource/raw_datas/'
const.FORMED_DATA_PATH = 'resource/formed_datas/'
const.CONVERTED_DATA_PATH = 'resource/monthly_report/raw_datas/converted_monthly_report/'
const.MONTHLY_RAW_DATA_PATH = 'resource/monthly_report/raw_datas/*/'
const.FILE_NAMES = dict(
    contact='ContactTraceRecords_同一顧客.csv',
    login='ログイン_ログアウトレポート.csv',
    agent='履歴メトリクスレポート_エージェント.csv',
    queue='履歴メトリクスレポート_キュー.csv',
    monthly_login='日次レポート_ログイン人数_*.csv',
    monthly_contact='日次レポート_同一顧客_*.csv',
    monthly_contact_unprocessed='日次レポート_同一顧客(無加工)_*.csv',
    monthly_metrics_agent='日次レポート_履歴メトリクス_エージェント単位*.csv',
    monthly_metrics_queue='日次レポート_履歴メトリクス_キュー単位*.csv'
)
const.BLACK_LIST_AGENT = [
    'IAM IAM'
]