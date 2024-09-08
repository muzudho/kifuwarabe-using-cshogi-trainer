import cshogi
from py_kifuwarabe_trainer import ColorHelper, SquareHelper, BoardHelper
from library.shogi import FILE_LEN, RANK_LEN, BOARD_AREA, EAST, NORTH_EAST, NORTH_NORTH_EAST, NORTH, NORTH_WEST, NORTH_NORTH_WEST, WEST, SOUTH_WEST, SOUTH_SOUTH_WEST, SOUTH, SOUTH_EAST, SOUTH_SOUTH_EAST
from library.engine_helper import LegalMovesHelper


class RouteSearchSub():
    """経路探索サブクラス"""


    @staticmethod
    def create_adjacent_squares(sq):
        """近接するマス番号のリスト生成"""

        # リストの要素に None が含まれることに注意
        items = [
            SquareHelper.get_east_of(sq),           # 東
            SquareHelper.get_north_east_of(sq),     # 北東
            SquareHelper.get_north_of(sq),          # 北
            SquareHelper.get_north_west_of(sq),     # 北西
            SquareHelper.get_west_of(sq),           # 西
            SquareHelper.get_south_west_of(sq),     # 南西
            SquareHelper.get_south_of(sq),          # 南
            SquareHelper.get_south_east_of(sq),     # 南東
        ]

        # リストの要素から None を除去
        return list(filter(None, items))


    @staticmethod
    def add_occupied_pieces(board, occupied_board, occupied_without_king):
        """全てのマスの自駒の有無を設定

        Parameters
        ----------
        board : cshogi.Board
            盤
        occupied_board : list
            自駒の有無盤
        occupied_without_king : bool
            両玉除く
        """
        for sq in range(0, BOARD_AREA):
            (file, rank) = SquareHelper.sq_to_file_rank(sq)
            piece = board.piece(sq)

            if (board.turn == cshogi.BLACK and piece in [cshogi.BPAWN, cshogi.BLANCE, cshogi.BKNIGHT, cshogi.BSILVER, cshogi.BGOLD, cshogi.BBISHOP, cshogi.BROOK, cshogi.BKING, cshogi.BPROM_PAWN, cshogi.BPROM_LANCE, cshogi.BPROM_KNIGHT, cshogi.BPROM_SILVER, cshogi.BPROM_BISHOP, cshogi.BPROM_ROOK]) or\
                (board.turn == cshogi.WHITE and piece in [cshogi.WPAWN, cshogi.WLANCE, cshogi.WKNIGHT, cshogi.WSILVER, cshogi.WGOLD, cshogi.WBISHOP, cshogi.WROOK, cshogi.WKING, cshogi.WPROM_PAWN, cshogi.WPROM_LANCE, cshogi.WPROM_KNIGHT, cshogi.WPROM_SILVER, cshogi.WPROM_BISHOP, cshogi.WPROM_ROOK]):

                if occupied_without_king and piece in [cshogi.BKING, cshogi.WKING]:
                    continue

                occupied_board[sq] += 1


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
    def add_opponent_control(board, control_board, without_opponet_king_control):
        """相手の駒の利きを、利き盤に加算します
        
        Parameters
        ----------
        without_opponet_king_control : bool
            相手玉の利きは除く
        """

        # 全てのマスの駒について
        for sq in range(0, BOARD_AREA):
            (file, rank) = SquareHelper.sq_to_file_rank(sq)
            piece = board.piece(sq)

            opponent_color = ColorHelper.flip(board.turn)

            # 相手の歩の利き
            if piece == BoardHelper.friend_pawn_from_black(opponent_color):
                # 黒番から見て北に利きを１つ追加
                control_board[BoardHelper.north_of_sq_from_black(opponent_color, sq)] += 1

            # 相手の香の利き
            elif piece == BoardHelper.friend_lance_from_black(opponent_color):
                for delta in range(1, BoardHelper.rank_from_black(opponent_color, rank)):
                    control_rank = rank - BoardHelper.positive_number_from_black(opponent_color, delta)
                    control_sq = SquareHelper.file_rank_to_sq(file, control_rank)
                    control_board[control_sq] += 1
                    if board.piece(control_sq) != 0:
                        break

            # 相手の桂の利き
            elif piece == BoardHelper.friend_knight_from_black(opponent_color):
                # 黒番から見て北北に行けるか？
                if BoardHelper.can_it_go_north_north_from_black(opponent_color, rank):
                    # 黒番から見て東に行けるか？
                    if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                        # 黒番から見て北北東に利きを１つ追加
                        control_board[BoardHelper.north_north_east_of_sq_from_black(opponent_color, sq)] += 1
                    
                    # 黒番から見て西に行けるか？
                    if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                        # 黒番から見て北北西に利きを１つ追加
                        control_board[BoardHelper.north_north_west_of_sq_from_black(opponent_color, sq)] += 1

            # 相手の銀の利き
            elif piece == BoardHelper.friend_silver_from_black(opponent_color):
                # 黒番から見て北に行けるか？
                if BoardHelper.can_it_go_north_from_black(opponent_color, rank):
                    # 黒番から見て東に行けるか？
                    if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                        # 黒番から見て北東に利きを１つ追加
                        control_board[BoardHelper.north_east_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て北に利きを１つ追加
                    control_board[BoardHelper.north_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て西に行けるか？
                    if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                        # 黒番から見て北西に利きを１つ追加
                        control_board[BoardHelper.north_west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て南に行けるか？
                if BoardHelper.can_it_go_south_from_black(opponent_color, rank):
                    # 黒番から見て西に行けるか？
                    if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                        # 黒番から見て南西に利きを１つ追加
                        control_board[BoardHelper.south_west_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て東に行けるか？
                    if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                        # 黒番から見て南東に利きを１つ追加
                        control_board[BoardHelper.south_east_of_sq_from_black(opponent_color, sq)] += 1

            # 相手の金と杏圭全の利き
            elif piece in [
                BoardHelper.friend_gold_from_black(opponent_color),
                BoardHelper.friend_prom_pawn_from_black(opponent_color),
                BoardHelper.friend_prom_lance_from_black(opponent_color),
                BoardHelper.friend_prom_knight_from_black(opponent_color),
                BoardHelper.friend_prom_silver_from_black(opponent_color)]:

                # 黒番から見て東に行けるか？
                if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                    # 黒番から見て東に利きを１つ追加
                    control_board[BoardHelper.west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て北に行けるか？
                if BoardHelper.can_it_go_north_from_black(opponent_color, rank):
                    # 黒番から見て東に行けるか？
                    if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                        # 黒番から見て南西に利きを１つ追加
                        control_board[BoardHelper.north_east_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て北に利きを１つ追加
                    control_board[BoardHelper.north_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て西に行けるか？
                    if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                        # 黒番から見て北西に利きを１つ追加
                        control_board[BoardHelper.north_west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て西に行けるか？
                if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                    # 黒番から見て西に利きを１つ追加
                    control_board[BoardHelper.west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て南に行けるか？
                if BoardHelper.can_it_go_south_from_black(opponent_color, rank):
                    # 黒番から見て南に利きを１つ追加
                    control_board[BoardHelper.south_of_sq_from_black(opponent_color, sq)] += 1

            # 相手の角の利き
            elif piece == BoardHelper.friend_bishop_from_black(opponent_color):
                RouteSearchSub.append_control_of_bishop(board, control_board, file, rank)

            # 相手の飛の利き
            elif piece == BoardHelper.friend_rook_from_black(opponent_color):
                RouteSearchSub.append_control_of_rook(board, control_board, file, rank)

            # 相手の玉の利き
            elif piece == BoardHelper.friend_king_from_black(opponent_color):
                if without_opponet_king_control:
                    continue

                # 黒番から見て東に行けるか？
                if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                    # 黒番から見て東に利きを１つ追加
                    control_board[BoardHelper.west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て北に行けるか？
                if BoardHelper.can_it_go_north_from_black(opponent_color, rank):
                    # 黒番から見て東に行けるか？
                    if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                        # 黒番から見て南西に利きを１つ追加
                        control_board[BoardHelper.north_east_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て北に利きを１つ追加
                    control_board[BoardHelper.north_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て西に行けるか？
                    if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                        # 黒番から見て北西に利きを１つ追加
                        control_board[BoardHelper.north_west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て西に行けるか？
                if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                    # 黒番から見て西に利きを１つ追加
                    control_board[BoardHelper.west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て南に行けるか？
                if BoardHelper.can_it_go_south_from_black(opponent_color, rank):
                    # 黒番から見て西に行けるか？
                    if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                        # 黒番から見て南西に利きを１つ追加
                        control_board[BoardHelper.south_west_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て南に利きを１つ追加
                    control_board[BoardHelper.south_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て東に行けるか？
                    if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                        # 黒番から見て南東に利きを１つ追加
                        control_board[BoardHelper.south_east_of_sq_from_black(opponent_color, sq)] += 1

            # 相手の馬の利き
            elif piece == BoardHelper.friend_prom_bishop_from_black(opponent_color):
                RouteSearchSub.append_control_of_bishop(board, control_board, file, rank)

                # 黒番から見て北に行けるか？
                if BoardHelper.can_it_go_north_from_black(opponent_color, rank):
                    # 黒番から見て東に行けるか？
                    if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                        # 黒番から見て南西に利きを１つ追加
                        control_board[BoardHelper.north_east_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て西に行けるか？
                    if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                        # 黒番から見て北西に利きを１つ追加
                        control_board[BoardHelper.north_west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て南に行けるか？
                if BoardHelper.can_it_go_south_from_black(opponent_color, rank):
                    # 黒番から見て西に行けるか？
                    if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                        # 黒番から見て南西に利きを１つ追加
                        control_board[BoardHelper.south_west_of_sq_from_black(opponent_color, sq)] += 1

                    # 黒番から見て東に行けるか？
                    if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                        # 黒番から見て南東に利きを１つ追加
                        control_board[BoardHelper.south_east_of_sq_from_black(opponent_color, sq)] += 1

            # 相手の竜の利き
            elif piece == BoardHelper.friend_prom_rook_from_black(opponent_color):
                RouteSearchSub.append_control_of_rook(board, control_board, file, rank)

                # 黒番から見て東に行けるか？
                if BoardHelper.can_it_go_east_from_black(opponent_color, file):
                    # 黒番から見て東に利きを１つ追加
                    control_board[BoardHelper.west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て北に行けるか？
                if BoardHelper.can_it_go_north_from_black(opponent_color, rank):
                    # 黒番から見て北に利きを１つ追加
                    control_board[BoardHelper.north_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て西に行けるか？
                if BoardHelper.can_it_go_west_from_black(opponent_color, file):
                    # 黒番から見て西に利きを１つ追加
                    control_board[BoardHelper.west_of_sq_from_black(opponent_color, sq)] += 1

                # 黒番から見て南に行けるか？
                if BoardHelper.can_it_go_south_from_black(opponent_color, rank):
                    # 黒番から見て南に利きを１つ追加
                    control_board[BoardHelper.south_of_sq_from_black(opponent_color, sq)] += 1


class KingRouteSearch():
    """玉の経路探索
    
    玉は８方向に移動できます。
    これを使って、盤上の利きの無いところは移動できると仮定し、
    その盤上で自玉と相手玉の最短経路を探索します
    """


    # 目的地に到達できない距離の印
    _INFINITE = 99


    @staticmethod
    def _search_outward(route_board, control_board, occupied_board, adjacent_of_end_sq, remaining_distance):
        if route_board[adjacent_of_end_sq] == KingRouteSearch._INFINITE and control_board[adjacent_of_end_sq] == 0 and occupied_board[adjacent_of_end_sq] == 0:
            # 経路を記入
            route_board[adjacent_of_end_sq] = remaining_distance

            # 繰り返しを指示
            return True

        return False


    @staticmethod
    def _search_return(route_board, adjacent_of_end_sq, remaining_distance):
        # 印が付いているところを、戻っていく
        if route_board[adjacent_of_end_sq] == remaining_distance:
            # 経路を記入
            route_board[adjacent_of_end_sq] = abs(remaining_distance)

            # 繰り返しを指示
            return True

        return False


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

        #
        # DO start から end へ向かって事前探索を行う（候補挙げの探索）。 0 から -1,-2 と降順に負数を入れていく
        #

        is_searched = False

        route_board[friend_k_sq] = 0

        # 今の隣
        adjacent_square_list = RouteSearchSub.create_adjacent_squares(friend_k_sq)

        # 再帰ではなく、ループを使う
        # 幅優先探索
        while 0 < len(adjacent_square_list):
            # 次の次の探索先
            two_adjacent_square_list = []

            for adjacent_sq in adjacent_square_list:
                if KingRouteSearch._search_outward(route_board, control_board, occupied_board, adjacent_sq, remaining_distance - 1):
                    temp_list = RouteSearchSub.create_adjacent_squares(adjacent_sq)
                    two_adjacent_square_list.extend(temp_list)

                # ゴールに至った
                if adjacent_sq == end_sq:
                    print(f"[search] ゴールに至った {adjacent_sq=} {len(adjacent_square_list)=}")
                    is_searched = True
                    break

            adjacent_square_list = two_adjacent_square_list

            remaining_distance -= 1

            if is_searched:
                break

#         # 経路盤（往路）について
#         print(f"""\
# ROUTE BOARD OUTWARD
# -------------------""")
#         for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
#             for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
#                 sq = SquareHelper.file_rank_to_sq(file, rank)
#                 print(f"{route_board[sq]:3} ", end='')
#             print() # 改行
#         print(f"""\
# -------------------""")

        # ゴールに至らないことが分かった時
        if not is_searched:
            print("[search] ゴールに至らないことが分かった時")
            return False

        # DO end に到達した地点で事前探索終了。何回で到達するか数字が分かる
        max_count = abs(remaining_distance)
        #print(f"[search] 復路  {max_count=}  {remaining_distance=}  {len(adjacent_square_list)=}")

        route_board[end_sq] = max_count
        #print(f"[search] ゴール route_board[{end_sq=}] を {max_count=} にする")

        # 今の隣
        adjacent_square_list = RouteSearchSub.create_adjacent_squares(end_sq)

        # 経路盤（往路）について
#         print(f"""\
# ROUTE BOARD 終着点をMAX値にする
# -------------------""")
#         for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
#             for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
#                 sq = SquareHelper.file_rank_to_sq(file, rank)
#                 print(f"{route_board[sq]:3} ", end='')
#             print() # 改行
#         print(f"""\
# -------------------""")

        #
        # DO end から start へ逆順に探索。この探索が本番の探索（確定の探索）。ルート盤のマスの負数を絶対値にしていくとちょうど昇順の正の数になっていく
        #

        is_searched = False

        # 再帰ではなく、ループを使う
        # 幅優先探索
        while 0 < len(adjacent_square_list):
            # 次の次の探索先
            two_adjacent_square_list = []

            for adjacent_sq in adjacent_square_list:
                if KingRouteSearch._search_return(route_board, adjacent_sq, remaining_distance + 1):
                    temp_list = RouteSearchSub.create_adjacent_squares(adjacent_sq)
                    two_adjacent_square_list.extend(temp_list)

            adjacent_square_list = two_adjacent_square_list

            # 負数が０に戻っていく
            remaining_distance += 1

        return True


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
    def new_obj(
            board,
            friend_k_sq,
            opponent_k_sq,
            without_opponet_king_control=False):
        """
        Parameters
        ----------
        without_opponet_king_control : bool
            相手玉の利きは除く
        """

        route_board = [KingRouteSearch._INFINITE] * BOARD_AREA

        # マスに利いている利きの数
        control_board = [0] * BOARD_AREA

        # 自駒の有無
        occupied_board = [0] * BOARD_AREA

        # 全てのマスの自駒の有無を設定
        RouteSearchSub.add_occupied_pieces(
            board,
            occupied_board,
            occupied_without_king=True) # 両玉除く

        # 相手の駒の利きを、利き盤に加算します
        RouteSearchSub.add_opponent_control(board, control_board, without_opponet_king_control)


        # def each_legal_move(move):
        #     # 相手の駒の利きを調べたい
        #     # 利きの数追加
        #     control_board[move.dst_sq] += 1

        # # DO すべての合法手一覧
        # LegalMovesHelper.for_each_legal_move(board, each_legal_move)

#         # 盤上の自駒の有無について
#         print(f"""\
# OCCUPIED
# --------""")
#         for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
#             for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
#                 sq = SquareHelper.file_rank_to_sq(file, rank)
#                 print(f"{occupied_board[sq]:3} ", end='')
#             print() # 改行
#         print(f"""\
# --------""")

#         # 利き盤について
#         print(f"""\
# CONTROL BOARD
# -------------""")
#         for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
#             for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
#                 sq = SquareHelper.file_rank_to_sq(file, rank)
#                 print(f"{control_board[sq]:3} ", end='')
#             print() # 改行
#         print(f"""\
# -------------""")

        # DO 盤上を探索
        is_leached = KingRouteSearch.search(route_board, control_board, occupied_board, friend_k_sq, opponent_k_sq)

        if is_leached:
            # 経路盤（復路）について
            print(f"""\
ROUTE BOARD RETURN
------------------""")
            for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                    sq = SquareHelper.file_rank_to_sq(file, rank)
                    print(f"{route_board[sq]:3} ", end='')
                print() # 改行
            print(f"""\
------------------""")

        return KingRouteSearch(route_board, friend_k_sq, opponent_k_sq)


    def next_sq(self, sq):
        """次のマス。無ければ None"""

        remaining_distance = self._route_board[sq]
        # 昇順に上っていく
        next_distance = remaining_distance + 1

        # 移動不可
        if remaining_distance == KingRouteSearch._INFINITE:
            return None


        # ８方向のどこかに、移動回数が１小さいマスがある
        for adjacent_sq in RouteSearchSub.create_adjacent_squares(sq):
            if self._route_board[adjacent_sq] == next_distance:
                return adjacent_sq


        print(f"[next_sq] ８方向のどこにも移動不可")
        return None


    @property
    def friend_k_sq(self):
        """自玉のあるマス番号"""
        return self._friend_k_sq
    

    @property
    def opponent_k_sq(self):
        """敵玉のあるマス番号"""
        return self._opponent_k_sq
