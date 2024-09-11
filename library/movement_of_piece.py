import cshogi
from py_kifuwarabe_trainer import SquareHelper


class MovementOfKnight():
    """桂の動き
    
    桂は２方向に移動できます。先手後手で動きが異なります
    """


    def __init__(self, color):
        """初期化"""
        self._color = color


    def create_control_squares(self, sq):
        """利きの届くマス番号のリスト生成"""

        if self._color == cshogi.BLACK:
            # +---+---+---+
            # + 2 |   | 1 |
            # +---+---+---+
            # +   |   |   |
            # +---+---+---+
            # +   |you|   |
            # +---+---+---+
            # +   |   |   |
            # +---+---+---+
            #
            # リストの要素に None が含まれることに注意
            items = [
                SquareHelper.north_north_east_of_sq_from_black(self._color, sq),      # 1. 北北東
                SquareHelper.north_north_west_of_sq_from_black(self._color, sq),      # 2. 北北西
            ]
        
        else:
            # +---+---+---+
            # +   |   |   |
            # +---+---+---+
            # +   |you|   |
            # +---+---+---+
            # +   |   |   |
            # +---+---+---+
            # + 1 |   | 2 |
            # +---+---+---+
            #
            # リストの要素に None が含まれることに注意
            items = [
                SquareHelper.south_south_west_of_sq_from_black(self._color, sq),      # 1. 南南西
                SquareHelper.south_south_east_of_sq_from_black(self._color, sq),      # 2. 南南東
            ]

        # リストの要素から None を除去
        return list(filter(None, items))


class MovementOfSilver():
    """銀の動き
    
    銀は５方向に移動できます。先手後手で動きが異なります
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
            # +   |   |   |
            # +---+---+---+
            # + x |   | x |
            # +---+---+---+
            #
            # リストの要素に None が含まれることに注意
            items = [
                SquareHelper.north_east_of_sq_from_black(self._color, sq),      # 北東
                SquareHelper.north_of_sq_from_black(self._color, sq),           # 北
                SquareHelper.north_west_of_sq_from_black(self._color, sq),      # 北西
                SquareHelper.south_west_of_sq_from_black(self._color, sq),      # 南西
                SquareHelper.south_east_of_sq_from_black(self._color, sq),      # 南東
            ]
        
        else:
            # +---+---+---+
            # + x |   | x |
            # +---+---+---+
            # +   |   |   |
            # +---+---+---+
            # + x | x | x |
            # +---+---+---+
            #
            # リストの要素に None が含まれることに注意
            items = [
                SquareHelper.north_east_of_sq_from_black(self._color, sq),      # 北東
                SquareHelper.north_west_of_sq_from_black(self._color, sq),      # 北西
                SquareHelper.south_west_of_sq_from_black(self._color, sq),      # 南西
                SquareHelper.south_of_sq_from_black(self._color, sq),           # 南
                SquareHelper.south_east_of_sq_from_black(self._color, sq),      # 南東
            ]

        # リストの要素から None を除去
        return list(filter(None, items))


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
