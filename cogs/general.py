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

    @commands.group()
    async def join(self):
        """Returns information on how to add the bot to your server."""

        botInfo = await self.bot.application_info()
        oauthlink = discord.utils.oauth_url(botInfo.id)
        await self.bot.say('To invite Weeb Bot to your server, simply click the following link: {}'.format(oauthlink))

def setup(bot):
    bot.add_cog(General(bot))
