import cshogi
import datetime
import random
from library.shogi import FILE_LEN, RANK_LEN, BOARD_AREA, EAST, NORTH_EAST, NORTH_NORTH_EAST, NORTH, NORTH_WEST, NORTH_NORTH_WEST, WEST, SOUTH_WEST, SOUTH_SOUTH_WEST, SOUTH, SOUTH_EAST, SOUTH_SOUTH_EAST


class UsiEngine():
    """USI エンジン"""


    def __init__(self, engine_file_path):
        """初期化
        
        Parameters
        ----------
        engine_file_path : str
            エンジン名が書かれたテキストファイルへのパス
        """

        self._engine_file_path = engine_file_path

        # 盤
        self._board = cshogi.Board()


    def usi_loop(self):
        """USIループ"""

        while True:

            # 入力
            cmd = input().split(' ', 1)

            # USIエンジン握手
            if cmd[0] == 'usi':
                self.usi()

            # 対局準備
            elif cmd[0] == 'isready':
                self.isready()

            # 新しい対局
            elif cmd[0] == 'usinewgame':
                self.usinewgame()

            # 局面データ解析
            elif cmd[0] == 'position':
                self.position(cmd)

            # 思考開始～最善手返却
            elif cmd[0] == 'go':
                self.go()

            # 中断
            elif cmd[0] == 'stop':
                self.stop()

            # 対局終了
            elif cmd[0] == 'gameover':
                self.gameover(cmd)

            # アプリケーション終了
            elif cmd[0] == 'quit':
                break

            # 以下、独自拡張

            # 一手指す
            # example: ７六歩
            #       code: do 7g7f
            elif cmd[0] == 'do':
                self.do(cmd)

            # 一手戻す
            #       code: undo
            elif cmd[0] == 'undo':
                self.undo()


    def usi(self):
        """USIエンジン握手"""

        # エンジン名は別ファイルから読込。pythonファイルはよく差し替えるのでデータは外に出したい
        try:
            with open(self._engine_file_path, 'r', encoding="utf-8") as f:
                engine_name = f.read().strip()

        except FileNotFoundError as ex:
            print(f"[usi protocol > usi] '{self._engine_file_path}' file not found.  ex:{ex}")
            raise

        print(f'id name {engine_name}')
        print('usiok', flush=True)


    def isready(self):
        """対局準備"""
        print('readyok', flush=True)


    def usinewgame(self):
        """新しい対局"""
        print(f"[{datetime.datetime.now()}] usinewgame end", flush=True)


    def position(self, cmd):
        """局面データ解析"""
        pos = cmd[1].split('moves')
        sfen_text = pos[0].strip()
        # 区切りは半角空白１文字とします
        moves_text = (pos[1].split(' ') if len(pos) > 1 else [])
        self.position_detail(sfen_text, moves_text)


    def position_detail(self, sfen_text, moves_text_as_usi):
        """局面データ解析"""

        # 平手初期局面に変更
        if sfen_text == 'startpos':
            self._board.reset()

        # 指定局面に変更
        elif sfen_text[:5] == 'sfen ':
            self._board.set_sfen(sfen_text[5:])

        # 棋譜再生
        for move_as_usi in moves_text_as_usi:
            self._board.push_usi(move_as_usi)


    def stop(self):
        """中断"""
        print('bestmove resign', flush=True)


    def gameover(self, cmd):
        """対局終了"""

        if 2 <= len(cmd):
            # 負け
            if cmd[1] == 'lose':
                print("（＞＿＜）負けた")

            # 勝ち
            elif cmd[1] == 'win':
                print("（＾▽＾）勝ったぜ！")

            # 持将棋
            elif cmd[1] == 'draw':
                print("（ー＿ー）持将棋か～")

            # その他
            else:
                print(f"（・＿・）何だろな？：'{cmd[1]}'")


    def do(self, cmd):
        """一手指す
        example: ７六歩
            code: do 7g7f
        """
        self._board.push_usi(cmd[1])


    def undo(self):
        """一手戻す
            code: undo
        """
        self._board.pop()


class ColorHelper():
    """先手後手ヘルパー"""


    @staticmethod
    def flip(color):
        if color == cshogi.BLACK:
            return cshogi.WHITE
        
        if color == cshogi.WHITE:
            return cshogi.BLACK

        raise ValueError(f"{color=}")



