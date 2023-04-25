import asyncio
import datetime
import json
import os
import random
import subprocess
import sys
import time

import nextcord
import requests
from bs4 import BeautifulSoup
from nextcord import *
from nextcord.ext import commands, application_checks
from nextcord.ui import Button, View
from pytube import YouTube
from translate import Translator

import choice
import secret

# consts
guild_lannisters = 1097370199897939970  # id дискорд сервера
servertime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # получение мск времени

# Activity
names = ["Яриком", "Милой", "Толей", "Валдисом", "Сергеем", "Данилом", "Иваном"]
random_name = random.choice(names)
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=f"за {random_name}")

# Bot definition
bot = commands.Bot(intents=nextcord.Intents.all(), activity=activity, command_prefix="!")


# Добро пожаловать
@bot.event
async def on_member_join(member: Member):
    welcomeChannel = bot.get_channel(1097370868897816626)
    embed = Embed(title="Добро пожаловать!",
                  description=f"**Рады приветствовать тебя, {member.mention}!\nНадеюсь, тебе понравится здесь.**")
    embed.set_image(
        "https://cdn-longterm.mee6.xyz/plugins/commands/images/762281010648842261/08734025084d41c21139210c8256695bfe62f6647349672c3bc194814f0cecda.gif")
    embed.set_footer(text="Lannister's FAMQ")
    role = nextcord.utils.get(member.guild.roles, name="4-level")
    await member.add_roles(role)
    await welcomeChannel.send(embed=embed)


# Правила
@bot.slash_command(guild_ids=[guild_lannisters], description="[1-level] Правила")
@application_checks.has_any_role('1-level')
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


# Контракт
@bot.slash_command(guild_ids=[guild_lannisters], description="[Контракты] Взятие контракта")
@application_checks.has_any_role('Контракты')
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

    await interaction.send(embed=contractStartEmbed, ephemeral=False, view=view)

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


# шутка
@bot.slash_command(guild_ids=[guild_lannisters], description="[2-level] Получение рандомной шутки")
@application_checks.has_any_role('2-level', '3-level', '1-level', 'DSM')
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


# Purge
@bot.slash_command(guild_ids=[guild_lannisters], description="[1-level] Удаление предыдущих сообщений")
@application_checks.has_any_role('1-level')
async def очистить(interaction: Interaction,
                   amount: int = SlashOption(description="Сколько сообщений выше удалить?", required=True)):
    await bot.get_channel(interaction.channel_id).purge(limit=amount)
    await interaction.send(f"Пользователь <@{interaction.user.id}> удалил {amount} сообщений")
    time.sleep(1)
    await bot.get_channel(interaction.channel_id).purge(limit=1)


# Музыка
@bot.command()
async def play(ctx, url: str):
    re = requests.get(url).text
    soup = BeautifulSoup(re, "html.parser")
    filename = soup.find('title').text.replace(" - YouTube", "")
    if os.path.isfile(f'D:/tmp/{filename}.mp4'):
        await ctx.send("У меня есть эта песня!")
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()
        source = await nextcord.FFmpegOpusAudio.from_probe(f'D:/tmp/{filename}.mp4')
        voice_client.play(source)
        voicePlayEmbed = Embed(description=f"Cейчас играет: {filename}", colour=nextcord.Colour.random())
        voicePlayEmbed.set_footer(text=f"Приятного прослушивания, {ctx.author}")
        await ctx.send(embed=voicePlayEmbed)
        while voice_client.is_playing():
            await asyncio.sleep(2)
        await voice_client.disconnect()
    else:
        try:
            await ctx.send(
                "<a:musica53:1098869634880503908> Подождите пару секунд, я загружаю песню. <a:musica53:1098869634880503908>")
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            filename = stream.download(output_path='D:/tmp')
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()
            source = await nextcord.FFmpegOpusAudio.from_probe(f'{filename}')
            voice_client.play(source)
            voicePlayEmbed = Embed(description=f"Cейчас играет: {filename.replace('D:/tmp', '').replace('.mp4', '')}",
                                   colour=nextcord.Colour.random())
            voicePlayEmbed.set_footer(text=f"Приятного прослушивания, {ctx.author}")
            await ctx.send(embed=voicePlayEmbed)
            while voice_client.is_playing():
                await asyncio.sleep(2)
            await voice_client.disconnect()
        except KeyError:
            try:
                await ctx.send(
                    "<a:srt_discordloading:1098494332991963157> Не получилось загрузить песню, попробую по другому. <a:srt_discordloading:1098494332991963157>")
                yt = YouTube('https://youtu.be/' + url.split('watch?v=')[1].split('&')[0])
                stream = yt.streams.filter(only_audio=True).first()
                filename = stream.download(output_path='D:/tmp')
                voice_channel = ctx.author.voice.channel
                voice_client = await voice_channel.connect()
                source = await nextcord.FFmpegOpusAudio.from_probe(f'{filename}')
                voice_client.play(source)
                voicePlayEmbed = Embed(
                    description=f"Cейчас играет: {filename.replace('D:/tmp', '').replace('.mp4', '')}",
                    colour=nextcord.Colour.random())
                voicePlayEmbed.set_footer(text=f"Приятного прослушивания, {ctx.author}")
                await ctx.send(embed=voicePlayEmbed)
                while voice_client.is_playing():
                    await asyncio.sleep(2)
                await voice_client.disconnect()
            except KeyError:
                await ctx.send(
                    "<a:ghost64:1098869622645735565> Вообще не могу получить доступ :c\nВоспользуйтесь командой !restart, а после повторите попытку. <a:ghost64:1098869622645735565>")


