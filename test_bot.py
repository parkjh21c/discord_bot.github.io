import discord
from discord.ext import commands
import time
import asyncio
import random

# 규칙
# 1. 주석은 최대한 자세하게 달 것.
# 2. 각 변수 이름은 함수마다 같게 처리할 것.





# txt파일에서 봇 토큰 가져오기
with open("test_key.txt", "r") as f:
    key = f.read()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='%',intents=intents)

# 봇 가동을 위한 전역변수
member_entry = []

sec_10 = 10


#봇 가동
@bot.event
async def on_ready():
    print('로그인 중')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')
    game = discord.Game("온라인")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot == 1: # 봇이면 패스
        return None
    

    # 사다리타기
    if reaction.emoji == "⭕":
        # remove로 삭제할지 del로 삭제할지 판단
        member_entry.append(user.mention)
        


@bot.command()
async def 주사위(ctx, *, num):
    dice = random.randint(0, int(num))
    await ctx.send(ctx.author.mention + f" : {dice}")


@bot.command()
async def 사다리(ctx):
    # 중복 작동 체크
    if len(member_entry) != 0:
        await ctx.send("이미 작동중입니다!")
    else:
        member_entry.append("0")
        # 리스트 형성(초기화)
        a_team = []
        b_team = []

        # 사다리 탈 인원 받기
        button_msg = await ctx.send("아래 버튼을 눌러주세요!")
        await button_msg.add_reaction("⭕")
        time_msg = await ctx.send("카운트 다운")
        
        for k in range(0, sec_10 + 1):
            time_sec = sec_10 - k
            time.sleep(1)
            await time_msg.edit(content=f"{time_sec}초")
        await time_msg.edit(content="집계 완료")
        # 중복 확인용 요소 삭제
        member_entry.remove("0")

        total_member = len(member_entry)

        if total_member > 1:
            # a팀 뽑기
            for _ in range(total_member // 2):
                a_member = random.choice(member_entry)
                member_entry.remove(a_member)
                a_team.append(a_member)
            # b팀 뽑기
            for i in member_entry:
                member_entry.remove(i)
                b_team.append(i)

            # 결과
            a_text = ""
            for j in a_team:
                a_text = a_text + j + ", "
            await ctx.send("A팀 : " + a_text)

            b_text = ""
            for j in b_team:
                b_text = b_text + j + ", "
            await ctx.send("B팀 : " + b_text)
            
        else:
            await ctx.send("인원수가 부족합니다.")
        




        
        

bot.run(key)