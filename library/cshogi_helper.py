import cshogi


class CshogiHelper():
    """cshogi ヘルパー"""


    def sq_to_readable(sq):
        """マス番号を、マス符号に変換します。
        駒台はナン"""

        # 駒台
        if sq is None:
            return None
        
        return f"{sq // 9 + 1}{sq % 9 + 1}"


    @staticmethod
    def file_rank_to_sq(file, rank):
        return file * 9 + rank


    @staticmethod
    def piece_to_color(piece):
        # if piece == cshogi.NONE:
        #     return None

        if piece in [cshogi.BPAWN, cshogi.BLANCE, cshogi.BKNIGHT, cshogi.BSILVER, cshogi.BGOLD, cshogi.BBISHOP, cshogi.BROOK, cshogi.BKING, cshogi.BPROM_PAWN, cshogi.BPROM_LANCE, cshogi.BPROM_KNIGHT, cshogi.BPROM_SILVER, cshogi.BPROM_BISHOP, cshogi.BPROM_ROOK]:
            return cshogi.BLACK

        if piece in [cshogi.WPAWN, cshogi.WLANCE, cshogi.WKNIGHT, cshogi.WSILVER, cshogi.WGOLD, cshogi.WBISHOP, cshogi.WROOK, cshogi.WKING, cshogi.WPROM_PAWN, cshogi.WPROM_LANCE, cshogi.WPROM_KNIGHT, cshogi.WPROM_SILVER, cshogi.WPROM_BISHOP, cshogi.WPROM_ROOK]:
            return cshogi.WHITE
        
        raise ValueError(f"{piece=}")


    @staticmethod
    def is_pawn(piece):
        """歩か？"""
        return piece in [cshogi.BPAWN, cshogi.WPAWN]


    @staticmethod
    def is_lance(piece):
        """香か？"""
        return piece in [cshogi.BLANCE, cshogi.WLANCE]


    @staticmethod
    def is_knight(piece):
        """桂か？"""
        return piece in [cshogi.BKNIGHT, cshogi.WKNIGHT]


    @staticmethod
    def is_silver(piece):
        """銀か？"""
        return piece in [cshogi.BSILVER, cshogi.WSILVER]


    @staticmethod
    def is_gold(piece):
        """金か？"""
        return piece in [cshogi.BGOLD, cshogi.WGOLD]


    @staticmethod
    def is_bishop(piece):
        """角か？"""
        return piece in [cshogi.BBISHOP, cshogi.WBISHOP]


    @staticmethod
    def is_rook(piece):
        """飛か？"""
        return piece in [cshogi.BROOK, cshogi.WROOK]


    @staticmethod
    def is_king(piece):
        """玉か？"""
        return piece in [cshogi.BKING, cshogi.WKING]


    @staticmethod
    def is_prom_pawn(piece):
        """と金か？"""
        return piece in [cshogi.BPROM_PAWN, cshogi.WPROM_PAWN]


    @staticmethod
    def is_prom_lance(piece):
        """杏？"""
        return piece in [cshogi.BPROM_LANCE, cshogi.WPROM_LANCE]


    @staticmethod
    def is_prom_silver(piece):
        """全？"""
        return piece in [cshogi.BPROM_SILVER, cshogi.WPROM_SILVER]


    @staticmethod
    def is_prom_bishop(piece):
        """馬？"""
        return piece in [cshogi.BPROM_BISHOP, cshogi.WPROM_BISHOP]


    @staticmethod
    def is_prom_rook(piece):
        """竜？"""
        return piece in [cshogi.BPROM_ROOK, cshogi.WPROM_ROOK]


    @staticmethod
    def friend_pawn_from_black(color):
        """黒番から見て、自駒の歩"""
        if color == cshogi.BLACK:
            return cshogi.BPAWN
        return cshogi.WPAWN


    @staticmethod
    def friend_lance_from_black(color):
        """黒番から見て、自駒の香"""
        if color == cshogi.BLACK:
            return cshogi.BLANCE
        return cshogi.WLANCE


    @staticmethod
    def friend_knight_from_black(color):
        """黒番から見て、自駒の桂"""
        if color == cshogi.BLACK:
            return cshogi.BKNIGHT
        return cshogi.WKNIGHT


    @staticmethod
    def friend_silver_from_black(color):
        """黒番から見て、自駒の銀"""
        if color == cshogi.BLACK:
            return cshogi.BSILVER
        return cshogi.WSILVER


    @staticmethod
    def friend_gold_from_black(color):
        """黒番から見て、自駒の金"""
        if color == cshogi.BLACK:
            return cshogi.BGOLD
        return cshogi.WGOLD


    @staticmethod
    def friend_bishop_from_black(color):
        """黒番から見て、自駒の角"""
        if color == cshogi.BLACK:
            return cshogi.BBISHOP
        return cshogi.WBISHOP


    @staticmethod
    def friend_rook_from_black(color):
        """黒番から見て、自駒の飛"""
        if color == cshogi.BLACK:
            return cshogi.BROOK
        return cshogi.WROOK


    @staticmethod
    def friend_king_from_black(color):
        """黒番から見て、自駒の玉"""
        if color == cshogi.BLACK:
            return cshogi.BKING
        return cshogi.WKING


    @staticmethod
    def friend_prom_pawn_from_black(color):
        """黒番から見て、自駒のと金"""
        if color == cshogi.BLACK:
            return cshogi.BPROM_PAWN
        return cshogi.WPROM_PAWN


    @staticmethod
    def friend_prom_lance_from_black(color):
        """黒番から見て、自駒の杏"""
        if color == cshogi.BLACK:
            return cshogi.BPROM_LANCE
        return cshogi.WPROM_LANCE


    @staticmethod
    def friend_prom_knight_from_black(color):
        """黒番から見て、自駒の圭"""
        if color == cshogi.BLACK:
            return cshogi.BPROM_KNIGHT
        return cshogi.WPROM_KNIGHT


    @staticmethod
    def friend_prom_silver_from_black(color):
        """黒番から見て、自駒の全"""
        if color == cshogi.BLACK:
            return cshogi.BPROM_SILVER
        return cshogi.WPROM_SILVER


    @staticmethod
    def friend_prom_bishop_from_black(color):
        """黒番から見て、自駒の馬"""
        if color == cshogi.BLACK:
            return cshogi.BPROM_BISHOP
        return cshogi.WPROM_BISHOP


    @staticmethod
    def friend_prom_rook_from_black(color):
        """黒番から見て、自駒の竜"""
        if color == cshogi.BLACK:
            return cshogi.BPROM_ROOK
        return cshogi.WPROM_ROOK
