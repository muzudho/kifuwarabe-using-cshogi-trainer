import cshogi
import datetime
import random
from py_kifuwarabe_trainer import UsiEngine, SquareHelper, BoardHelper, UsiSquareHelper, UsiMoveHelper


_engine_file_path = "engine_1_0/engine_name.txt"


class UsiEngine_1_0(UsiEngine):
    """USI エンジン Lv. 1.0"""


    def __init__(self):
        """初期化"""
        super().__init__(
            engine_file_path=_engine_file_path)


    def go(self):
        """思考開始～最善手返却"""

        if self._board.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if self._board.is_nyugyoku():
            """入玉宣言局面時"""

            # 勝利宣言
            print(f'bestmove win', flush=True)
            return

        # 一手詰めを詰める
        if not self._board.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._board.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""

                best_move = cshogi.move_to_usi(matemove)
                print('info score mate 1 pv {}'.format(best_move), flush=True)
                print(f'bestmove {best_move}', flush=True)
                return

        # 投了のケースは対応済みなので、以降では指し手が必ず１つ以上ある

        # １手指す
        # --------

        move_list = list(self._board.legal_moves)

        if len(move_list) < 1:
            best_move_u = "resign"

        # 自玉が王手されていたら
        elif self._board.is_check():
            best_move_u = cshogi.move_to_usi(random.sample(move_list, 1)[0])

        else:
            # 敵玉のマス番号
            opponent_k_sq = BoardHelper.get_opponent_king_sq(self._board)


            # 相手玉と、進んだ駒の距離が最小の手を指す。
            #
            #   盤は１辺９マスなので、１番離れているとき８マス。それが２辺で１６マス。
            #   だから　１７マス離れることはない
            #
            nearest_distance = 8 + 8 + 1
            nearest_move_u = None

            random.shuffle(move_list)

            for move in move_list:
                # USI符号
                move_u = cshogi.move_to_usi(move)

                # 指し手オブジェクト
                move = UsiMoveHelper.code_to_move(move_u)

                # 敵玉とのマンハッタン距離
                d = BoardHelper.get_manhattan_distance(opponent_k_sq, move.dst_sq)

                if d < nearest_distance:
                    nearest_distance = d
                    nearest_move_u = move_u


            # 指し手が無ければ投了
            if nearest_move_u is None:
                nearest_move_u = 'resign'

            best_move_u = nearest_move_u


        print(f"""\
info depth 0 seldepth 0 time 1 nodes 0 score cp 0 Closest to king
bestmove {best_move_u}""", flush=True)
