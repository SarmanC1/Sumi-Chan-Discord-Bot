import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 699909552757276732

    @commands.Cog.listener() # Delete msg if invite
    async def on_message(self, message):
        if not message.author.bot and 'discord.gg/' in message.content:
            await message.delete()
            await message.channel.send(f"This is forbidden to send {message.author.mention}!")

    @commands.command(name='invite', description='Creates an invite link for the server')
    @commands.guild_only() # Restricts the command to the guild only
    async def invite(self, ctx):
        invite = await ctx.channel.create_invite()
        await ctx.author.send(str(invite)) #This will send the invite link to the user who asked for it
        loggingchannel = self.bot.get_channel(self.log_channel_id)
        embed = discord.Embed(title= "New Invite", description=f"Invite created by {ctx.author}\nCode: {str(invite)}")
        await loggingchannel.send(embed=embed) #Logs who created the invite link

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.log_channel_id)
        JoinEmbed = discord.Embed(title=f"Welcome {member}", description = f"Thanks for joining {member.guild.name}!")
        JoinEmbed.set_thumbnail(url=member.avatar_url) # Embed's thumbnail = Users PFP
        await channel.send(embed=JoinEmbed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print (f"{member} has left this server :-(")


def setup(bot):
    bot.add_cog(Logs(bot))