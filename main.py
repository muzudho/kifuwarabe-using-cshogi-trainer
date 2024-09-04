# python main.py 1.0
import sys
from engine_0_5_0 import UsiEngine_0_5_0
from engine_1_0 import UsiEngine_1_0


if __name__ == '__main__':
    """コマンドから実行時"""

    try:
        # 例えば `python main.py 1.0` というコマンドなら、
        # args=['main.py', '1.0'] といった具合に取得できる
        args = sys.argv
        #print(f"{args=}")

        usi_engine = None

        # 引数が付いていなければ、デフォルトのレベルを使う
        if len(args) < 2:
            pass

        elif args[1] == '0.5':
            usi_engine = UsiEngine_0_5_0()


        if usi_engine is None:
            usi_engine = UsiEngine_1_0()

        usi_engine.usi_loop()


    except Exception as err:
        print(f"[unexpected error] {err=}, {type(err)=}")
        raise
