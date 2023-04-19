import time

import asyncio
import nextcord
import datetime
import json
import requests
import random


from nextcord import *
from nextcord.ui import Button, View
from nextcord.ext import commands, application_checks
from translate import Translator


import secret

# consts
guild_lannisters = 1097370199897939970
servertime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)

names = ["Яриком", "Милой", "Толей", "Валдисом", "Сергеем"]

random_name = random.choice(names)

# Activity
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=f"за {random_name}")

bot = commands.Bot(intents=nextcord.Intents.all(), activity=activity)

# Добро пожаловать
@bot.event
async def on_member_join(member: Member):
    welcomeChannel = bot.get_channel(1097370868897816626)
    embed = Embed(title="Добро пожаловать!", description=f"**Рады приветствовать тебя, {member.mention}!\nНадеюсь, тебе понравится здесь.**")
    embed.set_image("https://cdn-longterm.mee6.xyz/plugins/commands/images/762281010648842261/08734025084d41c21139210c8256695bfe62f6647349672c3bc194814f0cecda.gif")
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

    contractEndedEmbed = Embed(title=f"Контракт {contract_name} выполнен!", description=f"Контракт {contract_name} выполнен.\nПодтвердил действие {interaction.user.name}.")
    contractEndedEmbed.set_footer(text=f"Время выполнения: " + servertime.strftime('%d.%m.%Y %H:%M:%S'))

    await interaction.send(embed=contractStartEmbed, ephemeral=False, view=view)


    async def on_button_click(interaction: Interaction):
        # Удаляем кнопку из представления
        view.clear_items()
        # Обновляем сообщение с новым представлением без кнопки
        await interaction.message.edit(embed=contractEndedEmbed, view=view)

        if contract_name == "Большой улов (рыбка)":
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>", embed=contractTimeoutEmbed)

        elif contract_name == "Грандиозная уборка (мусор)":
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>", embed=contractTimeoutEmbed)

        elif contract_name == "Мясной день (мясо)":
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>", embed=contractTimeoutEmbed)
        elif contract_name == "Долгожданная встреча (схемы)":
            contractTimeoutEmbed = Embed(
                title=f"Контракт откатился!",
                description=f"{contract_name} взятый ранее {interaction.user.name} откатился!",
                colour=nextcord.Colour.dark_blue()
            )

            couldown = ((servertime + datetime.timedelta(seconds=5)) - servertime).total_seconds()
            await asyncio.sleep(couldown)
            await bot.get_channel(interaction.channel_id).send(content="<@&1097373637381726368>", embed=contractTimeoutEmbed)
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
    time.sleep(2)
    await bot.get_channel(interaction.channel_id).purge(limit=1)



bot.run(secret.key)