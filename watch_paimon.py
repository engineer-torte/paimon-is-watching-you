import os
import discord
from discord.ext import commands, tasks
from datetime import datetime

# 環境変数から監視パイモンのトークンを取得
TOKEN = os.getenv('DISCORD_WATCH_PAIMON_TOKEN')
VOICE_CHANNEL_ID = int(os.getenv('TORTE_VOICE_CHANNEL_ID'))

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

    # await check_voice() # 動作テスト


# 毎分実行（条件式で毎時0分, 30分で実行）
@tasks.loop(minutes=1)
async def check_voice():
    now = datetime.now().time()
    if now.minute != 0 and now.minute != 30:
        return # 0分および30分以外の場合は終了

    # print("Task started - Checking voice channel")  # デバッグ用出力
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    # print(f"Retrieved channel: {channel}")  # デバッグ用出力

    # 通話チャンネルかどうか判定
    if isinstance(channel, discord.VoiceChannel):
        # print("Channel is a VoiceChannel")  # デバッグ用出力
        if len(channel.members) > 0:
            # print(f"Members in channel: {len(channel.members)}, Current time: {now}")  # デバッグ用出力
            
            # 午前2時以降かつ午前12時までだったらパイモンは夜更かしだと認識する。
            if now.hour >= 2 and 12 > now.hour:
                # パイモンは怒った！
                await channel.send(f'<#{VOICE_CHANNEL_ID}> <:Paimon_NoProblem:1310934408387104788>「オイラ寝るまで見てるぞ。夜更かししないで早く寝るんだぞ！」')
            
                # print("Message sent: Past 2 AM with members")  # デバッグ用出力
            else:
                # await channel.send(f'<#{VOICE_CHANNEL_ID}> <:Paimon_NoProblem:1310934408387104788> 「これはチャンネルのお試しメンションだぞー」')
                # print("Before 2 AM, no message sent")  # デバッグ用出力
                pass # 午前2時より前ならパイモンは怒らない。
        else:
            # await channel.send(f'<#{VOICE_CHANNEL_ID}> <:Paimon_NoProblem:1310934408387104788> 「チャンネルのメンションは誰もいないと通知されないぞ…」')
            # print("Message sent: Channel is empty")  # デバッグ用出力
            pass # 誰も居なければパイモンは仕事をしなくていい。
    else:
        # print("Specified channel is not a VoiceChannel")  # デバッグ用出力
        pass # 通話チャンネル以外はパイモンの仕事がない。


# 停止コマンドの追加
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('オイラ、休むぞー')
    await bot.close()


# ボットの起動
bot.run(TOKEN)
