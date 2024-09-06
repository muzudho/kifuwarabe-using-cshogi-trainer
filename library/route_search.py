import cshogi
from py_kifuwarabe_trainer import SquareHelper
from library.shogi import FILE_LEN, RANK_LEN, BOARD_AREA, EAST, NORTH_EAST, NORTH_NORTH_EAST, NORTH, NORTH_WEST, NORTH_NORTH_WEST, WEST, SOUTH_WEST, SOUTH_SOUTH_WEST, SOUTH, SOUTH_EAST, SOUTH_SOUTH_EAST
from library.engine_helper import LegalMovesHelper


class KingRouteSearch():
    """玉の経路探索
    
    玉は８方向に移動できます。
    これを使って、盤上の利きの無いところは移動できると仮定し、
    その盤上で自玉と相手玉の最短経路を探索します
    """


    # 目的地に到達できない距離の印
    _INFINITE = 99


    @staticmethod
    def search(route_board, control_board, friend_k_sq, end_sq, remaining_distance=0):
        """end_sq から friend_k_sq に向かって経路を伸ばします

        Parameters
        ----------
        remaining_distance : int
            玉の残り最短移動回数
        """

        (end_sq_file, end_sq_rank) = SquareHelper.sq_to_file_rank(end_sq)

        def _then_process(adjacent_of_end_sq):
            if route_board[adjacent_of_end_sq] == KingRouteSearch._INFINITE:
                route_board[adjacent_of_end_sq] = remaining_distance + 1

                # 探索終了
                if adjacent_of_end_sq == friend_k_sq:
                    return True

                # 再帰
                KingRouteSearch.search(control_board, route_board, friend_k_sq, end_sq, remaining_distance + 1)

            return False


        # 東
        adjacent_sq = SquareHelper.get_west_of(end_sq)
        if adjacent_sq is not None:
            if _then_process(adjacent_sq):
                return

        # 東北
        adjacent_sq = SquareHelper.get_north_west_of(end_sq)
        if adjacent_sq is not None:
            if _then_process(adjacent_sq):
                return

        # 北
        adjacent_sq = SquareHelper.get_north_of(end_sq)
        if adjacent_sq is not None:
            if _then_process(adjacent_sq):
                return

        # 北西
        adjacent_sq = SquareHelper.get_north_west_of(end_sq)
        if adjacent_sq is not None:
            if _then_process(adjacent_sq):
                return

        # 西
        adjacent_sq = SquareHelper.get_west_of(end_sq)
        if adjacent_sq is not None:
            if _then_process(adjacent_sq):
                return

        # 南西
        adjacent_sq = SquareHelper.get_south_west_of(end_sq)
        if adjacent_sq is not None:
            if _then_process(adjacent_sq):
                return

        # 南
        adjacent_sq = SquareHelper.get_south_of(end_sq)
        if adjacent_sq is not None:
            if _then_process(adjacent_sq):
                return

        # 南東
        adjacent_sq = SquareHelper.get_south_east_of(end_sq)
        if adjacent_sq is not None:
            if _then_process(adjacent_sq):
                return


    def __init__(self, route_board, friend_k_sq, opponent_k_sq):
        """初期化
        
        Parameters
        ----------
        route_board : list
            盤上の経路
            敵玉への残り最短移動回数
            到達できない場合は 99 でも入れておく
        friend_k_sq : int
            自玉のあるマス番号
        opponent_k_sq : int
            敵玉のあるマス番号
        """

        self._friend_k_sq = friend_k_sq
        self._opponent_k_sq = opponent_k_sq
        self._route_board = route_board


    @staticmethod
    def new_obj(board, friend_k_sq, opponent_k_sq):
        route_board = [KingRouteSearch._INFINITE] * BOARD_AREA

        # マスに利いている利きの数
        control_board = [0] * BOARD_AREA

        # 全てのマスの駒について
        for sq in range(0, BOARD_AREA):
            (file, rank) = SquareHelper.sq_to_file_rank(sq)
            piece = board.piece(sq)
            #print(f"[new_obj] {sq=}  {piece=}")

            if board.turn == cshogi.BLACK:
                # ▽歩の利き
                if piece == cshogi.WPAWN:
                    control_board[sq+SOUTH] += 1

                # ▽香の利き
                elif piece == cshogi.WLANCE:
                    for delta in range(1, RANK_LEN - rank):
                        control_rank = rank + delta
                        control_sq = SquareHelper.file_rank_to_sq(file, control_rank)
                        control_board[control_sq] += 1
                        if board.piece(control_sq) != 0:
                            break

                # ▽桂の利き
                elif piece == cshogi.WKNIGHT:
                    # 南に行けるか？
                    if rank + 2 < RANK_LEN:
                        if file + 1 < FILE_LEN:
                            control_board[sq+SOUTH_SOUTH_WEST] += 1
                        
                        if 0 < file - 1:
                            control_board[sq+SOUTH_SOUTH_EAST] += 1

                # ▽銀の利き
                elif piece == cshogi.WSILVER:
                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        if file + 1 < FILE_LEN:
                            control_board[sq+SOUTH_WEST] += 1

                        control_board[sq+SOUTH] += 1

                        if 0 < file - 1:
                            control_board[sq+SOUTH_EAST] += 1

                    # 北に行けるか？
                    if 0 < rank - 1:
                        if 0 < file - 1:
                            control_board[sq+NORTH_EAST] += 1

                        if file + 1 < FILE_LEN:
                            control_board[sq+NORTH_WEST] += 1

                # ▽金と杏圭全馬竜の利き
                elif piece in [cshogi.WGOLD, cshogi.WPROM_PAWN, cshogi.WPROM_LANCE, cshogi.WPROM_KNIGHT, cshogi.WPROM_SILVER, cshogi.WPROM_BISHOP, cshogi.WPROM_ROOK]:
                    if file + 1 < FILE_LEN:
                        control_board[sq+WEST] += 1

                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        if file + 1 < FILE_LEN:
                            control_board[sq+SOUTH_WEST] += 1
                        
                        control_board[sq+SOUTH] += 1

                        if 0 < file - 1:
                            control_board[sq+SOUTH_EAST] += 1

                    if 0 < file - 1:
                        control_board[sq+EAST] += 1

                    # 北に行けるか？
                    if 0 < rank - 1:
                        control_board[sq+NORTH] += 1

                # ▽角の利き
                elif piece == cshogi.WBISHOP:
                    # 南西への動き
                    for delta in range(1, min(FILE_LEN, RANK_LEN)):
                        control_file = file + delta
                        control_rank = rank + delta
                        if FILE_LEN <= control_file or RANK_LEN <= control_rank:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 南東への動き
                    for delta in range(1, min(FILE_LEN, RANK_LEN)):
                        control_file = file - delta
                        control_rank = rank + delta
                        if control_file < 0 or RANK_LEN <= control_rank:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 北東への動き
                    for delta in range(1, min(FILE_LEN, RANK_LEN)):
                        control_file = file - delta
                        control_rank = rank - delta
                        if control_file < 0 or control_rank < 0:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 北西への動き
                    for delta in range(1, min(FILE_LEN, RANK_LEN)):
                        control_file = file + delta
                        control_rank = rank - delta
                        if FILE_LEN <= control_file or control_rank < 0:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                # ▽飛の利き
                elif piece == cshogi.WROOK:
                    # 西への動き
                    for delta in range(1, FILE_LEN):
                        control_file = file + delta
                        if FILE_LEN <= control_file:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 南への動き
                    for delta in range(1, RANK_LEN):
                        control_rank = rank + delta
                        if RANK_LEN <= control_rank:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 東への動き
                    for delta in range(1, FILE_LEN):
                        control_file = file - delta
                        if control_file < 0:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 北への動き
                    for delta in range(1, RANK_LEN):
                        control_rank = rank - delta
                        if control_rank < 0:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                # ▽玉の利き
                elif piece == cshogi.WKING:
                    if file + 1 < FILE_LEN:
                        control_board[sq+WEST] += 1

                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        if file + 1 < FILE_LEN:
                            control_board[sq+SOUTH_WEST] += 1

                        control_board[sq+SOUTH] += 1

                        if 0 < file - 1:
                            control_board[sq+SOUTH_EAST] += 1

                    if 0 < file - 1:
                        control_board[sq+EAST] += 1

                    # 北に行けるか？
                    if 0 < rank - 1:
                        if 0 < file - 1:
                            control_board[sq+NORTH_EAST] += 1
    
                        control_board[sq+NORTH] += 1

                        if file + 1 < FILE_LEN:
                            control_board[sq+NORTH_WEST] += 1

            elif board.turn == cshogi.WHITE:
                # ▲歩の利き
                if piece == cshogi.BPAWN:
                    control_board[sq+NORTH] += 1

                # ▲香の利き
                elif piece == cshogi.BLANCE:
                    for delta in range(1, rank):
                        control_rank = rank - delta
                        control_sq = SquareHelper.file_rank_to_sq(file, control_rank)
                        control_board[control_sq] += 1
                        if board.piece(control_sq) != 0:
                            break

                # ▲桂の利き
                elif piece == cshogi.BKNIGHT:
                    # 北に行けるか？
                    if 0 < rank - 2:
                        if 0 < file - 1:
                            control_board[sq+NORTH_NORTH_EAST] += 1
                        
                        if file + 1 < FILE_LEN:
                            control_board[sq+NORTH_NORTH_WEST] += 1

                # ▲銀の利き
                elif piece == cshogi.BSILVER:
                    # 北に行けるか？
                    if 0 < rank - 1:
                        if 0 < file - 1:
                            control_board[sq+NORTH_EAST] += 1
                        
                        control_board[sq+NORTH] += 1

                        if file + 1 < FILE_LEN:
                            control_board[sq+NORTH_WEST] += 1
                    
                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        if file + 1 < FILE_LEN:
                            control_board[sq+SOUTH_WEST] += 1

                        if 0 < file - 1:
                            control_board[sq+SOUTH_EAST] += 1

                # ▲金と杏圭全馬竜の利き
                elif piece in [cshogi.BGOLD, cshogi.BPROM_PAWN, cshogi.BPROM_LANCE, cshogi.BPROM_KNIGHT, cshogi.BPROM_SILVER, cshogi.BPROM_BISHOP, cshogi.BPROM_ROOK]:
                    if 0 < file - 1:
                        control_board[sq+EAST] += 1

                    # 北に行けるか？
                    if 0 < rank - 1:
                        if 0 < file - 1:
                            control_board[sq+NORTH_EAST] += 1
                        
                        control_board[sq+NORTH] += 1

                        if file + 1 < FILE_LEN:
                            control_board[sq+NORTH_WEST] += 1

                    if file + 1 < FILE_LEN:
                        control_board[sq+WEST] += 1

                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        control_board[sq+SOUTH] += 1

                # ▲角の利き
                elif piece == cshogi.BBISHOP:
                    # 北東への動き
                    for delta in range(1, min(FILE_LEN, RANK_LEN)):
                        control_file = file - delta
                        control_rank = rank - delta
                        if control_file < 0 or control_rank < 0:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 北西への動き
                    for delta in range(1, min(FILE_LEN, RANK_LEN)):
                        control_file = file + delta
                        control_rank = rank - delta
                        if FILE_LEN <= control_file or control_rank < 0:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 南西への動き
                    for delta in range(1, min(FILE_LEN, RANK_LEN)):
                        control_file = file + delta
                        control_rank = rank + delta
                        if FILE_LEN <= control_file or RANK_LEN <= control_rank:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 南東への動き
                    for delta in range(1, min(FILE_LEN, RANK_LEN)):
                        control_file = file - delta
                        control_rank = rank + delta
                        if control_file < 0 or RANK_LEN <= control_rank:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                # ▲飛の利き
                elif piece == cshogi.BROOK:
                    # 東への動き
                    for delta in range(1, FILE_LEN):
                        control_file = file - delta
                        if control_file < 0:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 北への動き
                    for delta in range(1, RANK_LEN):
                        control_rank = rank - delta
                        if control_rank < 0:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 西への動き
                    for delta in range(1, FILE_LEN):
                        control_file = file + delta
                        if FILE_LEN <= control_file:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(control_file, rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                    # 南への動き
                    for delta in range(1, RANK_LEN):
                        control_rank = rank + delta
                        if RANK_LEN <= control_rank:
                            break
                        control_sq = SquareHelper.file_rank_to_sq(file, control_rank)
                        control_board[control_sq] += 1

                        if board.piece(control_sq) != 0:
                            break

                # ▲玉の利き
                elif piece == cshogi.BKING:
                    if 0 < file - 1:
                        control_board[sq+EAST] += 1

                    # 北に行けるか？
                    if 0 < rank - 1:
                        if 0 < file - 1:
                            control_board[sq+NORTH_EAST] += 1
                        
                        control_board[sq+NORTH] += 1

                        if file + 1 < FILE_LEN:
                            control_board[sq+NORTH_WEST] += 1

                    if file + 1 < FILE_LEN:
                        control_board[sq+WEST] += 1

                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        if file + 1 < FILE_LEN:
                            control_board[sq+SOUTH_WEST] += 1
                        
                        control_board[sq+SOUTH] += 1

                        if 0 < file - 1:
                            control_board[sq+SOUTH_EAST] += 1

        # def each_legal_move(move):
        #     # TODO 相手の駒の利きを調べたい
        #     # 利きの数追加
        #     control_board[move.dst_sq] += 1

        # # DO すべての合法手一覧
        # LegalMovesHelper.for_each_legal_move(board, each_legal_move)

        # 利き盤について
        print(f"""\
CONTROL BOARD
-------------""")
        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = SquareHelper.file_rank_to_sq(file, rank)
                print(f"{control_board[sq]} ", end='')
            print() # 改行
        print(f"""\
-------------""")

        # 経路盤について
        print(f"""\
ROUTE BOARD
-----------""")
        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = SquareHelper.file_rank_to_sq(file, rank)
                print(f"{route_board[sq]} ", end='')
            print() # 改行
        print(f"""\
-----------""")

        # DO 盤上を探索
        KingRouteSearch.search(route_board, control_board, friend_k_sq, opponent_k_sq)

        return KingRouteSearch(route_board, friend_k_sq, opponent_k_sq)


    def next_sq(self, friend_k_sq):
        """次のマス。無ければ None"""

        remaining_distance = self._route_board[friend_k_sq]

        if remaining_distance == KingRouteSearch._INFINITE:
            return None


        # ８方向のどこかに、移動回数が１小さいマスがある
        # 東
        adjacent_sq = SquareHelper.get_west_of(end_sq)
        if adjacent_sq is not None and self._route_board[adjacent_sq] == remaining_distance - 1:
            return adjacent_sq

        # 東北
        adjacent_sq = SquareHelper.get_north_west_of(end_sq)
        if adjacent_sq is not None and self._route_board[adjacent_sq] == remaining_distance - 1:
            return adjacent_sq

        # 北
        adjacent_sq = SquareHelper.get_north_of(end_sq)
        if adjacent_sq is not None and self._route_board[adjacent_sq] == remaining_distance - 1:
            return adjacent_sq

        # 北西
        adjacent_sq = SquareHelper.get_north_west_of(end_sq)
        if adjacent_sq is not None and self._route_board[adjacent_sq] == remaining_distance - 1:
            return adjacent_sq

        # 西
        adjacent_sq = SquareHelper.get_west_of(end_sq)
        if adjacent_sq is not None and self._route_board[adjacent_sq] == remaining_distance - 1:
            return adjacent_sq

        # 南西
        adjacent_sq = SquareHelper.get_south_west_of(end_sq)
        if adjacent_sq is not None and self._route_board[adjacent_sq] == remaining_distance - 1:
            return adjacent_sq

        # 南
        adjacent_sq = SquareHelper.get_south_of(end_sq)
        if adjacent_sq is not None and self._route_board[adjacent_sq] == remaining_distance - 1:
            return adjacent_sq

        # 南東
        adjacent_sq = SquareHelper.get_south_east_of(end_sq)
        if adjacent_sq is not None and self._route_board[adjacent_sq] == remaining_distance - 1:
            return adjacent_sq


        return None


    @property
    def friend_k_sq(self):
        """自玉のあるマス番号"""
        return self._friend_k_sq
    

    @property
    def opponent_k_sq(self):
        """敵玉のあるマス番号"""
        return self._opponent_k_sq
