import cshogi
from py_kifuwarabe_trainer import ColorHelper, SquareHelper, BoardHelper
from library.cshogi_helper import CshogiHelper
from library.shogi import FILE_LEN, RANK_LEN, BOARD_AREA, EAST, NORTH_EAST, NORTH_NORTH_EAST, NORTH, NORTH_WEST, NORTH_NORTH_WEST, WEST, SOUTH_WEST, SOUTH_SOUTH_WEST, SOUTH, SOUTH_EAST, SOUTH_SOUTH_EAST
from library.engine_helper import LegalMovesHelper
from library.view import RouteSearchView


class MovementOfGold():
    """金の動き
    
    金は６方向に移動できます。先手後手で動きが異なります
    """


    def __init__(self, color):
        """初期化"""
        self._color = color


    def create_control_squares(self, sq):
        """利きの届くマス番号のリスト生成"""

        if self._color == cshogi.BLACK:
            # +---+---+---+
            # + x | x | x |
            # +---+---+---+
            # + x |   | x |
            # +---+---+---+
            # +   | x |   |
            # +---+---+---+
            #
            # リストの要素に None が含まれることに注意
            items = [
                SquareHelper.east_of_sq_from_black(self._color, sq),            # 東
                SquareHelper.north_east_of_sq_from_black(self._color, sq),      # 北東
                SquareHelper.north_of_sq_from_black(self._color, sq),           # 北
                SquareHelper.north_west_of_sq_from_black(self._color, sq),      # 北西
                SquareHelper.west_of_sq_from_black(self._color, sq),            # 西
                SquareHelper.south_of_sq_from_black(self._color, sq),           # 南
            ]
        
        else:
            # +---+---+---+
            # +   | x |   |
            # +---+---+---+
            # + x |   | x |
            # +---+---+---+
            # + x | x | x |
            # +---+---+---+
            #
            # リストの要素に None が含まれることに注意
            items = [
                SquareHelper.east_of_sq_from_black(self._color, sq),            # 東
                SquareHelper.north_of_sq_from_black(self._color, sq),           # 北
                SquareHelper.west_of_sq_from_black(self._color, sq),            # 西
                SquareHelper.south_west_of_sq_from_black(self._color, sq),      # 南西
                SquareHelper.south_of_sq_from_black(self._color, sq),           # 南
                SquareHelper.south_east_of_sq_from_black(self._color, sq),      # 南東
            ]

        # リストの要素から None を除去
        return list(filter(None, items))


class MovementOfKing():
    """玉の動き
    
    玉は８方向に移動できます。
    """


    def __init__(self, color):
        """初期化"""
        self._color = color


    def create_control_squares(self, sq):
        """利きの届くマス番号のリスト生成

        先手も後手も同じです
        """

        # +---+---+---+
        # + x | x | x |
        # +---+---+---+
        # + x |   | x |
        # +---+---+---+
        # + x | x | x |
        # +---+---+---+
        #
        # リストの要素に None が含まれることに注意
        items = [
            SquareHelper.east_of_sq_from_black(cshogi.BLACK, sq),       # 東
            SquareHelper.north_east_of_sq_from_black(cshogi.BLACK, sq), # 北東
            SquareHelper.north_of_sq_from_black(cshogi.BLACK, sq),      # 北
            SquareHelper.north_west_of_sq_from_black(cshogi.BLACK, sq), # 北西
            SquareHelper.west_of_sq_from_black(cshogi.BLACK, sq),       # 西
            SquareHelper.south_west_of_sq_from_black(cshogi.BLACK, sq), # 南西
            SquareHelper.south_of_sq_from_black(cshogi.BLACK, sq),      # 南
            SquareHelper.south_east_of_sq_from_black(cshogi.BLACK, sq), # 南東
        ]

        # リストの要素から None を除去
        return list(filter(None, items))


