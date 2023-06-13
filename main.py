import asyncio
import datetime
import json
import subprocess
import sys
import time
from functools import partial

import urllib.request
import os
import nextcord
import requests
from bs4 import BeautifulSoup
from nextcord import *
from nextcord.ext import commands, application_checks, tasks
from nextcord.ui import Button, View
from pytube import YouTube, Search
from translate import Translator
from itertools import cycle

import choice
import secret

# consts
guild_lannisters = 1097370199897939970  # id дискорд сервера
servertime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # получение мск времени

# Activity
names = cycle(["за Яриком", "за Милой", "за Толей", "за Валдисом", "за Сергеем", "за Данилом", "за Иваном", "за Настей", "за Алисой", "за Олегом", "за Наташей", "за Антоном", "за Львом", "за Денисом"])


# Bot definition
bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix="!")

@tasks.loop(seconds=5)
async def change_activity():
    await bot.change_presence(activity=Activity(type=nextcord.ActivityType.watching, name=next(names)))

@bot.event
async def on_ready():
    change_activity.start()
    print('bot started')

# Добро пожаловать
@bot.event
async def on_member_join(member: Member):
    welcomeChannel = bot.get_channel(1097370868897816626)
    embed = Embed(title="Добро пожаловать!",
                  description=f"**Рады приветствовать тебя, {member.mention}!\nНадеюсь, тебе понравится здесь.**")
    embed.set_image(
        "https://cdn-longterm.mee6.xyz/plugins/commands/images/762281010648842261/08734025084d41c21139210c8256695bfe62f6647349672c3bc194814f0cecda.gif")
    embed.set_footer(text="Lannister's FAMQ")
    role = nextcord.utils.get(member.guild.roles, name="Гость")
    await member.add_roles(role)
    await welcomeChannel.send(embed=embed)


# Правила
@bot.slash_command(guild_ids=[guild_lannisters], description="[1-level] Правила")
async def правила(interaction: Interaction):
    channelRules = bot.get_channel(1097373322947342366)
    await channelRules.send("**Привет всем!** 😱\nЯ Ваш персональный помощник по всем вопросам.\n\n"
                            "Первое с чем **нужно** ознакомиться - это правила. Уверяю, их немного.\n"
                            "```1. Всё что происходит в этом дискорде - остаётся в этом дискорде\n"
                            "2. Взаимовежливость - основа адекватного коммьюнити.\n"
                            "3. В почти каждом канале есть закреп, пожалуйста, ознакомьтесь, прежде чем что-то писать.\n"
                            "4. Проводите время совместно и приятно :)```\n"
                            "Касаемо бота обращаться к <@265087722853498880> / <@504694073525796884>\n"
                            "Перед любой slash-командой есть значок \"[role]\", который показывает уровень доступа к команде."
                            "Без этой роли. у Вас не получится отправить команду (она не будет обработана).")


choices = choice.contract_choices

"""
/контракты НАЗВАНИЕ_КОНТРАКТА

Вывод Embed'ki и кнопки,
после выполнения команды у Вас появится информационное Embed сообщение с названием и временем взятия,
а также кнопка Контракт выполнен,
по нажатию на кнопку, происходит отчёт времени кд контракта,
как только КД будет подходить к концу,
бот тегнет роль @Контракты и оповестит о завершение КД у НАЗВАНИЕ_КОНТРАКТА,
тем самым не придётся постоянно чекать, когда пройдёт КД.
"""


@bot.slash_command(guild_ids=[guild_lannisters], description="[Контракты] Взятие контракта")
async def контракт(
        interaction: Interaction,
        contract_name: str = SlashOption(description="Какой контракт Вы взяли?",
                                         required=True,
                                         choices=choices)):
    # Объявление и добавление кнопки
    accept_button = Button(label="Контракт выполнен!", style=ButtonStyle.green, custom_id="accept_button")
    view = View()
    view.add_item(accept_button)

    contractStartEmbed = Embed(
        title=f"Внимание!",
        description=f"<@{interaction.user.id}> взял контракт {contract_name}.",
        colour=nextcord.Colour.dark_gold())
    contractStartEmbed.set_footer(text=f"Время взятия: {servertime.strftime('%d.%m.%Y %H:%M:%S')}")

    contractEndedEmbed = Embed(title=f"Контракт {contract_name} выполнен!",
                               description=f"Контракт {contract_name} выполнен.\nПодтвердил действие {interaction.user.name}.")
    contractEndedEmbed.set_footer(text=f"Время выполнения: " + servertime.strftime('%d.%m.%Y %H:%M:%S'))

    await interaction.send(content="<@&1111988562678779996>", embed=contractStartEmbed, ephemeral=False, view=view)

    async def on_button_click(interaction: Interaction):
        view.clear_items()
        await interaction.message.edit(embed=contractEndedEmbed, view=view)

        if contract_name == "Большой улов (рыбка)":
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>",
                                                               embed=contractTimeoutEmbed)

        elif contract_name == "Грандиозная уборка (мусор)":
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>",
                                                               embed=contractTimeoutEmbed)

        elif contract_name == "Мясной день (мясо)":
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>",
                                                               embed=contractTimeoutEmbed)
        elif contract_name == "Долгожданная встреча (схемы)":
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>",
                                                               embed=contractTimeoutEmbed)
        else:
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>",
                                                               embed=contractTimeoutEmbed)

    # Привязываем обработчик событий к кнопке
    accept_button.callback = on_button_click