class SquareHelper():
    """マス番号ヘルパー"""


    @staticmethod
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


    @staticmethod
    def file_rank_to_sq(file, rank):
        return file * 9 + rank


    @staticmethod
    def sq_to_file_rank(sq):
        return (sq // 9, sq % 9)


    @staticmethod
    def can_it_go_east_from_black(color, file):
        """黒番から見て、東に行けるか？"""
        if color == cshogi.BLACK:
            return 0 <= file - 1
        return file + 1 < FILE_LEN


    @staticmethod
    def can_it_go_north_east_from_black(color, file, rank):
        """黒番から見て、北東に行けるか？"""
        if color == cshogi.BLACK:
            return 0 <= file - 1 and 0 <= rank - 1
        return file + 1 < FILE_LEN and rank + 1 < RANK_LEN


    @staticmethod
    def can_it_go_north_north_east_from_black(color, file, rank):
        """黒番から見て、北北東に行けるか？"""
        if color == cshogi.BLACK:
            return 0 <= file - 1 and 0 <= rank - 2
        return file + 1 < FILE_LEN and rank + 2 < RANK_LEN


    @staticmethod
    def can_it_go_north_from_black(color, rank):
        """黒番から見て、北に行けるか？"""
        if color == cshogi.BLACK:
            return 0 <= rank - 1
        return rank + 1 < RANK_LEN


    @staticmethod
    def can_it_go_north_north_from_black(color, rank):
        """黒番から見て、北北に行けるか？"""
        if color == cshogi.BLACK:
            return 0 <= rank - 2
        return rank + 2 < RANK_LEN


    @staticmethod
    def can_it_go_north_north_west_from_black(color, file, rank):
        """黒番から見て、北北西に行けるか？"""
        if color == cshogi.BLACK:
            return file + 1 < FILE_LEN and 0 <= rank - 2
        return 0 <= file - 1 and rank + 2 < RANK_LEN


    @staticmethod
    def can_it_go_north_west_from_black(color, file, rank):
        """黒番から見て、北西に行けるか？"""
        if color == cshogi.BLACK:
            return file + 1 < FILE_LEN and 0 <= rank - 1
        return 0 <= file - 1 and rank + 1 < RANK_LEN


    @staticmethod
    def can_it_go_west_from_black(color, file):
        """黒番から見て、西に行けるか？"""
        if color == cshogi.BLACK:
            return file + 1 < FILE_LEN
        return 0 <= file - 1


    @staticmethod
    def can_it_go_south_west_from_black(color, file, rank):
        """黒番から見て、南西に行けるか？"""
        if color == cshogi.BLACK:
            return file + 1 < FILE_LEN and rank + 1 < RANK_LEN
        return 0 <= file - 1 and 0 <= rank - 1


    @staticmethod
    def can_it_go_south_from_black(color, rank):
        """黒番から見て、南に行けるか？"""
        if color == cshogi.BLACK:
            return rank + 1 < RANK_LEN
        return 0 <= rank - 1


    @staticmethod
    def can_it_go_south_east_from_black(color, file, rank):
        """黒番から見て、南東に行けるか？"""
        if color == cshogi.BLACK:
            return 0 <= file - 1 and rank + 1 < RANK_LEN
        return file + 1 < FILE_LEN and 0 <= rank - 1


    @staticmethod
    def east_of_sq_from_black(color, sq):
        """黒番から見て、東隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_east_from_black(color, file):
                return sq+EAST
            return None
        
        if SquareHelper.can_it_go_east_from_black(color, file):
            return sq+WEST
        return None


    @staticmethod
    def north_east_of_sq_from_black(color, sq):
        """黒番から見て、北東隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_north_east_from_black(color, file=file, rank=rank):
                return sq+NORTH_EAST
            return None
        
        if SquareHelper.can_it_go_north_east_from_black(color, file=file, rank=rank):
            return sq+SOUTH_WEST
        return None


    @staticmethod
    def north_north_east_of_sq_from_black(color, sq):
        """黒番から見て、北北東隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_north_north_east_from_black(color, file=file, rank=rank):
                return sq+NORTH_NORTH_EAST
            return None

        if SquareHelper.can_it_go_north_north_east_from_black(color, file=file, rank=rank):
            return sq+SOUTH_SOUTH_WEST
        return None


    @staticmethod
    def north_of_sq_from_black(color, sq):
        """黒番から見て、北隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_north_from_black(color, rank=rank):
                return sq+NORTH
            return None
        
        if SquareHelper.can_it_go_north_from_black(color, rank=rank):
            return sq+SOUTH
        return None


    @staticmethod
    def north_north_west_of_sq_from_black(color, sq):
        """黒番から見て、北北西隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_north_north_west_from_black(color, file=file, rank=rank):
                return sq+NORTH_NORTH_WEST
            return None

        if SquareHelper.can_it_go_north_north_west_from_black(color, file=file, rank=rank):
            return sq+SOUTH_SOUTH_EAST
        return None


    @staticmethod
    def north_west_of_sq_from_black(color, sq):
        """黒番から見て、北西隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_north_west_from_black(color, file=file, rank=rank):
                return sq+NORTH_WEST
            return None

        if SquareHelper.can_it_go_north_west_from_black(color, file=file, rank=rank):
            return sq+SOUTH_EAST
        return None


    @staticmethod
    def west_of_sq_from_black(color, sq):
        """黒番から見て、西隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_west_from_black(color, file=file):
                return sq+WEST
            return None

        if SquareHelper.can_it_go_west_from_black(color, file=file):
            return sq+EAST
        return None


    @staticmethod
    def south_west_of_sq_from_black(color, sq):
        """TODO 黒番から見て、南西隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_south_west_from_black(color, file=file, rank=rank):
                return sq+SOUTH_WEST
            return None

        if SquareHelper.can_it_go_south_west_from_black(color, file=file, rank=rank):
            return sq+NORTH_EAST
        return None


    @staticmethod
    def south_of_sq_from_black(color, sq):
        """黒番から見て、南隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            if SquareHelper.can_it_go_south_from_black(color, rank=rank):
                return sq+SOUTH
            return None
        
        if SquareHelper.can_it_go_south_from_black(color, rank=rank):
            return sq+NORTH
        return None


    @staticmethod
    def south_east_of_sq_from_black(color, sq):
        """黒番から見て、南東隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if color == cshogi.BLACK:
            (file, rank) = SquareHelper.sq_to_file_rank(sq)
            if SquareHelper.can_it_go_south_east_from_black(color, file=file, rank=rank):
                return sq+SOUTH_EAST
            return None
        
        if SquareHelper.can_it_go_south_east_from_black(color, file=file, rank=rank):
            return sq+NORTH_WEST
        return None


class Move():
    """指し手"""


    def __init__(self,
        src_sq,
        dst_sq):
        """初期化
        
        Parameters
        ----------
        src_sq : int
            移動元マス番号
            駒台ならナン
        dst_sq : int
            移動先マス番号
        """
        self._src_sq = src_sq
        self._dst_sq = dst_sq


    @property
    def src_sq(self):
        """移動元マス番号
        駒台ならナン
        """
        return self._src_sq


    @property
    def dst_sq(self):
        """移動先マス番号"""
        return self._dst_sq


class BoardHelper():
    """盤ヘルパー"""


    @staticmethod
    def get_friend_king_sq(board):
        """自玉が置いてあるマスの番号
        
        Parameters
        ----------
        board : cshogi.Board
            盤
        """
        # 自玉のマス番号
        if board.turn == cshogi.BLACK:
            return board.king_square(cshogi.BLACK)

        return board.king_square(cshogi.WHITE)


    @staticmethod
    def get_opponent_king_sq(board):
        """敵玉が置いてあるマスの番号
        
        Parameters
        ----------
        board : cshogi.Board
            盤
        """
        # 敵玉のマス番号
        if board.turn == cshogi.BLACK:
            return board.king_square(cshogi.WHITE)

        return board.king_square(cshogi.BLACK)


    @staticmethod
    def get_manhattan_distance(p_sq, q_sq):
        """敵玉と、進んだ駒とのマンハッタン距離"""
        (p_file, p_rank) = SquareHelper.sq_to_file_rank(p_sq)
        (q_file, q_rank) = SquareHelper.sq_to_file_rank(q_sq)

        return abs(p_file -  q_file) + abs(p_rank - q_rank)


    @staticmethod
    def positive_number_from_black(color, value):
        """黒番から見て、正の数"""
        if color == cshogi.BLACK:
            return value
        return - value


    @staticmethod
    def rank_from_black(color, rank):
        """黒番から見て、段"""
        if color == cshogi.BLACK:
            return rank
        return RANK_LEN - rank


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


class UsiSquareHelper():
    """Usi マス番号ヘルパー"""


    @staticmethod
    def code_to_sq(code, can_panic=False):
        """

        Parameters
        ----------
        code : str
            例： `7g` - ７筋、７段
        
        Returns
        -------
        マス番号、駒台の駒を指してたらナン
        """

        # TODO 打ではマス番号は返せません
        if code[0:1] in ['P', 'L', 'N', 'S', 'G', 'B', 'R']:
            if can_panic:
                raise ValueError(f"it is drop move. {code=}")
            
            return None

        else:
            file_th = int(code[0: 1])
            rank_th = SquareHelper.a_to_i(code[1: 2])

        return SquareHelper.file_rank_to_sq(file_th - 1, rank_th - 1)


class UsiMoveHelper():
    """USI 指し手ヘルパー"""


    @staticmethod
    def code_to_move(code):
        return Move(
            # 移動元マス番号 FIXME 駒台注意
            src_sq=UsiSquareHelper.code_to_sq(code[0: 2]),
            # 移動先マス番号
            dst_sq=UsiSquareHelper.code_to_sq(code[2: 4], can_panic=True))


class HumanHelper():
    """人間ヘルパー"""

    def sq_to_readable(sq):
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        return f"{file + 1}{rank + 1}"