class RouteSearchSub():
    """経路探索サブクラス"""


    # 目的地に到達できない距離の印。数字に続きがないことを表す符牒
    _TERMINATE_OF_ROUTE = 99


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
            control_sq = CshogiHelper.file_rank_to_sq(control_file, control_rank)
            control_board[control_sq] += 1

            if board.piece(control_sq) != 0:
                break

        # 北西への動き
        for delta in range(1, min(FILE_LEN, RANK_LEN)):
            control_file = file + delta
            control_rank = rank - delta
            if FILE_LEN <= control_file or control_rank < 0:
                break
            control_sq = CshogiHelper.file_rank_to_sq(control_file, control_rank)
            control_board[control_sq] += 1

            if board.piece(control_sq) != 0:
                break

        # 南西への動き
        for delta in range(1, min(FILE_LEN, RANK_LEN)):
            control_file = file + delta
            control_rank = rank + delta
            if FILE_LEN <= control_file or RANK_LEN <= control_rank:
                break
            control_sq = CshogiHelper.file_rank_to_sq(control_file, control_rank)
            control_board[control_sq] += 1

            if board.piece(control_sq) != 0:
                break

        # 南東への動き
        for delta in range(1, min(FILE_LEN, RANK_LEN)):
            control_file = file - delta
            control_rank = rank + delta
            if control_file < 0 or RANK_LEN <= control_rank:
                break
            control_sq = CshogiHelper.file_rank_to_sq(control_file, control_rank)
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
            control_sq = CshogiHelper.file_rank_to_sq(control_file, rank)
            control_board[control_sq] += 1

            if board.piece(control_sq) != 0:
                break

        # 北への動き
        for delta in range(1, RANK_LEN):
            control_rank = rank - delta
            if control_rank < 0:
                break
            control_sq = CshogiHelper.file_rank_to_sq(file, control_rank)
            control_board[control_sq] += 1

            if board.piece(control_sq) != 0:
                break

        # 西への動き
        for delta in range(1, FILE_LEN):
            control_file = file + delta
            if FILE_LEN <= control_file:
                break
            control_sq = CshogiHelper.file_rank_to_sq(control_file, rank)
            control_board[control_sq] += 1

            if board.piece(control_sq) != 0:
                break

        # 南への動き
        for delta in range(1, RANK_LEN):
            control_rank = rank + delta
            if RANK_LEN <= control_rank:
                break
            control_sq = CshogiHelper.file_rank_to_sq(file, control_rank)
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
            if piece == CshogiHelper.friend_pawn_from_black(opponent_color):
                # 黒番から見て北に利きを１つ追加
                next_sq = SquareHelper.north_of_sq_from_black(opponent_color, sq)
                if next_sq is not None:
                    control_board[next_sq] += 1

            # 相手の香の利き
            elif piece == CshogiHelper.friend_lance_from_black(opponent_color):
                for delta in range(1, BoardHelper.rank_from_black(opponent_color, rank)):
                    control_rank = rank - BoardHelper.positive_number_from_black(opponent_color, delta)
                    control_sq = CshogiHelper.file_rank_to_sq(file, control_rank)
                    control_board[control_sq] += 1
                    if board.piece(control_sq) != 0:
                        break

            # 相手の桂の利き
            elif piece == CshogiHelper.friend_knight_from_black(opponent_color):
                # 黒番から見て北北に行けるか？
                if SquareHelper.can_it_go_north_north_from_black(opponent_color, rank=rank):
                    # 黒番から見て東に行けるか？
                    if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                        # 黒番から見て北北東に利きを１つ追加
                        next_sq = SquareHelper.north_north_east_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1
                    
                    # 黒番から見て西に行けるか？
                    if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                        # 黒番から見て北北西に利きを１つ追加
                        next_sq = SquareHelper.north_north_west_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

            # 相手の銀の利き
            elif piece == CshogiHelper.friend_silver_from_black(opponent_color):
                # 黒番から見て北に行けるか？
                if SquareHelper.can_it_go_north_from_black(opponent_color, rank=rank):
                    # 黒番から見て東に行けるか？
                    if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                        # 黒番から見て北東に利きを１つ追加
                        next_sq = SquareHelper.north_east_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                    # 黒番から見て北に利きを１つ追加
                    next_sq = SquareHelper.north_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                    # 黒番から見て西に行けるか？
                    if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                        # 黒番から見て北西に利きを１つ追加
                        next_sq = SquareHelper.north_west_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                # 黒番から見て南に行けるか？
                if SquareHelper.can_it_go_south_from_black(opponent_color, rank=rank):
                    # 黒番から見て西に行けるか？
                    if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                        # 黒番から見て南西に利きを１つ追加
                        next_sq = SquareHelper.south_west_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                    # 黒番から見て東に行けるか？
                    if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                        # 黒番から見て南東に利きを１つ追加
                        next_sq = SquareHelper.south_east_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

            # 相手の金と杏圭全の利き
            elif piece in [
                CshogiHelper.friend_gold_from_black(opponent_color),
                CshogiHelper.friend_prom_pawn_from_black(opponent_color),
                CshogiHelper.friend_prom_lance_from_black(opponent_color),
                CshogiHelper.friend_prom_knight_from_black(opponent_color),
                CshogiHelper.friend_prom_silver_from_black(opponent_color)]:

                # 黒番から見て東に行けるか？
                if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                    # 黒番から見て東に利きを１つ追加
                    next_sq = SquareHelper.west_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                # 黒番から見て北に行けるか？
                if SquareHelper.can_it_go_north_from_black(opponent_color, rank=rank):
                    # 黒番から見て東に行けるか？
                    if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                        # 黒番から見て南西に利きを１つ追加
                        next_sq = SquareHelper.north_east_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                    # 黒番から見て北に利きを１つ追加
                    next_sq = SquareHelper.north_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                    # 黒番から見て西に行けるか？
                    if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                        # 黒番から見て北西に利きを１つ追加
                        next_sq = SquareHelper.north_west_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                # 黒番から見て西に行けるか？
                if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                    # 黒番から見て西に利きを１つ追加
                    next_sq = SquareHelper.west_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                # 黒番から見て南に行けるか？
                if SquareHelper.can_it_go_south_from_black(opponent_color, rank=rank):
                    # 黒番から見て南に利きを１つ追加
                    next_sq = SquareHelper.south_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

            # 相手の角の利き
            elif piece == CshogiHelper.friend_bishop_from_black(opponent_color):
                RouteSearchSub.append_control_of_bishop(board, control_board, file, rank)

            # 相手の飛の利き
            elif piece == CshogiHelper.friend_rook_from_black(opponent_color):
                RouteSearchSub.append_control_of_rook(board, control_board, file, rank)

            # 相手の玉の利き
            elif piece == CshogiHelper.friend_king_from_black(opponent_color):
                if without_opponet_king_control:
                    continue

                # 黒番から見て東に行けるか？
                if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                    # 黒番から見て東に利きを１つ追加
                    next_sq = SquareHelper.west_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                # 黒番から見て北に行けるか？
                if SquareHelper.can_it_go_north_from_black(opponent_color, rank=rank):
                    # 黒番から見て東に行けるか？
                    if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                        # 黒番から見て南西に利きを１つ追加
                        next_sq = SquareHelper.north_east_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                    # 黒番から見て北に利きを１つ追加
                    next_sq = SquareHelper.north_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                    # 黒番から見て西に行けるか？
                    if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                        # 黒番から見て北西に利きを１つ追加
                        next_sq = SquareHelper.north_west_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                # 黒番から見て西に行けるか？
                if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                    # 黒番から見て西に利きを１つ追加
                    next_sq = SquareHelper.west_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                # 黒番から見て南に行けるか？
                if SquareHelper.can_it_go_south_from_black(opponent_color, rank=rank):
                    # 黒番から見て西に行けるか？
                    if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                        # 黒番から見て南西に利きを１つ追加
                        next_sq = SquareHelper.south_west_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                    # 黒番から見て南に利きを１つ追加
                    next_sq = SquareHelper.south_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                       control_board[next_sq] += 1

                    # 黒番から見て東に行けるか？
                    if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                        # 黒番から見て南東に利きを１つ追加
                        next_sq = SquareHelper.south_east_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

            # 相手の馬の利き
            elif piece == CshogiHelper.friend_prom_bishop_from_black(opponent_color):
                RouteSearchSub.append_control_of_bishop(board, control_board, file, rank)

                # 黒番から見て北に行けるか？
                if SquareHelper.can_it_go_north_from_black(opponent_color, rank=rank):
                    # 黒番から見て東に行けるか？
                    if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                        # 黒番から見て南西に利きを１つ追加
                        next_sq = SquareHelper.north_east_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                    # 黒番から見て西に行けるか？
                    if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                        # 黒番から見て北西に利きを１つ追加
                        next_sq = SquareHelper.north_west_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                # 黒番から見て南に行けるか？
                if SquareHelper.can_it_go_south_from_black(opponent_color, rank=rank):
                    # 黒番から見て西に行けるか？
                    if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                        # 黒番から見て南西に利きを１つ追加
                        next_sq = SquareHelper.south_west_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

                    # 黒番から見て東に行けるか？
                    if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                        # 黒番から見て南東に利きを１つ追加
                        next_sq = SquareHelper.south_east_of_sq_from_black(opponent_color, sq)
                        if next_sq is not None:
                            control_board[next_sq] += 1

            # 相手の竜の利き
            elif piece == CshogiHelper.friend_prom_rook_from_black(opponent_color):
                RouteSearchSub.append_control_of_rook(board, control_board, file, rank)

                # 黒番から見て東に行けるか？
                if SquareHelper.can_it_go_east_from_black(opponent_color, file=file):
                    # 黒番から見て東に利きを１つ追加
                    next_sq = SquareHelper.west_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                # 黒番から見て北に行けるか？
                if SquareHelper.can_it_go_north_from_black(opponent_color, rank=rank):
                    # 黒番から見て北に利きを１つ追加
                    next_sq = SquareHelper.north_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                # 黒番から見て西に行けるか？
                if SquareHelper.can_it_go_west_from_black(opponent_color, file=file):
                    # 黒番から見て西に利きを１つ追加
                    next_sq = SquareHelper.west_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1

                # 黒番から見て南に行けるか？
                if SquareHelper.can_it_go_south_from_black(opponent_color, rank=rank):
                    # 黒番から見て南に利きを１つ追加
                    next_sq = SquareHelper.south_of_sq_from_black(opponent_color, sq)
                    if next_sq is not None:
                        control_board[next_sq] += 1


