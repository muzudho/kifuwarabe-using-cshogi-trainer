import cshogi
import datetime
import random


_engine_file_path = "engine_1_0/engine_name.txt"


class UsiEngine():
    """USI エンジン"""


    def __init__(self):
        """初期化"""

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
            with open(_engine_file_path, 'r', encoding="utf-8") as f:
                engine_name = f.read().strip()

        except FileNotFoundError as ex:
            print(f"[usi protocol > usi] '{_engine_file_path}' file not found.  ex:{ex}")
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


    def go(self):
        """思考開始～最善手返却"""

        if self._board.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if self._board.is_nyugyoku():
            """入玉宣言局面時"""

            # 勝利宣言
            print(f'bestmove win', flush=True)
            return

        # 一手詰めを詰める
        if not self._board.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._board.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""

                best_move = cshogi.move_to_usi(matemove)
                print('info score mate 1 pv {}'.format(best_move), flush=True)
                print(f'bestmove {best_move}', flush=True)
                return

        # 投了のケースは対応済みなので、以降では指し手が必ず１つ以上ある

        # １手指す
        # --------

        # 敵玉のマス番号
        if self._board.turn == cshogi.BLACK:
            opponent_k_sq = self._board.king_square(cshogi.WHITE)
        else:
            opponent_k_sq = self._board.king_square(cshogi.BLACK)


        # 敵玉と、進んだ駒とのマンハッタン距離
        def get_distance(opponent_k_sq, p_file_th, p_rank_th):
            opponent_k_file = opponent_k_sq // 9 + 1
            opponent_k_rank = opponent_k_sq % 9 + 1

            return abs(opponent_k_file - p_file_th) + abs(opponent_k_rank - p_rank_th)


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

        # 相手玉と、進んだ駒の距離が最小の手を指す。
        #
        #   盤は１辺９マスなので、１番離れているとき８マス。それが２辺で１６マス。
        #   だから　１７マス離れることはない
        #
        nearest_distance = 8 + 8 + 1
        nearest_move_u = None

        move_list = list(self._board.legal_moves)
        random.shuffle(move_list)

        for move in move_list:
            # USI符号
            move_u = cshogi.move_to_usi(move)
            # 移動先
            dst_file_th = int(move_u[2: 3])
            dst_rank_th = a_to_i(move_u[3: 4])
            # 敵玉とのマンハッタン距離
            d = get_distance(opponent_k_sq, dst_file_th, dst_rank_th)

            if d < nearest_distance:
                nearest_distance = d
                nearest_move_u = move_u

        print(f"info depth 0 seldepth 0 time 1 nodes 0 score cp 0 Closest to king")
        print(f'bestmove {nearest_move_u}', flush=True)


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
