import re, os, asyncio, random, string, keep_alive
from random import choice
from discord.ext import commands, tasks

version = 'v2.7.4'

user_token = os.environ['user_token']
spam_id = os.environ['spam_id']
catch_id = os.environ['catch_id']

with open('data/pokemon', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/legendary', 'r') as file:
    legendary_list = file.read()
with open('data/mythical', 'r') as file:
    mythical_list = file.read()
with open('data/level', 'r') as file:
    to_level = file.readline()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

poketwo = 716390085896962058
bot = commands.Bot(command_prefix="->", self_bot=True)
intervals = [2.0, 2.1, 2.2, 2.3, 2.4]


def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^' + hint_replaced + '$', pokemon_list,
                          re.MULTILINE)
    return solution


@tasks.loop(seconds=3)
async def spam():
    channel = bot.get_channel(int(spam_id))
    await channel.send(' '.join(
        random.sample(string.ascii_letters + string.digits, 50) * 1))


@spam.before_loop
async def before_spam():
    await bot.wait_until_ready()


spam.start()


@bot.event
async def on_ready():
    print(f'Logged into account: {bot.user.name}')


@bot.event
async def on_message(message):
    channel = bot.get_channel(int(catch_id))
    if message.channel.id == int(catch_id):
        if message.author.id == poketwo:
            if message.embeds:
                embed_title = message.embeds[0].title
                if 'wild pokémon has appeared!' in embed_title:
                    spam.cancel()
                    await asyncio.sleep(3)
                    await channel.send('<@716390085896962058> h')
                elif "Congratulations" in embed_title:
                    embed_content = message.embeds[0].description
                    if 'now level' in embed_content:
                        split = embed_content.split(' ')
                        a = embed_content.count(' ')
                        level = int(split[a].replace('!', ''))
                        if level == 100:
                            await channel.send(
                                f"<@716390085896962058> s {to_level}")
                            with open('data/level', 'r') as fi:
                                data = fi.read().splitlines(True)
                            with open('data/level', 'w') as fo:
                                fo.writelines(data[1:])
            else:
                content = message.content
                if 'The pokémon is ' in content:
                    if not len(solve(content)):
                        print('Pokemon not found.')
                    else:
                        for i in solve(content):
                            j = (''.join(
                                choice((str.upper, str.lower))(c) for c in i))
                            await asyncio.sleep(3)
                            await channel.send(f'<@716390085896962058> c {j}')
                    check = random.randint(1, 60)
                    if check == 1:
                        await asyncio.sleep(900)
                        spam.start()
                    else:
                        await asyncio.sleep(3)
                        spam.start()

                elif 'Congratulations' in content:
                    global shiny
                    global legendary
                    global num_pokemon
                    global mythical
                    num_pokemon += 1
                    split = content.split(' ')
                    pokemon = split[7].replace('!', '')
                    if 'seem unusual...' in content:
                        shiny += 1
                        print(f'Shiny Pokémon caught! Pokémon: {pokemon}')
                        print(
                            f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}'
                        )
                    elif re.findall('^' + pokemon + '$', legendary_list,
                                    re.MULTILINE):
                        legendary += 1
                        print(f'Legendary Pokémon caught! Pokémon: {pokemon}')
                        print(
                            f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}'
                        )
                    elif re.findall('^' + pokemon + '$', mythical_list,
                                    re.MULTILINE):
                        mythical += 1
                        print(f'Mythical Pokémon caught! Pokémon: {pokemon}')
                        print(
                            f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}'
                        )
                    else:
                        print(f'Total Pokémon Caught: {num_pokemon}')
                elif 'human' in content:
                    spam.cancel()
                    print(
                        'Captcha detected; autocatcher paused. Press enter to restart, after solving captcha manually.'
                    )
                    input()
                    await channel.send('<@716390085896962058> h')
    if not message.author.bot:
        await bot.process_commands(message)


print(
    f'Pokétwo Autocatcher {version}\nA second gen free and open-source Pokétwo autocatcher by Beefcake\nEvent Log:'
)
keep_alive.keep_alive()
bot.run(f"{user_token}")
