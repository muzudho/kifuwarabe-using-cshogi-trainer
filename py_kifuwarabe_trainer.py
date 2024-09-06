import cshogi
import datetime
import random
from library.shogi import FILE_LEN, RANK_LEN


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
    def get_east_of(sq):
        """東隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if 0 < file:
            return SquareHelper.file_rank_to_sq(file-1, rank)
        
        return None


    @staticmethod
    def get_north_east_of(sq):
        """東北隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if 0 < file and 0 < rank:
            return SquareHelper.file_rank_to_sq(file-1, rank-1)
        
        return None


    @staticmethod
    def get_north_of(sq):
        """北隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if 0 < rank:
            return SquareHelper.file_rank_to_sq(file, rank-1)
        
        return None


    @staticmethod
    def get_north_west_of(sq):
        """北西隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if file + 1 < FILE_LEN and 0 < rank:
            return SquareHelper.file_rank_to_sq(file+1, rank-1)
        
        return None


    @staticmethod
    def get_west_of(sq):
        """西隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if file + 1 < FILE_LEN:
            return SquareHelper.file_rank_to_sq(file+1, rank)
        
        return None


    @staticmethod
    def get_south_west_of(sq):
        """南西隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if file + 1 < FILE_LEN and rank + 1 < RANK_LEN:
            return SquareHelper.file_rank_to_sq(file+1, rank+1)
        
        return None


    @staticmethod
    def get_south_of(sq):
        """南隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if rank + 1 < RANK_LEN:
            return SquareHelper.file_rank_to_sq(file, rank + 1)
        
        return None


    @staticmethod
    def get_south_east_of(sq):
        """南東隣のマス番号を取得

        Returns
        -------
        マス番号。該当なしならナン
        """
        (file, rank) = SquareHelper.sq_to_file_rank(sq)
        if 0 < file and rank + 1 < RANK_LEN:
            return SquareHelper.file_rank_to_sq(file - 1, rank + 1)
        
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
