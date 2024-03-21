# CODE BY DOUXX.XYZ
# https://douxx.xyz/contact


import discord
from discord.ext import commands, tasks

TOKEN = "YOUR BOT TOKEN"

statuses = [
    discord.Streaming(name='/suggest', url='https://twitch.tv/AstroTools'),
    discord.Streaming(name="Support bot", url='https://twitch.tv/astrobot_douxx')
]


@tasks.loop(seconds=8) 
async def change_status():
    global statuses
    await bot.change_presence(activity=statuses[0])
    statuses.append(statuses.pop(0))

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="suppcmd", intents=intents, case_insensitive=True)

    async def on_ready(self):
        print("""
███╗   ███╗ █████╗ ██╗██╗     ██████╗  ██████╗ ████████╗
████╗ ████║██╔══██╗██║██║     ██╔══██╗██╔═══██╗╚══██╔══╝
██╔████╔██║███████║██║██║     ██████╔╝██║   ██║   ██║   
██║╚██╔╝██║██╔══██║██║██║     ██╔══██╗██║   ██║   ██║   
██║ ╚═╝ ██║██║  ██║██║███████╗██████╔╝╚██████╔╝   ██║   
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═════╝  ╚═════╝    ╚═╝   support
              """)
        print("BY douxx.xyz")
        print(f"[READY] Logged in as {self.user}") #The ready is for pterodactyl
        change_status.start()
        print(f"[INFO] add me: https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=30781964549367&scope=bot")
        await self.tree.sync()

intents = discord.Intents.all()
bot = Bot(intents=intents)

pub_chan = YOUR AD CHANNEL ID HERE 
sug_chan =  YOUR SUGGESTIONS CHANNEL ID HERE


@bot.hybrid_command(name='suggest', description='Make a suggestion')
async def suggestion_command(interaction: discord.Interaction, suggestion: str):
    channel = await bot.fetch_channel(sug_chan)

    embed = discord.Embed(
        title='New Suggestion',
        description=f"`{suggestion}`",
        color=discord.Color.dark_blue()
    )

    embed.set_footer(text='\N{LARGE GREEN CIRCLE} Accept | \N{LARGE ORANGE CIRCLE} Pending | \N{LARGE RED CIRCLE} Reject')
    embed.set_author(name=interaction.author.display_name, icon_url=interaction.author.avatar.url if interaction.author.avatar else bot.user.avatar.url)

    msg = await channel.send(embed=embed)
    await msg.add_reaction('\N{LARGE GREEN CIRCLE}') 
    await msg.add_reaction('\N{LARGE ORANGE CIRCLE}')  
    await msg.add_reaction('\N{LARGE RED CIRCLE}')
    embed = discord.Embed(
        description=":white_check_mark: Suggestion sended !",
        color=discord.Color.dark_blue()
    )
    await interaction.reply(embed=embed, ephemeral=True)

async def pub_reply(message):
    if message.channel.id == pub_chan and message.author != bot.user:
        embed = discord.Embed(
            description="""**💡 You too, share your ad by [voting on Top.gg](https://top.gg/bot/1217516172719947847) !**""",
            color=discord.Color.dark_blue()
        )
        embed.add_field(name="Options", value="[`Rules`](https://discord.com/channels/1217557763971088556/1218242133904064582/1218245740682416229) | [`Report this ad`](https://discord.com/channels/1217557763971088556/1217562457934135416/1217581582408220743)")
        await message.reply(embed=embed, mention_author=False)

        embed_priv = discord.Embed(
            title="⚠️ Reminder",
            description=f"All ads posted in the {message.jump_url} channel must comply with **[these rules](https://discord.com/channels/1217557763971088556/1218242133904064582/1218245740682416229)** or they will be deleted.",
            color=discord.Color.dark_blue()
        )
        await message.author.send(embed=embed_priv)

    await bot.process_commands(message)

    

@bot.event
async def on_message(message):
    await pub_reply(message)

bot.run(TOKEN)
