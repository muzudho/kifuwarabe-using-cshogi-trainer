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
    def _then_process(route_board, control_board, occupied_board, adjacent_of_end_sq, remaining_distance):
        #print(f"[_then_process 1]  {remaining_distance=}  {adjacent_of_end_sq=}  {route_board[adjacent_of_end_sq]=}  {control_board[adjacent_of_end_sq]=}")
        if route_board[adjacent_of_end_sq] == KingRouteSearch._INFINITE and control_board[adjacent_of_end_sq] == 0 and occupied_board[adjacent_of_end_sq] == 0:
            #print("[_then_process 2]")

            # 経路を記入
            route_board[adjacent_of_end_sq] = remaining_distance + 1

            # 再帰を指示
            return True

        #print("[_then_process 5] 探索終了")
        return False


    @staticmethod
    def create_adjacent_squares(sq):
        """リストの要素に None が含まれることに注意"""
        return [
            SquareHelper.get_east_of(sq),           # 東
            SquareHelper.get_north_east_of(sq),     # 北東
            SquareHelper.get_north_of(sq),          # 北
            SquareHelper.get_north_west_of(sq),     # 北西
            SquareHelper.get_west_of(sq),           # 西
            SquareHelper.get_south_west_of(sq),     # 南西
            SquareHelper.get_south_of(sq),          # 南
            SquareHelper.get_south_east_of(sq),     # 南東
        ]


    @staticmethod
    def search(route_board, control_board, occupied_board, friend_k_sq, end_sq, remaining_distance=0):
        """end_sq から friend_k_sq に向かって経路を伸ばします

        Parameters
        ----------
        route_board : list
            経路の記憶
        control_board : list
            敵駒の利きの数
        occupied_board : list
            自駒の有無
        remaining_distance : int
            玉の残り最短移動回数
        """

        # 今の隣
        adjacent_square_list = KingRouteSearch.create_adjacent_squares(end_sq)

        # 再帰ではなく、ループを使う
        # 幅優先探索
        while 0 < len(adjacent_square_list):
            #print(f"[search] 幅優先探索 {remaining_distance=}")

            # 次の次の探索先
            two_adjacent_square_list = []

            for adjacent_sq in adjacent_square_list:
                #print(f"[search] {adjacent_sq=}")
                if adjacent_sq is None:
                    continue

                if KingRouteSearch._then_process(route_board, control_board, occupied_board, adjacent_sq, remaining_distance):
                    temp_list = KingRouteSearch.create_adjacent_squares(adjacent_sq)
                    #print(f"[search] {temp_list=}")
                    two_adjacent_square_list.extend(temp_list)

            adjacent_square_list = two_adjacent_square_list

            remaining_distance += 1


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
    def append_control_of_bishop(board, control_board, file, rank):
        """角の利きを追加"""

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


    @staticmethod
    def append_control_of_rook(board, control_board, file, rank):
        """飛の利きを追加"""

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


    @staticmethod
    def new_obj(
            board,
            friend_k_sq,
            opponent_k_sq,
            without_opponet_king_control=False):

        route_board = [KingRouteSearch._INFINITE] * BOARD_AREA

        # マスに利いている利きの数
        control_board = [0] * BOARD_AREA

        # 自駒の有無
        occupied_board = [0] * BOARD_AREA

        # 全てのマスの自駒について
        occupied_without_king = True    # 両玉除く
        for sq in range(0, BOARD_AREA):
            (file, rank) = SquareHelper.sq_to_file_rank(sq)
            piece = board.piece(sq)
            #print(f"[new_obj] {sq=}  {piece=}")

            if (board.turn == cshogi.BLACK and piece in [cshogi.BPAWN, cshogi.BLANCE, cshogi.BKNIGHT, cshogi.BSILVER, cshogi.BGOLD, cshogi.BBISHOP, cshogi.BROOK, cshogi.BKING, cshogi.BPROM_PAWN, cshogi.BPROM_LANCE, cshogi.BPROM_KNIGHT, cshogi.BPROM_SILVER, cshogi.BPROM_BISHOP, cshogi.BPROM_ROOK]) or\
                (board.turn == cshogi.WHITE and piece in [cshogi.WPAWN, cshogi.WLANCE, cshogi.WKNIGHT, cshogi.WSILVER, cshogi.WGOLD, cshogi.WBISHOP, cshogi.WROOK, cshogi.WKING, cshogi.WPROM_PAWN, cshogi.WPROM_LANCE, cshogi.WPROM_KNIGHT, cshogi.WPROM_SILVER, cshogi.WPROM_BISHOP, cshogi.WPROM_ROOK]):

                if occupied_without_king and piece in [cshogi.BKING, cshogi.WKING]:
                    continue

                occupied_board[sq] += 1

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
                    KingRouteSearch.append_control_of_bishop(board, control_board, file, rank)

                # ▽飛の利き
                elif piece == cshogi.WROOK:
                    KingRouteSearch.append_control_of_rook(board, control_board, file, rank)

                # ▽玉の利き
                elif piece == cshogi.WKING:
                    if without_opponet_king_control:
                        continue

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

                # ▽馬の利き
                elif piece == cshogi.WPROM_BISHOP:
                    KingRouteSearch.append_control_of_bishop(board, control_board, file, rank)

                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        if file + 1 < FILE_LEN:
                            control_board[sq+SOUTH_WEST] += 1

                        if 0 < file - 1:
                            control_board[sq+SOUTH_EAST] += 1

                    # 北に行けるか？
                    if 0 < rank - 1:
                        if 0 < file - 1:
                            control_board[sq+NORTH_EAST] += 1
    
                        if file + 1 < FILE_LEN:
                            control_board[sq+NORTH_WEST] += 1

                # ▽竜の利き
                elif piece == cshogi.WPROM_ROOK:
                    KingRouteSearch.append_control_of_rook(board, control_board, file, rank)

                    if file + 1 < FILE_LEN:
                        control_board[sq+WEST] += 1

                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        control_board[sq+SOUTH] += 1

                    if 0 < file - 1:
                        control_board[sq+EAST] += 1

                    # 北に行けるか？
                    if 0 < rank - 1:
                        control_board[sq+NORTH] += 1

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
                    KingRouteSearch.append_control_of_bishop(board, control_board, file, rank)

                # ▲飛の利き
                elif piece == cshogi.BROOK:
                    KingRouteSearch.append_control_of_rook(board, control_board, file, rank)

                # ▲玉の利き
                elif piece == cshogi.BKING:
                    if without_opponet_king_control:
                        continue

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

                # ▲馬の利き
                elif piece == cshogi.BPROM_BISHOP:
                    KingRouteSearch.append_control_of_bishop(board, control_board, file, rank)

                    # 北に行けるか？
                    if 0 < rank - 1:
                        if 0 < file - 1:
                            control_board[sq+NORTH_EAST] += 1

                        if file + 1 < FILE_LEN:
                            control_board[sq+NORTH_WEST] += 1

                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        if file + 1 < FILE_LEN:
                            control_board[sq+SOUTH_WEST] += 1

                        if 0 < file - 1:
                            control_board[sq+SOUTH_EAST] += 1

                # ▲竜の利き
                elif piece == cshogi.BPROM_ROOK:
                    KingRouteSearch.append_control_of_rook(board, control_board, file, rank)

                    if 0 < file - 1:
                        control_board[sq+EAST] += 1

                    # 北に行けるか？
                    if 0 < rank - 1:
                        control_board[sq+NORTH] += 1

                    if file + 1 < FILE_LEN:
                        control_board[sq+WEST] += 1

                    # 南に行けるか？
                    if rank + 1 < RANK_LEN:
                        control_board[sq+SOUTH] += 1


        # def each_legal_move(move):
        #     # TODO 相手の駒の利きを調べたい
        #     # 利きの数追加
        #     control_board[move.dst_sq] += 1

        # # DO すべての合法手一覧
        # LegalMovesHelper.for_each_legal_move(board, each_legal_move)

        # 盤上の自駒の有無について
        print(f"""\
OCCUPIED
--------""")
        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = SquareHelper.file_rank_to_sq(file, rank)
                print(f"{occupied_board[sq]:2} ", end='')
            print() # 改行
        print(f"""\
--------""")

        # 利き盤について
        print(f"""\
CONTROL BOARD
-------------""")
        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = SquareHelper.file_rank_to_sq(file, rank)
                print(f"{control_board[sq]:2} ", end='')
            print() # 改行
        print(f"""\
-------------""")

        # DO 盤上を探索
        route_board[opponent_k_sq] = 0
        KingRouteSearch.search(route_board, control_board, occupied_board, friend_k_sq, opponent_k_sq)

        # 経路盤について
        print(f"""\
ROUTE BOARD
-----------""")
        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = SquareHelper.file_rank_to_sq(file, rank)
                print(f"{route_board[sq]:2} ", end='')
            print() # 改行
        print(f"""\
-----------""")

        return KingRouteSearch(route_board, friend_k_sq, opponent_k_sq)


    def next_sq(self, sq):
        """次のマス。無ければ None"""

        remaining_distance = self._route_board[sq]
        next_distance = remaining_distance - 1
        print(f"[next_sq]  {sq=}  {remaining_distance=}  {next_distance=}")

        if remaining_distance == KingRouteSearch._INFINITE:
            print(f"[next_sq] 移動不可")
            return None


        # ８方向のどこかに、移動回数が１小さいマスがある
        adjacent_squares = [
            SquareHelper.get_west_of(sq),           # 東
            SquareHelper.get_north_west_of(sq),     # 東北
            SquareHelper.get_north_of(sq),          # 北
            SquareHelper.get_north_west_of(sq),     # 北西
            SquareHelper.get_west_of(sq),           # 西
            SquareHelper.get_south_west_of(sq),     # 南西
            SquareHelper.get_south_of(sq),          # 南
            SquareHelper.get_south_east_of(sq),     # 南東
        ]

        for adjacent_sq in adjacent_squares:
            print(f"[next_sq] {adjacent_sq=}")
            if adjacent_sq is not None:
                print(f"[next_sq] {self._route_board[adjacent_sq]=}")
                if self._route_board[adjacent_sq] == next_distance:
                    return adjacent_sq


        print(f"[next_sq] ８方向に移動不可")
        return None


    @property
    def friend_k_sq(self):
        """自玉のあるマス番号"""
        return self._friend_k_sq
    

    @property
    def opponent_k_sq(self):
        """敵玉のあるマス番号"""
        return self._opponent_k_sq
