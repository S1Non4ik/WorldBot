import disnake
import os
from cfg.cfg import *
from disnake.ext import commands
from disnake.ext.commands import Bot

activity = disnake.Streaming(name="With 💙 by S1Non_",url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

intents = disnake.Intents.all()
bot = Bot(command_prefix ='/', intents=intents, activity=activity, status=disnake.Status.do_not_disturb)
bot.remove_command("help")

@bot.event
async def on_ready():
    channel = bot.get_channel(Logs_channel)
    emb = disnake.Embed(title='📚 Start', description='💻 Server Answer: ```root@admin:~# Bot is running| ✅```')
    await channel.send(embed=emb)

    async def load_cogg(name):
        bot.load_extension(f"modules.{name}")

    async def reload_cogg(name):
        bot.unload_extension(f"modules.{name}")
        bot.load_extension(f"modules.{name}")

    print('------')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            try:
                await load_cogg(filename[:-3])
            except Exception as ex:
                print(f"{filename[:-3]} crashed. I'm automaticly fixing it")
                await reload_cogg(filename[:-3])


@bot.slash_command(guild_ids=[guild])
@commands.has_permissions(administrator=True)
async def restart(inter, name: str):
    bot.unload_extension(f"modules.{name}")
    bot.load_extension(f"modules.{name}")
    await inter.response.send_message("All ready!")






bot.run(token)