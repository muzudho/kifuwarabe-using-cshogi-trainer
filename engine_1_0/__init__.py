import cshogi
import datetime
import random
from py_kifuwarabe_trainer import DefaultUsiEngine


_engine_file_path = "engine_1_0/engine_name.txt"


class UsiEngine(DefaultUsiEngine):
    """USI エンジン"""


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

        # 敵玉のマス番号
        if self._board.turn == cshogi.BLACK:
            opponent_k_sq = self._board.king_square(cshogi.WHITE)
        else:
            opponent_k_sq = self._board.king_square(cshogi.BLACK)


        # 敵玉と、進んだ駒とのマンハッタン距離
        def get_distance(opponent_k_sq, p_file_th, p_rank_th):
            opponent_k_file = opponent_k_sq // 9 + 1
            opponent_k_rank = opponent_k_sq % 9 + 1

            return abs(opponent_k_file - p_file_th) + abs(opponent_k_rank - p_rank_th)


        def a_to_i(alphabet):
            if alphabet == 'a':
                return 1
            if alphabet == 'b':
                return 2
            if alphabet == 'c':
                return 3
            if alphabet == 'd':
                return 4
            if alphabet == 'e':
                return 5
            if alphabet == 'f':
                return 6
            if alphabet == 'g':
                return 7
            if alphabet == 'h':
                return 8
            if alphabet == 'i':
                return 9
            raise Error(f'rank alphabet: {alphabet}')

        # 相手玉と、進んだ駒の距離が最小の手を指す。
        #
        #   盤は１辺９マスなので、１番離れているとき８マス。それが２辺で１６マス。
        #   だから　１７マス離れることはない
        #
        nearest_distance = 8 + 8 + 1
        nearest_move_u = None

        move_list = list(self._board.legal_moves)
        random.shuffle(move_list)

        for move in move_list:
            # USI符号
            move_u = cshogi.move_to_usi(move)
            # 移動先
            dst_file_th = int(move_u[2: 3])
            dst_rank_th = a_to_i(move_u[3: 4])
            # 敵玉とのマンハッタン距離
            d = get_distance(opponent_k_sq, dst_file_th, dst_rank_th)

            if d < nearest_distance:
                nearest_distance = d
                nearest_move_u = move_u

        print(f"info depth 0 seldepth 0 time 1 nodes 0 score cp 0 Closest to king")
        print(f'bestmove {nearest_move_u}', flush=True)
