import discord
from discord.ext import commands
import random

slapGIFs = ["https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png"]
HugGIFs = [""]
KissGIFs = [""]
SmilingGIFs = [""]
TickleGIFs = [""]
HugGIFs = [""]

class Entertainment(commands.Cog, name="💣 Entertainment"):
    """
    General commands that server members can use
    """
    def __init__(self, bot): # Defining the constructor method
        self.bot = bot

    @commands.command(description="Slap a user!")
    async def slap(self, ctx, *, user: discord.Member=None):
        print(type(user))
        if (user is None) or (not isinstance(user, discord.Member)) or (not isinstance(user, discord.User)):
            user = "themselves"
        else:
            user = user.mention
        slapEmbed = discord.Embed(title= "Ouch!", description=f"{ctx.author} slapped {user}!", colour=discord.Color.from_rgb(241,210,231))
        slapEmbed.set_thumbnail(url=random.choice(slapGIFs))
        await ctx.reply(embed=slapEmbed, mention_author=False)
        
    @commands.command(description = "Hugs the tagged user!")
    async def hug(self, ctx, *, user:discord.Member=None):
        
        
        
        await ctx.reply(embed=, mention_author=False)
    
    @commands.command(description = "Kisses the tagged user!")
    async def kiss(self, ctx, *, user:dicsord.Member=None):  
        
        
        
        await ctx.reply(embed=, mention_author=False)

        
    @commands.command(description = "Smiles at the tagged user!")
    async def smile(self, ctx, *, user:discord.Member=None):  
        
        
        
        await ctx.reply(embed=, mention_author=False)
    
    @commands.command(description = "Tickles the tagged user!")
    async def tickle(self, ctx, *, user:discord.Member=None):  
        
        
        
        await ctx.reply(embed=, mention_author=False)
    
    @commands.command(description = "Holds Hands with the tagged user!")
    async def hh(self,ctx, *, user:discord.Member=None): 
        
        
        
        await ctx.reply(embed=, mention_author=False)
        


def setup(bot):
    bot.add_cog(Entertainment(bot))
