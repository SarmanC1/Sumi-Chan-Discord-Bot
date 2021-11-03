import discord
from discord import errors
from discord.ext import commands
import discord.utils
import asyncio
import os
import json
import requests

class Genshin(commands.Cog):
    """
    Trying out a Genshin API
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def genshin(self, ctx):
      await ctx.reply('A Genshin command in the works.')

    @genshin.command()
    async def character(self, ctx, *character = None):
        if character is None:
            embed = discord.Embed(title='Character Profiles', description='Learn more about characters in Genshin! For a list of available characters use `sc!genshin characters`.')
        else:
            character = character.lower()
            response = requests.get(f'https://api.genshin.dev/characters/{character}/')
            if response.status_code == 200:
                embed = discord.Embed(title=f"{character.capitalize()}'s Profile", description=f'Learn more about {character.capitalize()}!.')
                embed.set_thumbnail(url=f'https://api.genshin.dev/characters/{character}/icon-big')
                embed.add_field(name='Vision', value=response.json()['vision'], inline=True)
                embed.add_field(name='Weapon Type', value=response.json()['weapon'], inline=True)
                embed.add_field(name='Place of Origin', value=response.json()['nation'], inline=True)
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Profiles', description='That person does not exist! Please make sure you typed it correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_thumbnail(url=f'https://api.genshin.dev/characters/{character}/icon-big')
        embed.set_author(name='Character Profiles', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
            

def setup(bot):
    bot.add_cog(Genshin(bot))