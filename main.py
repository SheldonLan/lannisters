import asyncio
import datetime
import json
import os
import random
import time

import nextcord
import requests
from nextcord import *
from nextcord.ext import commands, application_checks
from nextcord.ui import Button, View
from translate import Translator
from pytube import YouTube

import secret

# consts
guild_lannisters = 1097370199897939970
servertime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)

names = ["Яриком", "Милой", "Толей", "Валдисом", "Сергеем", "Данилом"]

random_name = random.choice(names)

# Activity
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=f"за {random_name}")

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


choices = {"Большой улов": "Большой улов (рыбка)",
           "Грандиозная уборка": "Грандиозная уборка (мусор)",
           "Мясной день": "Мясной день (мясо)",
           "Долгожданная встреча": "Долгожданная встреча (схемы)",
           "Ломать - не строить": "Ломать - не строить",
           }


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
    if (jokeJson["type"] == 'single'):
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
    await ctx.send("<a:srt_discordloading:1098494332991963157> Подождите пару секунд, я загружаю песню. <a:srt_discordloading:1098494332991963157>")
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.download(output_path='D:/tmp')
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    source = await nextcord.FFmpegOpusAudio.from_probe(f'{filename}')
    voice_client.play(source)
    voicePlayEmbed = Embed(description=f"Cейчас играет: {str(filename).split('D:/tmp')[1].split('.mp')[0]}")
    voicePlayEmbed.set_footer(text=f"Приятного прослушивания, {ctx.author}")
    await ctx.send(embed=voicePlayEmbed)
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()
    dir_path = "D:/tmp"
    await asyncio.sleep(5)
    files = os.listdir(dir_path)

    for file in files:
        if file.endswith(".mp4"):
            file_path = os.path.join(dir_path, file)
            try:
                os.remove(file_path)
                print(f"Файл {file_path} успешно удален")
            except OSError as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")
    await voice_client.disconnect()

@bot.command()
async def pause(ctx):
    vc = ctx.voice_client
    if vc.is_playing():
        vc.pause()
    else:
        await ctx.send("Я ничего сейчас не играю.")

@bot.command()
async def resume(ctx):
    vc = ctx.voice_client
    if vc.is_paused():
        vc.resume()
    else:
        await ctx.send("Я не на паузе.")

@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    if vc.is_playing():
        vc.stop()
        dir_path = "D:/tmp"
        await asyncio.sleep(5)
        files = os.listdir(dir_path)

        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(dir_path, file)
                try:
                    os.remove(file_path)
                    print(f"Файл {file_path} успешно удален")
                except OSError as e:
                    print(f"Ошибка при удалении файла {file_path}: {e}")
        await voice_client.disconnect()
    else:
        await ctx.send("Я ничего не играю")

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        dir_path = "D:/tmp"
        await asyncio.sleep(5)
        files = os.listdir(dir_path)

        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(dir_path, file)
                try:
                    os.remove(file_path)
                    print(f"Файл {file_path} успешно удален")
                except OSError as e:
                    print(f"Ошибка при удалении файла {file_path}: {e}")
        await voice_client.disconnect()
    else:
        await ctx.send("Я не нахожусь в голосовом канале!")


bot.run(secret.key)
