from discord.ext import commands
import discord
import aiohttp


class General:
    """General commands"""
    def __init__(self, bot):
        self.bot = bot
    @commands.group(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""
        await self.bot.say('Pong! Channel ID: {}'.format(ctx.message.channel.id))

def setup(bot):
    bot.add_cog(General(bot))