@bot.command()
async def pause(ctx):
    vc = ctx.voice_client
    try:
        if vc.is_playing():
            vc.pause()
    except AttributeError:
        await ctx.send("Я ничего сейчас не играю.")


@bot.command()
async def resume(ctx):
    vc = ctx.voice_client
    try:
        if vc.is_paused():
            vc.resume()
    except AttributeError:
        await ctx.send("Я не на паузе.")


@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    try:
        if vc.is_playing():
            vc.stop()
    except AttributeError:
        await ctx.send("Я ничего не играю")


@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    try:
        if voice_client.is_connected():
            await voice_client.disconnect()
    except AttributeError:
        await ctx.send("Я не нахожусь в голосовом канале!")


@bot.command()
async def restart(ctx):
    await ctx.send('Перезапускаюсь...')
    subprocess.run(['bat.bat'])
    os.execl(sys.executable, sys.executable, "C:/Users/RTA-Telecom/Desktop/test files/lannisters/main.py")


@bot.slash_command(name="to-do")
async def todo(interaction: Interaction):
    await interaction.send("1. Дни рождения участников set/remove/remember\n"
                           "2. ")


# NEW MUSIC PLAYER
@bot.slash_command(guild_ids=[guild_lannisters], description="Добавление песни по URL")
async def add(interaction: Interaction,
              url: str = SlashOption(description="Ссылка на youtube", required=True)):
    # Отправка запроса по URL для получения названия файла
    re = requests.get(url).text
    soup = BeautifulSoup(re, "html.parser")
    filename = soup.find('title').text.replace(" - YouTube", "")
    # Проверка на существование файла
    if os.path.isfile(f'D:/tmp/{filename}.mp4'):
        with open("queue.txt", 'a', encoding="utf-8") as queue:
            queue.write(f"{filename.replace('D:/tmp', '')}\n")
            addEmbed = Embed(description=f"Файл {filename} был добавлен в очередь воспроизведения!",  colour=nextcord.Colour.red())
        await interaction.send(embed=addEmbed, ephemeral=True)
    else:
        await interaction.send("Скачиваю файл.", ephemeral=True)
        try:
        # Скачиваем по url трек
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            filename = stream.download(output_path='D:/tmp')
            with open("queue.txt", 'a', encoding="utf-8") as queue:
                queue.write(f"{filename.replace('D:/tmp', '')[1:].replace('.mp4', '')}\n")
                downloadAddEmbed = Embed(description=f"Файл {filename.replace('D:/tmp', '')[1:].replace('.mp4', '')} был добавлен в очередь воспроизведения!",  colour=nextcord.Colour.red())
            await interaction.edit_original_message(content="", embed=downloadAddEmbed)
        except KeyError:
            await interaction.edit_original_message(content=f"Не удалось загрузить {filename}. Попробуйте !restart и добавить трек снова.")


@bot.slash_command(guild_ids=[guild_lannisters], description="Удаление списка песен")
async def clearqueue(interaction: Interaction):
    with open("queue.txt", 'w', encoding='utf-8') as file:
        file.write('')
    clearEmbed = Embed(description=f"Очередь была очищена {interaction.user.name}",  colour=nextcord.Colour.random())
    await interaction.send(embed=clearEmbed)


@bot.slash_command(guild_ids=[guild_lannisters], description="show queue")
async def showqueue(interaction: Interaction):
    with open('queue.txt', 'r', encoding="utf-8") as queue:
        lines = queue.read().split('\n')
        message = "\n".join(lines)
        queueEmbed = Embed(title="Очередь воспроизведения:", description=f"{message}", colour=nextcord.Colour.random())
        await interaction.send(embed=queueEmbed)

@bot.slash_command(guild_ids=[guild_lannisters], description="black")
async def психолог(interaction: Interaction):
    await interaction.send("Лучше бы повесился")


@bot.slash_command(guild_ids=[guild_lannisters], description="play test")
async def play(interaction: Interaction, channel: VoiceChannel):
    voice_client = await channel.connect()
    with open('queue.txt', 'r', encoding="utf-8") as queue:
        queueList = queue.read().strip().split('\n')
        await interaction.send("Запускаюсь!")
    if len(queueList) == 0:
        await interaction.send("Очередь пуста")
    else:
        for element in queueList:
            source = await nextcord.FFmpegOpusAudio.from_probe(f'D:/tmp/{element}.mp4')
            voice_client.play(source)
            voicePlayEmbed = Embed(description=f"Cейчас играет: {element}", colour=nextcord.Colour.random())
            voicePlayEmbed.set_footer(text=f"Приятного прослушивания, {interaction.user.name}")
            await interaction.edit_original_message(content="", embed=voicePlayEmbed)
            while voice_client.is_playing():
                await asyncio.sleep(1)
        await voice_client.disconnect()

bot.run(secret.key)