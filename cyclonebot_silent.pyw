import discord
import asyncio
import logging
import random

loggerC = logging.getLogger('program')
loggerD = logging.getLogger('discord')
loggerC.setLevel(logging.DEBUG)
loggerD.setLevel(logging.INFO)
handler = logging.FileHandler(filename='cyclonebot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s] %(levelname)s - %(name)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p'))
loggerC.addHandler(handler)
loggerD.addHandler(handler)

loggerL = logging.getLogger('lore')
loggerL.setLevel(logging.DEBUG)
handlerL = logging.FileHandler(filename='channel_lore.log', encoding='utf-8', mode='a')
handlerL.setFormatter(logging.Formatter(fmt='[%(asctime)s] %(message)s', datefmt='%d/%m/%Y %H:%M'))
loggerL.addHandler(handlerL)

client = discord.Client()
global chansdict, title
chansdict = {}
title = 'with fire'

@client.event
async def on_ready():
    loggerC.info('Logged in as %s, id %s', client.user.name, client.user.id)
    global title
    await client.change_presence(game = discord.Game(name = title))
    loggerC.info('Game status set to %s', str(discord.Game.name))
    for i in client.servers:
        loggerC.info('Online in server: %s', i)
    for i in client.get_all_channels():
        global chansdict
        chansdict[i.name] = i.id
##    await client.send_message(client.get_channel(chansdict['bot']), '```Cyclonebot coming online```')
    print('Cyclonebot online')
    loggerC.info('Cyclonebot online')

@client.event
async def on_message(message):
    global title
    await client.change_presence(game = discord.Game(name = title), status = discord.Status.online)

    global chansdict
    if message.channel.id == chansdict['lore']:
        if message.content != '':
            loggerL.info('[%s] %s: %s', message.id, message.author, message.content)
        if message.attachments != []:
            for f in message.attachments:
                g = f['filename']
                loggerL.info('[%s] %s [sent attachment %s]', message.id, message.author, g)
                                     
    if message.content.startswith('!test'):
        if message.channel.id == chansdict['bot']:
            print(message.type)
            print(message.attachments)
            print(message.clean_content)
        loggerC.debug('test recieved')
        counter = 0
        tmp = await client.send_message(message.channel, '```Calculating messages...```')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, '```You have {} of the last 100 messages.```'.format(counter))
        
    elif message.content.startswith('!sleep'):
        await client.send_message(message.channel, ':zzz:')
        await asyncio.sleep(1)
        await client.change_presence(status = discord.Status.idle)
        # await client.send_message(message.channel, '```Done sleeping```')

    elif message.content.startswith('!8ball'):
        answers = [
        'It is certain',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Reply hazy try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        "Don't count on it",
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful',
        ]
        tmp = await client.send_message(message.channel, ':8ball: `The 8-ball is rolling...` :8ball:')
        thenumbers = random.randrange(0, 15)
        reply = answers[thenumbers]
        await asyncio.sleep(2)
        await client.edit_message(tmp, '```The magic 8-ball replies "{}"```'.format(reply))

    elif message.content.startswith('!play'):
        title = message.content
        title = title.split()
        del title[0]
        title = ' '.join(title)
        await client.change_presence(game = discord.Game(name = title))
        loggerC.info('Game status set to %s', title)

    elif message.content.startswith('!say'):
        speech = message.content
        speech = speech.split()
        del speech[0]
        speech = ' '.join(speech)
        await client.send_message(message.channel, '```{}```'.format(speech), tts=True)

    elif message.content.startswith('!kill'):
        await client.send_message(message.channel, '```Cyclonebot going offline```')
        await client.logout()

@client.event
async def on_message_edit(before, after):
    global chansdict
    if before.channel.id == chansdict['lore']:
        loggerL.info('[%s was edited to] %s', after.id, after.content)

client.run('MjEzNDI2OTEyOTM1MDE4NDk2.Co6VaQ.mewdnzTWknsjkEZuq5iN4y6IGGY')
