import cshogi
from py_kifuwarabe_trainer import UsiMoveHelper


class LegalMovesHelper():


    @staticmethod
    def for_each_legal_move(board, each_legal_move):
        # 合法手一覧ループ
        for move in board.legal_moves:

            # USI符号
            move_u = cshogi.move_to_usi(move)

            # 指し手オブジェクト
            move = UsiMoveHelper.code_to_move(
                code=move_u)

            each_legal_move(move)
