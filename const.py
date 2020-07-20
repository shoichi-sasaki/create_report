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
const.FILE_NAMES = dict(
    contact='ContactTraceRecords_同一顧客.csv',
    login='ログイン_ログアウトレポート.csv',
    agent='履歴メトリクスレポート_エージェント.csv',
    queue='履歴メトリクスレポート_キュー.csv'
)
const.BLACK_LIST_AGENT = [
    'IAM IAM'
]