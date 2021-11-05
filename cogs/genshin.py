import discord, discord.utils, asyncio, os, json, requests
from discord import errors
from discord.ext import commands
from datetime import datetime
from datetime import date

colours = {"Anemo": discord.Color.from_rgb(166,245,207), "Cryo": discord.Color.from_rgb(189,254,254), "Dendro": discord.Color.from_rgb(176,233,36), "Electro": discord.Color.from_rgb(210,154,254), "Geo": discord.Color.from_rgb(247,214,98), "Hydro": discord.Color.from_rgb(12,228,252), "Pyro": discord.Color.from_rgb(255,167,104)}

def make_ordinal(n: int):
    suffixes = ["th", "st", "nd", "rd"] + (["th"]*6)
    return f"{n}{suffixes[n%10]}"
def month_name(n: int):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return months[n-1]

class Genshin(commands.Cog, name='<:GenshinImpact:905489184205197322> Genshin Impact'):
    """
    Trying out a Genshin API
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True, aliases=['gi', 'g', 'genshinimpact', 'genshin_impact'], description='Get information about Genshin Impact! Use `sc!help genshin` for subcommands.')
    async def genshin(self, ctx):
      await ctx.reply('Genshin Impact is a free-to-play action RPG developed and published by miHoYo. The game features a fantasy open-world environment and action based combat system using elemental magic, character switching, and gacha monetization system for players to obtain new characters, weapons, and other resources. The game can only be played with an internet connection and features a limited multiplayer mode allowing up to four players in a world.\n\nUse `sc!help genshin` for subcommands!', mention_author=False)

    @commands.Cog.listener() # Listener for pagination
    async def on_raw_reaction_add(self, payload):
        # Get the message object they reacted to
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        user = self.bot.get_user(payload.user_id)
        # Check the bot is the author
        if (message.author.id == 773275097221169183) and (payload.user_id != 773275097221169183):
            try:
                # Tries to retrieve the embed
                embed = message.embeds[0]
            except Exception as e:
                # If the embed doesn't exist (i.e. not a message we are interested in)
                pass
            else:
                # If we get an embed in our message
                # If the embed is displaying skills
                if embed.title[-6:] == "Skills":
                    # Check if the reaction is one we are interested in
                    if (payload.emoji.name == "➡️") or (payload.emoji.name == "⬅️"):
                        # Get the page number
                        page_number = int(embed.footer.text[-1])
                        # Check if the reaction is correct for the page number
                        if ((payload.emoji.name == "➡️") and ((page_number == 1) or (page_number == 2))) or ((payload.emoji.name == "⬅️") and ((page_number == 2) or (page_number == 3))):
                            character = embed.footer.text[:-9]
                            response = requests.get(f'https://api.genshin.dev/characters/{character.lower()}/')
                            if payload.emoji.name == "➡️":
                                newpagenumber = page_number + 1
                                newpage = response.json()['skillTalents'][page_number]
                                await message.remove_reaction("➡️", user)
                                if page_number == 1:
                                    await message.remove_reaction("➡️", self.bot)
                                    await message.add_reaction("⬅️")
                                    await message.add_reaction("➡️")
                            else:
                                newpagenumber = page_number - 1
                                newpage = response.json()['skillTalents'][page_number-2]
                                await message.remove_reaction("⬅️", user)
                                if page_number == 3:
                                    await message.add_reaction("➡️")
                                elif page_number == 2:
                                    await message.remove_reaction("⬅️", self.bot)#
                            newEmbed = discord.Embed(title=f"{character}'s Skills", description=f"**{newpage['name']} ({newpage['unlock']})**\n{newpage['description']}", colour=colours[response.json()['vision']])
                            newEmbed.set_footer(text=embed.footer.text[:-1]+str(newpagenumber))
                            newEmbed.set_thumbnail(url=f"https://api.genshin.dev/characters/{character.lower()}/icon-big")
                            try:
                                upgrades = newpage['upgrades']
                            except:
                                pass
                            else:
                                upgradesText = ""
                                for i in upgrades:
                                    upgradesText += f"{i['name']}: {i['value']}\n"
                                newEmbed.add_field(name="Upgrades", value=upgradesText, inline=False)
                                newEmbed.set_thumbnail(url=embed.thumbnail.url)
                            await message.edit(embed=newEmbed)
                
    
    @genshin.command(aliases=['ch', 'char'], description='Get character profiles.')
    async def character(self, ctx, character = None):
        if character is None:
            embed = discord.Embed(title='Character Profiles', description='Learn more about characters in Genshin! For a list of available characters use `sc!genshin characters`.')
        else:
            character = character.lower()
            response = requests.get(f'https://api.genshin.dev/characters/{character}/')
            if response.status_code == 200:
                rarity = ''
                for i in range(response.json()['rarity']):
                    rarity += '⭐'
                embed = discord.Embed(title=f"{character.capitalize()}'s Profile", description=f"{response.json()['description']}\n**Rarity:** {rarity}", colour=colours[response.json()['vision']])
                embed.set_thumbnail(url=f'https://api.genshin.dev/characters/{character}/icon-big')
                embed.add_field(name='Vision', value=response.json()['vision'], inline=True)
                embed.add_field(name='Weapon Type', value=response.json()['weapon'], inline=True)
                embed.add_field(name='Place of Origin', value=response.json()['nation'], inline=True)
                # Create datetime.date() object using birthday
                isoformat = date.fromisoformat('2021-'+response.json()['birthday'][-5:])
                day = make_ordinal(int(response.json()['birthday'][-2:]))
                month = month_name(int(response.json()['birthday'][-5:-3]))
                embed.add_field(name='Birthday', value=f"{day} {month}", inline=True)
                embed.add_field(name='Skills', value=f'Use `sc!genshin skills {character}`', inline=True)
                embed.add_field(name='Affiliation', value=response.json()['affiliation'], inline=True)
                embed.add_field(name='Constellations', value=f"**{response.json()['constellation']}**\nUse `sc!genshin constellation {character}`", inline=True)
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Profiles', description='That person does not exist! Please make sure you typed their name correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                embed = discord.Embed(title='Character Profiles', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the character command.\nArguments: {character}")
        embed.set_author(name='Character Profiles', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)


        
    @genshin.command(aliases=['chars', 'chs'], description="List of valid character names, sorted alphabetically.")
    async def characters(self, ctx):
        embed = discord.Embed(title='Available Characters', description="Albedo\nAloy\nAmber\nAyaka\nBarbara\nBeidou\nBennett\nChongyun\nDiluc\nDiona\nEula\nFischl\nGanyu\nHu-Tao\nJean\nKaeya\nKazuha\nKeqing\nKlee\nKokomi\nLisa\nMona\nNingguang\nNoelle\nQiqi\nRaiden\nRazor\nRosaria\nSara\nSayu\nSucrose\nTartaglia\nTraveler-Anemo\nTraveler-Electro\nTraveler-Geo\nVenti\nXiangling\nXiao\nXingqiu\nXinyan\nYanfei\nYoimiya\nZhongli", colour=discord.Color.from_rgb(241,210,231))
        await ctx.reply(embed=embed, mention_author=False)
    @genshin.command(aliases=['s', 'skill', 't', 'talents'], description="Look at a character's skills.")
    async def skills(self, ctx, character: str = None):
        if character is None:
            embed = discord.Embed(title='Character Skills', description="Learn about a Genshin characters' skills! For a list of available characters use `sc!genshin characters`.", colour=discord.Color.from_rgb(241,210,231))
        else:
            character = character.lower()
            response = requests.get(f'https://api.genshin.dev/characters/{character}/')
            if response.status_code == 200:
                skills = response.json()['skillTalents']
                embed = discord.Embed(title=f"{character.capitalize()}'s Skills", description=f"**{skills[0]['name']} ({skills[0]['unlock']})**\n{skills[0]['description']}", colour=colours[response.json()['vision']])
                try:
                    upgrades = skills[0]['upgrades']
                except:
                    upgradesText = None
                else:
                    upgradesText = ""
                    for i in upgrades:
                        upgradesText += f"{i['name']}: {i['value']}\n"
                if upgradesText is not None:
                    embed.add_field(name="Upgrades", value=upgradesText, inline=False)
                embed.set_footer(text=f"{character.capitalize()} | Page 1")
                embed.set_thumbnail(url=f"https://api.genshin.dev/characters/{character}/icon-big")
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Profiles', description='That person does not exist! Please make sure you typed their name correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_image(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                embed = discord.Embed(title='Character Profiles', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the character command.\nArguments: {character}")
        embed.set_author(name='Character Skills', icon_url=ctx.author.avatar_url)
        skillsEmbed = await ctx.reply(embed=embed, mention_author=False)
        if response.status_code == 200:
            await skillsEmbed.add_reaction("➡️")

    @genshin.command(aliases=['co'], description="Look at a character's constellation.")
    async def constellation(self, ctx, * character: str):
        await ctx.reply('Hi!')
    
            
def setup(bot):
    bot.add_cog(Genshin(bot))
