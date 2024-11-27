import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv

# 環境変数をカレントディレクトリの.envから読み込む
load_dotenv()
# 環境変数から監視パイモンのトークンを取得
TOKEN = os.getenv('DISCORD_WATCH_PAIMON_TOKEN')
# 監視対象のチャンネルID
VOICE_CHANNEL_ID = int(os.getenv('PAIMON_WATCHES_CHANNEL_ID'))
# 監視タイミング（分）
MONITOR_TIMING = os.getenv('PAIMON_MONITOR_TIMING').split(',')
# 監視開始時間
START_HOUR = int(os.getenv('PAIMON_WATCH_START_HOUR'))
# 監視終了時間
END_HOUR = int(os.getenv('PAIMON_WATCH_END_HOUR'))
# 怒るときの絵文字
EMOJI_NAME_ID = os.getenv('PAIMON_EMOJI_NAME_ID')
# お怒りの言葉
ANGRY_WORDS = os.getenv('PAIMON_ANGRY_WORDS')


# インテントの設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージコンテンツインテントを有効化
intents.presences = True        # プレゼンスインテントを有効化
intents.members = True          # サーバーメンバーインテントを有効化
intents.voice_states = True     # ボイスステートインテントを有効化

# ボットのクライアントを設定
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    # パイモンが監視を始める
    check_voice.start()

# 毎分実行（条件式で毎時0分, 30分で実行）
@tasks.loop(minutes=1)
async def check_voice(is_test=False):
    now = datetime.now().time()
    if (False == is_test) and (str(now.minute) not in MONITOR_TIMING):
        return # 監視対象の分数以外の場合は終了

    # print("Task started - Checking voice channel")  # デバッグ用出力
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    # print(f"Retrieved channel: {channel}")  # デバッグ用出力

    # 通話チャンネルかどうか判定
    if isinstance(channel, discord.VoiceChannel):
        # print("Channel is a VoiceChannel")  # デバッグ用出力
        if len(channel.members) > 0:
            # print(f"Members in channel: {len(channel.members)}, Current time: {now}")  # デバッグ用出力
            
            # 監視時間内だったらパイモンは夜更かしだと認識する。
            if now.hour >= START_HOUR and END_HOUR > now.hour:
                # パイモンは怒った！
                await channel.send(f'<#{VOICE_CHANNEL_ID}> <{EMOJI_NAME_ID}>「{ANGRY_WORDS}」')
            
                # print("Paimon became angry.")  # デバッグ用出力
            else:
                if is_test:
                    await channel.send(f'<#{VOICE_CHANNEL_ID}> <{EMOJI_NAME_ID}> 「これはテストだぞ！今は怒らないぞ。」')
                # print("Paimon left in peace.")  # デバッグ用出力
                pass # 午前2時より前ならパイモンは怒らない。
        else:
            if is_test:
                await channel.send(f'<#{VOICE_CHANNEL_ID}> <{EMOJI_NAME_ID}> 「これはテストだぞ！誰もいないみたいだ。」')
            # print("Paimon did not meet anyone.")  # デバッグ用出力
            pass # 誰も居なければパイモンは仕事をしなくていい。
    else:
        # print("Paimon can only go to the voice channel.")  # デバッグ用出力
        pass # 通話チャンネル以外はパイモンの仕事がない。

# テスト実行コマンド
@bot.command()
async def test_check(ctx):
    await check_voice(is_test=True)

# 停止コマンド
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('オイラ、休むぞー')
    await bot.close()

# ボットの起動
bot.run(TOKEN)
