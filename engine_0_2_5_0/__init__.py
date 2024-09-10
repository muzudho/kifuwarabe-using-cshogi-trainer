import cshogi
import datetime
import random
from py_kifuwarabe_trainer import UsiEngine, SquareHelper, BoardHelper, UsiSquareHelper, UsiMoveHelper, HumanHelper
from library.cshogi_helper import CshogiHelper
from library.route_search import MovementOfGold, MovementOfKing, RouteSearch


_engine_file_path = "engine_0_2_5_0/engine_name.txt"


class UsiEngine_0_2_5_0(UsiEngine):
    """USI エンジン Lv. 0.25"""


    def __init__(self):
        """初期化"""
        super().__init__(
            engine_file_path=_engine_file_path)


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

        move_list = list(self._board.legal_moves)

        if len(move_list) < 1:
            print("[go] 合法手無し")
            best_move_u = "resign"

        # 自玉が王手されていたら
        elif self._board.is_check():
            print("[go] 自玉が王手されてる")
            best_move_u = cshogi.move_to_usi(random.sample(move_list, 1)[0])
        
        else:
            best_move_u = None

            # 玉のマス番号
            friend_king_sq = BoardHelper.get_friend_king_sq(self._board)
            opponent_king_sq = BoardHelper.get_opponent_king_sq(self._board)

            # 駒の経路探索開始
            gold_route_search = None
            king_route_search = None

            # 駒の経路探索終了
            is_gold_route_searched = False
            is_king_route_searched = False

            # 駒の最短経路の次の移動先マス。無ければナン
            friend_gold_next_sq = None
            friend_king_next_sq = None

            # 相手玉と、進んだ駒の距離が縮まる動きのうち、相手玉から一番遠い駒を選ぶ
            #
            #   盤は１辺９マスなので、１番離れているとき８マス。それが２辺で１６マス。
            #   だから　１７マス離れることはない
            #
            farthest_distance = 0
            #nearest_distance = 8 + 8 + 1

            # シャッフルしておくこと
            random.shuffle(move_list)

            # 指し手一覧ループ
            for move in move_list:
                #print("指し手一覧ループ")

                # USI符号
                move_u = cshogi.move_to_usi(move)

                # 指し手オブジェクト
                move = UsiMoveHelper.code_to_move(
                    code=move_u)

                # 指し手の先の駒
                dst_piece = self._board.piece(move.dst_sq)
                #print(f"{dst_piece=}")

                # 駒を取るような動きはしません（ただし、玉は最短経路を進みたいので、玉は除く）
                if dst_piece != 0 and move.src_sq != friend_king_sq:
                    continue

                # 動かした駒の移動元位置と、敵玉とのマンハッタン距離
                if move.src_sq is None:
                    d_of_src = 99
                else:
                    d_of_src = BoardHelper.get_manhattan_distance(opponent_king_sq, move.src_sq)

                # 動かした駒の移動先位置と、敵玉とのマンハッタン距離
                d_of_dst = BoardHelper.get_manhattan_distance(opponent_king_sq, move.dst_sq)
                #print(f"{d=}")
                #print(f"min_d={nearest_distance}  {d=}  opponent_k_masu={HumanHelper.sq_to_readable(opponent_king_sq)}  dst_masu={HumanHelper.sq_to_readable(move.dst_sq)}")

                # 盤上の自金が移動した場合（金の最短経路をまだ選んでいない場合）
                if move.src_sq is not None and CshogiHelper.is_gold(self._board.piece(move.src_sq)):

                    # 既に最短経路を選んでいる場合は無視
                    if is_gold_route_searched:
                        continue

                    if gold_route_search is None:
                        gold_route_search = RouteSearch.new_obj(
                                board=self._board,
                                # 開始地点（自駒のある場所）のマス番号
                                start_sq=move.src_sq,
                                # 目的地（敵玉のある場所）のマス番号
                                goal_sq=opponent_king_sq,
                                # 敵玉自身の利きは無視する
                                without_opponet_king_control=True)

                    if friend_gold_next_sq is None:
                        friend_gold_next_sq = gold_route_search.next_sq(MovementOfGold(self._board.turn), gold_route_search.start_sq)
                        print(f"[go] 金の経路の次の移動先マス。無ければナン {friend_gold_next_sq=}  {gold_route_search.start_sq=}")

                    # 当該駒が敵玉へ近づく最短経路上を進んでいるなら、 d と関係なくこの指し手で更新
                    if friend_gold_next_sq is not None and move.dst_sq == friend_gold_next_sq:
                        best_move_u = move_u
                        is_gold_route_searched = True

                # 盤上の自玉が移動した場合（玉は盤上に限られるが）（玉の最短経路をまだ選んでいない場合）
                if move.src_sq is not None and CshogiHelper.is_king(self._board.piece(move.src_sq)):

                    # 既に最短経路を選んでいる場合は無視
                    if is_king_route_searched:
                        continue

                    if king_route_search is None:
                        king_route_search = RouteSearch.new_obj(
                                board=self._board,
                                # 開始地点（自駒のある場所）のマス番号
                                start_sq=move.src_sq,
                                # 目的地（敵玉のある場所）のマス番号
                                goal_sq=opponent_king_sq,
                                # 敵玉自身の利きは無視する
                                without_opponet_king_control=True)

                    if friend_king_next_sq is None:
                        friend_king_next_sq = king_route_search.next_sq(MovementOfKing(self._board.turn), king_route_search.start_sq)
                        print(f"[go] 玉の経路の次の移動先マス。無ければナン {friend_king_next_sq=}  {king_route_search.start_sq=}")

                    # 当該駒が敵玉へ近づく最短経路上を進んでいるなら、 d と関係なくこの指し手で更新
                    if friend_king_next_sq is not None and move.dst_sq == friend_king_next_sq:
                        best_move_u = move_u
                        is_king_route_searched = True
                        
                # それ以外の駒なら

                # 相手玉と、進んだ駒の距離が縮まる動きだ。かつ、相手玉から一番遠い駒だ
                if d_of_dst < d_of_src and farthest_distance < d_of_src:
                    farthest_distance = d_of_src
                    best_move_u = move_u

            #print("指し手一覧ループ終了")

            # 指し手が無ければ、指せる手をどれでも選ぶ
            if best_move_u is None:
                print("[go] 指し手が無ければ、指せる手をどれでも選ぶ")
                best_move_u = cshogi.move_to_usi(random.sample(move_list, 1)[0])


        print(f"""\
info depth 0 seldepth 0 time 1 nodes 0 score cp 0 I feed.
bestmove {best_move_u}""", flush=True)
