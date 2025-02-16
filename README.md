# paimon-is-watching-you

Discordサーバーでゲーミング夜更かし勢を監視して寝るようにつつくパイモンのリポジトリです。非公式の非常食です。

PC起動時に実行させるようにしてDiscord Botのタスクとして毎分動作で毎時0分と30分にチェックします。  
深夜2時～午前12時に指定したチャンネルにメンバーがいるとチャンネルメンションして警告します。

※試験的に静的解析ツール（ruff, black）を導入。

- [動作設定手順](#動作設定手順)
- [構築手順](#構築手順)

## 動作設定手順

Pythonをインストールしておいてください。  
構築にはMicrosoft StoreにあるPythonを使用しています。

1. ソースコードの配置（`%USERPROFILE%\workspace\paimon-is-watching-you`）
2. pipパッケージのインストール

    ```shell
    python -m pip install -r "%USERPROFILE%\workspace\paimon-is-watching-you\requirement.txt"
    ```

3. 環境変数の設定（※`.env.example`を`.env`にリネームして以下を設定してください。）
   1. Botのトークン：`DISCORD_WATCH_PAIMON_TOKEN`
   2. チャンネルのID：`PAIMON_WATCHES_CHANNEL_ID`
   3. 監視タイミング：`PAIMON_MONITOR_TIMING`  
   ※これは**カンマ区切りで分数を記述**してください。
   4. 対象時間：`PAIMON_WATCH_START_HOUR`, `PAIMON_WATCH_END_HOUR`
   5. 怒るときの絵文字：`PAIMON_EMOJI_NAME_ID`
   6. お怒りの言葉：`PAIMON_ANGRY_WORDS`
4. タスクスケジューラに実行タスクを追加
   1. **全般**：`最上位特権`、`Windows10`
   2. **トリガー**：`ログオン時`  
        →スタートアップ時だと遅延かけても失敗する可能性があるかも…
      1. **遅延時間を必ず入れてください。** Discordが自動起動するまでは必要みたいです。
   3. **操作**：`プログラムの実行`
      1. **プログラム/スクリプト**

            ```txt
            "%LocalAppData%\Microsoft\WindowsApps\pythonw.exe"
            ```

      2. **引数の追加**：配置したスクリプトを指定する

            ```txt
            "%USERPROFILE%\workspace\paimon-is-watching-you\watch_paimon.py"
            ```

   4. **条件**
      1. `OFF`：コンピューターをAC電源で使用している場合のみタスクを開始する
      2. `ON` ：次のネットワーク接続が使用可能な場合のみタスクを開始する（任意の接続）
   5. **設定**
      1. `ON`
         1. タスクを要求時に実行する
         2. スケジュールされた時刻にタスクを開始できなかった場合、すぐにタスクを実行する
         3. 要求時に実行中のタスクが終了しない場合、タスクを強制的に停止する
         4. タスクが既に実行中の場合に適用される規則（**既存のインスタンスの停止**）
      2. `OFF`
         1. 上記以外
5. システムを再起動 or タスクを手動実行

## 構築手順

1. Discord Botの動作するスクリプトを記述
2. Discord Botを作成（<https://discord.com/developers/applications>）
3. Botメニューの`Privileged Gateway Intents`はすべて有効にするべきかも。
   1. Presence Intent
   2. Server Members Intent
   3. Message Content Intent
4. トークンを取得して環境変数にセット
5. OAuth2でリンクを発行してサーバーに招待する
   1. Scopesは`bot`, `application.commands`を有効
   2. Bot Permissionsは`Send Messages`, `Embed Links`, `Attach Files`を有効
6. ローカルPCにて実行
