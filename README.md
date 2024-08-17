# kifuwarabe-using-cshogi-trainer

きふわらべの成長を助ける弱いトレーナー
## Visual Studio Code で Python スクリプトを動かす方法

Python を公式からインストールすると環境設定が難しすぎる（不完全な初期状態で設定される）ので、  
Anaconda をインストールして、  
VS Code から適当に `*.py` ファイルを選択し、VSCodeのウィンドウの右下あたりから Python インタープリターを選択できるので、  
Anaconda の中に入っている Python インタープリターを選択した方が、断然早い  

📖 [https://www.anaconda.com/](https://www.anaconda.com/)  

例えば以下のフォルダーにインストールされる  

📁 `C:\Users\ユーザー名\anaconda3`  

```shell
# pip のバージョン確認。 19.0 以上が必要
pip -V

# cshogi をインストール
pip install cshogi

# 実行
python main.py
```

### トラブルシューティング

```shell
Traceback (most recent call last):
  File "C:\Users\muzud\OneDrive\ドキュメント\GitHub\kifuwarabe-using-cshogi-trainer\main.py", line 1, in <module>
    import cshogi
  File "C:\Users\muzud\AppData\Local\Programs\Python\Python312\Lib\site-packages\cshogi\__init__.py", line 1, in <module>
    from ._cshogi import *
ImportError: DLL load failed while importing _cshogi: 指定されたモジュールが見つかりません。
```

👆　cshogi をインストールしたにも関わらず上記のエラーが出る場合は、パソコンに Python のインタープリターが複数インストールされていて、別のインタープリターを見ている可能性があります。Python のインタープリターの設定を見直してください。  
VSCode であれば、 `*.py` ファイルを開き、画面の右下の Python のバージョンをクリックしてください  

## 将棋所にエンジン登録する方法

例えば、 📄 `main.bat` に以下のように書く。これをエンジン登録する

```shell
set PATH=%%PATH%%;C:\Users\muzud\anaconda3

python main.py
```
