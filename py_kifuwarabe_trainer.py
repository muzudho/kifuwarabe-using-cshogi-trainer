import cshogi
import datetime
import random


class DefaultUsiEngine():
    """USI エンジン"""


    def __init__(self):
        """初期化"""

        # 盤
        self._board = cshogi.Board()
