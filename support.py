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
        print(f"Logged in as {self.user}")
        change_status.start()
        print(f"add me: https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=30781964549367&scope=bot")
        await self.tree.sync()

intents = discord.Intents.all()
bot = Bot(intents=intents)

pub_chan = 1217562443006611587 
sug_chan =  1217562446244614174
topgg_link = "Your top.gg link"
ad_rules_message = "the link to your rules"
ticket = "link to your tickets"


@bot.hybrid_command(name='suggest', description='Make a suggestion')
async def suggestion_command(interaction: discord.Interaction, suggestion: str):
    channel = await bot.fetch_channel(sug_chan)

    embed = discord.Embed(
        title='New Suggestion',
        description=f"`{suggestion}`",
        color=discord.Color.dark_blue()
    )

    embed.set_footer(text='\N{LARGE GREEN CIRCLE} Yes | \N{LARGE ORANGE CIRCLE} I don\'t know | \N{LARGE RED CIRCLE} No')
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
            description=f"""**💡 You too, share your ad by [voting on Top.gg]({topgg_link}) !**""",
            color=discord.Color.dark_blue()
        )
        embed.add_field(name="Options", value=f"[`Rules`]({ad_rules_message}) | [`Report this ad`]({ticket})")
        await message.reply(embed=embed, mention_author=False)

        embed_priv = discord.Embed(
            title="⚠️ Reminder",
            description=f"All ads posted in the {message.jump_url} channel must comply with **[these rules]({ad_rules_message})** or they will be deleted.",
            color=discord.Color.dark_blue()
        )
        await message.author.send(embed=embed_priv)

    await bot.process_commands(message)

    

@bot.event
async def on_message(message):
    await pub_reply(message)

bot.run(TOKEN)


#CODE BY DOUXX.XYZ
#CONTACT ME: https://douxx.xyz/contact