class RouteSearch():
    """駒の経路探索
    
    駒は種類ごとに移動方法が異なります。
    それらは除き、それ以外のことでは、駒は盤上の利きの無いところは移動できると仮定し、
    その盤上で開始地点と目標地点の最短経路を探索します
    """


    @staticmethod
    def _search_outward(route_board, control_board, occupied_board, adjacent_of_end_sq, remaining_distance):
        if route_board[adjacent_of_end_sq] == RouteSearchSub._TERMINATE_OF_ROUTE and control_board[adjacent_of_end_sq] == 0 and occupied_board[adjacent_of_end_sq] == 0:
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
    def search(route_board, control_board, occupied_board, movement_of_piece, start_sq, goal_sq, remaining_distance=0):
        """start から goal_sq への最短経路を探します

        Parameters
        ----------
        route_board : list
            経路の記憶
        control_board : list
            敵駒の利きの数
        occupied_board : list
            自駒の有無
        start_sq : int
            開始地点のマス番号
        goal_sq : int
            目的地のマス番号
        remaining_distance : int
            玉の残り最短移動回数
        """

        #
        # DO start から end へ向かって事前探索を行う（候補挙げの探索）。 0 から -1,-2 と降順に負数を入れていく
        #

        is_searched = False

        route_board[start_sq] = 0

        # 駒の利きが届くマス
        adjacent_square_list = movement_of_piece.create_control_squares(start_sq)

        # 再帰ではなく、ループを使う
        # 幅優先探索
        while 0 < len(adjacent_square_list):
            # 次の次の探索先
            two_adjacent_square_list = []

            for adjacent_sq in adjacent_square_list:
                if RouteSearch._search_outward(route_board, control_board, occupied_board, adjacent_sq, remaining_distance - 1):
                    temp_list = movement_of_piece.create_control_squares(adjacent_sq)
                    two_adjacent_square_list.extend(temp_list)

                # ゴールに至った
                if adjacent_sq == goal_sq:
                    print(f"[search] ゴールに至った {adjacent_sq=} {len(adjacent_square_list)=}")
                    is_searched = True
                    break

            adjacent_square_list = two_adjacent_square_list

            remaining_distance -= 1

            if is_searched:
                break

        # 経路盤（往路）
        RouteSearchView.print_outward(route_board)

        # ゴールに至らないことが分かった時
        if not is_searched:
            print("[search] ゴールに至らないことが分かった時")
            return False

        # DO end に到達した地点で事前探索終了。何回で到達するか数字が分かる
        max_count = abs(remaining_distance)
        #print(f"[search] 復路  {max_count=}  {remaining_distance=}  {len(adjacent_square_list)=}")

        route_board[goal_sq] = max_count
        #print(f"[search] ゴール route_board[{goal_sq=}] を {max_count=} にする")

        # 駒の利きが届くマス
        adjacent_square_list = movement_of_piece.create_control_squares(goal_sq)

        # 経路盤（往路２）
        RouteSearchView.print_outward2(route_board)

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
                if RouteSearch._search_return(route_board, adjacent_sq, remaining_distance + 1):
                    temp_list = movement_of_piece.create_control_squares(adjacent_sq)
                    two_adjacent_square_list.extend(temp_list)

            adjacent_square_list = two_adjacent_square_list

            # 負数が０に戻っていく
            remaining_distance += 1

        return True


    def __init__(self, route_board, start_sq, goal_sq):
        """初期化
        
        Parameters
        ----------
        route_board : list
            盤上の経路
            敵玉への残り最短移動回数
            到達できない場合は 99 でも入れておく
        start_sq : int
            開始地点のマス番号
        goal_sq : int
            目的地のマス番号
        """

        self._start_sq = start_sq
        self._goal_sq = goal_sq
        self._route_board = route_board


    @staticmethod
    def new_obj(
            board,
            start_sq,
            goal_sq,
            without_opponet_king_control=False):
        """
        Parameters
        ----------
        without_opponet_king_control : bool
            相手玉の利きは除く
        """

        route_board = [RouteSearchSub._TERMINATE_OF_ROUTE] * BOARD_AREA

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

        # 盤上の自駒の有無について
        RouteSearchView.print_occupied(occupied_board)

        # 利き盤について
        RouteSearchView.print_control(control_board)

        # DO 盤上を探索
        is_leached = RouteSearch.search(route_board, control_board, occupied_board, MovementOfKing(board.turn), start_sq, goal_sq)

        if is_leached:
            # 経路盤（復路）について
            print(f"""\
ROUTE BOARD RETURN
------------------""")
            for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                    sq = CshogiHelper.file_rank_to_sq(file, rank)
                    print(f"{route_board[sq]:3} ", end='')
                print() # 改行
            print(f"""\
------------------""")

        return RouteSearch(route_board, start_sq, goal_sq)


    def next_sq(self, movement_of_piece, sq):
        """次のマス。無ければ None"""

        # 探索の現在地点のマスに記録されている移動回数
        number_of_moves = self._route_board[sq]

        # 移動不可。続きの番号がない
        if number_of_moves == RouteSearchSub._TERMINATE_OF_ROUTE:
            return None

        # １つ大きな移動回数。昇順に上っていく。 successor は後者の意味
        successor_number_of_moves = number_of_moves + 1


        # 駒の利きが届くマスについて
        for adjacent_sq in movement_of_piece.create_control_squares(sq):
            if self._route_board[adjacent_sq] == successor_number_of_moves:
                return adjacent_sq


        print(f"[next_sq] ８方向のどこにも移動不可")
        return None


    @property
    def start_sq(self):
        """開始地点のマス番号"""
        return self._start_sq
    

    @property
    def goal_sq(self):
        """目的地のマス番号"""
        return self._goal_sq
