from library.cshogi_helper import CshogiHelper


class RouteSearchView():


    def print_outward(route_board):
        """経路盤（往路）の表示"""

        print(f"""\
ROUTE BOARD OUTWARD
-------------------""")

        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = CshogiHelper.file_rank_to_sq(file, rank)
                print(f"{route_board[sq]:3} ", end='')
            print() # 改行

        print(f"""\
-------------------""")


    def print_outward2(route_board):
        """経路盤（往路）の表示"""

        print(f"""\
ROUTE BOARD 終着点をMAX値にする
-------------------""")

        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = CshogiHelper.file_rank_to_sq(file, rank)
                print(f"{route_board[sq]:3} ", end='')
            print() # 改行

        print(f"""\
-------------------""")


    def print_occupied(occupied_board):
        """盤上の自駒の有無を表示"""

        print(f"""\
OCCUPIED
--------""")

        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = CshogiHelper.file_rank_to_sq(file, rank)
                print(f"{occupied_board[sq]:3} ", end='')
            print() # 改行

        print(f"""\
--------""")


    def print_control(control_board):
        """利き盤について"""

        print(f"""\
CONTROL BOARD
-------------""")

        for rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            for file in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                sq = CshogiHelper.file_rank_to_sq(file, rank)
                print(f"{control_board[sq]:3} ", end='')
            print() # 改行

        print(f"""\
-------------""")


    def print_return(route_board):
        """経路盤（復路）の表示"""

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
