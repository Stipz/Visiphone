from discord.ext import commands
import json, aiohttp, discord


class PSO2:
    """Commands related to the Emergency Quest alerts"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def eq(self, ctx):
        """EQ-related commands"""

        if ctx.invoked_subcommand is None:
            await self.bot.say('Incorrect subcommand passed. Do ``+help eq`` for the available subcommands.')
                
    @commands.command(pass_context=True)
    async def item(self, ctx, *, itemname : str):
        """Looks up JP name of an item."""

        async with aiohttp.ClientSession() as session:
            url = "http://db.kakia.org/item/search?name={0}".format(itemname.replace(" ", "%20"))
            r = await session.get(url)
            if r.status == 200:
                js = await r.json()
                iteminfo = []

                if js:
                    if len(js) >= 1 and len(js) <= 41:
                        for result in js:
                            if result["EnName"]:
                                iteminfo.append("``{}`` || {}".format(result["EnName"], result["JpName"]))
                                
                        string = "\n".join(iteminfo)
                        message = "{}, Found matches: \n\n{}".format(ctx.message.author.mention, string)
                        await self.bot.say(message)

                    elif len(js) > 41:
                        await self.bot.say("{} ERROR: Too many items matching ``{}``. Please try a more specific search.".format(ctx.message.author.mention, itemname))

                else:
                    await self.bot.say("{} ERROR: No Matches ``{}``, Please check your spelling or copied text.".format(ctx.message.author.mention, itemname))
                    
def setup(bot):
    bot.add_cog(PSO2(bot))
