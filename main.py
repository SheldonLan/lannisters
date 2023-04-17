import asyncio
import time

import nextcord
from nextcord import *
from nextcord.ext import commands, application_checks
import datetime

import secret

guild_lannisters = 1097370199897939970
servertime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
bot = commands.Bot()


# правила
@bot.slash_command(guild_ids=[guild_lannisters], description="[1-level] Правила")
@application_checks.has_any_role('1-level')
async def rules(interaction: Interaction):
    await interaction.send("**Привет всем!** 😱\nЯ Ваш персональный помощник по всем вопросам.\n\n"
                           "Первое с чем **нужно** ознакомиться - это правила. Уверяю, их немного.\n"
                           "```1. Всё что происходит в этом дискорде - остаётся в этом дискорде\n"
                           "2. Взаимовежливость - основа адекватного коммьюнити.\n"
                           "3. В почти каждом канале есть закреп, пожалуйста, ознакомьтесь, прежде чем что-то писать.\n"
                           "4. Проводите время совместно и приятно :)```\n"
                           "Касаемо бота обращаться к <@265087722853498880> / <@504694073525796884>\n"
                           "Перед любой slash-командой есть значок \"[level]\", который показывает уровень доступа к команде."
                           "Без этой роли. у Вас не получится отправить команду (она не будет обработана).")


# Контракт
@bot.slash_command(guild_ids=[guild_lannisters], description="[Контракты] Взятие контракта")
@application_checks.has_any_role('Контракты')
async def контракт(
        interaction: Interaction,
        contract_name: str = SlashOption(description="Какой контракт Вы взяли?", required=True)):

    contractStartEmbed = Embed(
        title=f"Может брать контракт {contract_name}!",
        description=f"<@{interaction.user.id}> взял контракт {contract_name}.\n"
                    f"Время на выполнение: ",
        colour=nextcord.Colour.dark_gold())

    contractStartEmbed.set_footer(text=f"Время взятия: {servertime.strftime('%d.%m.%Y %H:%M:%S')}\n"
                                       f"Контракт откатится: {(servertime + datetime.timedelta(hours=26)).strftime('%d.%m.%Y %H:%M:%S')}")

    await interaction.send(embed=contractStartEmbed, ephemeral=False)

    contractTimeoutEmbed = Embed(
        title=f"Контракт откатился!",
        description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
        colour=nextcord.Colour.dark_blue()
    )
    couldown = ((servertime + datetime.timedelta(hours=26)) - servertime).total_seconds()
    await asyncio.sleep(couldown)
    await interaction.send(embed=contractTimeoutEmbed, ephemeral=False)










bot.run(secret.key)