"""
Генерация рандомной шутки через jokeapi
Получение Json, парсинг его, отправка одним/двумя сообщениями в зависимости от типа сообщения.
"""


@bot.slash_command(guild_ids=[guild_lannisters], description="[2-level] Получение рандомной шутки")
async def шутка(interaction: Interaction):
    response = requests.get('https://v2.jokeapi.dev/joke/Any')
    jokeJson = json.loads(response.text)
    translator = Translator(from_lang='en', to_lang='ru')
    if jokeJson["type"] == 'single':
        await bot.get_channel(interaction.channel_id).send(translator.translate(str(jokeJson["joke"])))
    else:
        await bot.get_channel(interaction.channel_id).send(translator.translate(str(jokeJson["setup"])))
        time.sleep(2)
        await bot.get_channel(interaction.channel_id).send(translator.translate(str(jokeJson["delivery"])))


"""
Слеш-команда /Очистить + "int: amount(кол-во)",
Выполняет функцию удаления сообщений канала,
где эта команда была вызвана.
"""


@bot.slash_command(guild_ids=[guild_lannisters], description="[1-level] Удаление предыдущих сообщений")
async def очистить(interaction: Interaction,
                   amount: int = SlashOption(description="Сколько сообщений выше удалить?", required=True)):
    await bot.get_channel(interaction.channel_id).purge(limit=amount)
    await interaction.send(f"Пользователь <@{interaction.user.id}> удалил {amount} сообщений")
    time.sleep(1)
    await bot.get_channel(interaction.channel_id).purge(limit=1)


@bot.command()
async def restart(ctx):
    await ctx.send('Перезапускаюсь...')
    subprocess.run(['bat.bat'])
    os.execl(sys.executable, sys.executable, "C:/Users/RTA-Telecom/Desktop/test files/lannisters/main.py")


"""
ВЗП, отправка Embed сообщения
По клику добавляет участников
По клику убирает участников
Просчитывает кол-во аммуниции
"""


@bot.slash_command(guild_ids=[guild_lannisters], description="Война за предприятие")
async def взп(interaction: Interaction, time: str = SlashOption(description="Во сколько группаемся?",
                                                                required=True)):
    edy_button = Button(label="Я еду!", style=ButtonStyle.green, custom_id="accept_button")
    view = View()
    view.add_item(edy_button)

    vzpEmbed = Embed(title="Поехали на ВЗП?", description="Функция просчётов участников и аммуниции")
    vzpEmbed.set_footer(text=f"Объявил сбор: {interaction.user.name}")
    sborshik = interaction.user.name

    with open('vzp.txt', 'w', encoding='utf-8') as vzptxt:
        vzptxt.write(f"<@{interaction.user.id}>\n")

    await interaction.send(f"{interaction.guild.get_role(1100736955643351070).mention} собираемся в {time}",
                           embed=vzpEmbed, view=view)

    async def on_edy_button_click(interaction: Interaction):
        with open("vzp.txt", 'a', encoding="utf-8") as vpz_txt:
            list_vzp_members = open('vzp.txt', 'r', encoding='utf-8').read().strip().split('\n')
            if "<@" + str(interaction.user.id) + ">" in list_vzp_members:
                list_vzp_members.remove(f'<@{interaction.user.id}>')
                with open("vzp.txt", "w", encoding="utf-8") as f:
                    f.write('\n'.join(list_vzp_members) + "\n")
            else:
                vpz_txt.write(f"<@{interaction.user.id}>\n")
        vzp_members = open('vzp.txt', 'r', encoding='utf-8').read().strip().split("\n")
        counter = 0
        for el in vzp_members:
            counter += 1
        vzp_members_str = '\n'.join(vzp_members)

        bullets = counter * 300
        armor = counter * 2
        gun = counter

        vzp_edyEmbed = Embed(title="Поехали на ВЗП?")
        vzp_edyEmbed.add_field(name="Кто едет:", value=f"{vzp_members_str}")
        vzp_edyEmbed.add_field(name="   ", value="   ")
        vzp_edyEmbed.add_field(name="Расчёты:", value=f"На {counter} человек нужно:\n"
                                                      f"Ганов: {gun}\n"
                                                      f"Патронов: {bullets}\n"
                                                      f"Броников: {armor}")
        vzp_edyEmbed.set_footer(text=f"Объявил сбор: {sborshik}")
        await interaction.message.edit(embed=vzp_edyEmbed, view=view)

    edy_button.callback = on_edy_button_click


bot.run(secret.key)