from discord.ext import commands
import json, aiohttp, discord


class PSO2:
    """Commands related to the Emergency Quest alerts"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pso2(self):
        data = discord.Embed(colour=discord.Colour.red())
        data.set_author(name="Phantasy Star Online 2", icon_url="http://img.informer.com/icons/png/48/3365/3365560.png")

        info = "[News](http://bumped.org/psublog)\n[Reddit](http://reddit.com/r/pso2)\n[Guides](http://fulldive.nu)\n[Forums](http://pso-world.com)\n[Wiki](https://pso2.arks-visiphone.com)"
        data.add_field(name="Information", value=info)

        downloads = "[Launcher](http://arks-layer.com)\n[Mods](https://goo.gl/M8PpWh)"
        data.add_field(name="Downloads", value=downloads)

        translations = "English Patch: :ballot_box_with_check:\nStory Patch: :ballot_box_with_check:\nItem Patch: :ballot_box_with_check:"
        data.add_field(name="Translations", value=translations)

        data.set_footer(text="Those are hyperlinks. Give them a click.")

        await self.bot.say(embed=data)

    @commands.group(pass_context=True)
    async def eq(self, ctx):
        """EQ-related commands"""

        if ctx.invoked_subcommand is None:
            await self.bot.say('Incorrect subcommand passed. Do ``+help eq`` for the available subcommands.')

    @eq.command()
    async def last(self):
        """Returns last EQ recorded by the bot"""

        eqs = []
        i = 0

        with open('cogs/json/last_eq.json', 'r') as file:
            file = json.load(file)
            eq = file['text'].splitlines()
            eqtime = file['jst']

            for line in eq:
                if 'Emergency Quest' not in line and line != 'Ship%02d: -' % i and line.startswith('Ship'):
                    line = '``' + line.replace(':', ':``')
                    line = line.replace('Ship', 'SHIP ')
                    eqs.append(line)

                if line == 'All ships are in event preparation.':
                    eqs.append('``' + line + '``')

                if line.startswith('[In Progress]'):
                    line = line.replace('[In Progress]', '``IN PROGRESS:``')
                    eqs.append(line)

                if line.startswith('[In Preparation]'):
                    line = line.replace('[In Preparation]', '``IN 1 HOUR:``')
                    eqs.append(line)

                if line.startswith('[1 hour later]'):
                    line = line.replace('[1 hour later]', '``IN 2 HOURS:``')
                    eqs.append(line)

                if line.startswith('[2 hours later]'):
                    line = line.replace('[2 hours later]', '``IN 3 HOURS:``')
                    eqs.append(line)

                i += 1

            string = '\n'.join(eqs)
            message = ':loudspeaker: **Last Emergency Quest Update:** JP Time: `%s00HRS`\n\n%s' % (eqtime, string)

            await self.bot.say(message)

    @eq.command(pass_context=True)
    async def enable(self, ctx):
        """Enables Emergency Quest alerts on this channel."""

        # Loads eq_channels.json file
        with open('cogs/json/eq_channels.json', encoding="utf8") as eq_channels:
            eq_channels = json.load(eq_channels)

        if ctx.message.channel.id not in eq_channels['channels']:
            # Writes channel ID to file
            with open('cogs/json/eq_channels.json', 'w') as outfile:
                eq_channels['channels'].append(ctx.message.channel.id)
                json.dump(eq_channels, outfile)

            await self.bot.say("EQ alerts successfully enabled on this channel.")
        else:
            await self.bot.say('EQ alerts are already enabled on this channel.')

    @eq.command(pass_context=True)
    async def disable(self, ctx):
        """Disables Emergency Quest alerts on this channel."""

        # Loads eq_channels.json file
        with open('cogs/json/eq_channels.json', encoding="utf8") as eq_channels:
            eq_channels = json.load(eq_channels)

        if ctx.message.channel.id in eq_channels['channels']:
            eq_channels['channels'].remove(ctx.message.channel.id)

            # Writes channel ID to file
            with open('cogs/json/eq_channels.json', 'w') as outfile:
                json.dump(eq_channels, outfile)

            await self.bot.say("EQ alerts now disabled on this channel.")

        else:
            await self.bot.say("EQ alerts are not enabled on this channel.")

 #  @commands.command(pass_context=True)
 #  async def price(self, ctx, *, itemname : str):
 #      """Looks up the price of an item."""
 #
 #       async with aiohttp.ClientSession() as session:
 #           url = "http://db.kakia.org/item/search?name={0}".format(itemname.replace(" ", "%20"))
 #           r = await session.get(url)
 #           if r.status == 200:
 #               js = await r.json()
 #               iteminfo = []
 #
 #               if js:
 #                   if len(js) >= 1 and len(js) <= 1:
 #                       for result in js:
 #                           if result["EnName"]:
                                #iteminfo.append("``EN Name:`` {} | ``JP Name:`` {}\n\n``Ship 01:`` {:,.0f}\n``Ship 02:`` {:,.0f}\n``Ship 03:`` {:,.0f}\n``Ship 04:`` {:,.0f}\n``Ship 05:`` {:,.0f}\n``Ship 06:`` {:,.0f}\n``Ship 07:`` {:,.0f}\n``Ship 08:`` {:,.0f}\n``Ship 09:`` {:,.0f}\n``Ship 10:`` {:,.0f}\n".format(result["EnName"], result["JpName"]
                                #                                          , result["PriceInfo"][9]["Price"]
                                #                                          , result["PriceInfo"][4]["Price"]
                                #                                          , result["PriceInfo"][7]["Price"]
                                #                                          , result["PriceInfo"][8]["Price"]
                                #                                          , result["PriceInfo"][5]["Price"]
                                #                                          , result["PriceInfo"][6]["Price"]
                                #                                          , result["PriceInfo"][2]["Price"]
                                #                                          , result["PriceInfo"][0]["Price"]
                                #                                          , result["PriceInfo"][3]["Price"]
#                                          , result["PriceInfo"][1]["Price"]))
#                                iteminfo.append("``EN Name:`` {} | ``JP Name:`` {}\nPrice: {:,.0f}\n".format(result["EnName"], result["JpName"] , result["PriceInfo"][8]["Price"]))
#                        string = "\n".join(iteminfo)
#                        #message = "{} Here are the results of your query:\n{}".format(ctx.message.author.mention, string)
#                        message = "{} Here are the results of your [price] query: \n{}\n".format(ctx.message.author.mention, string)
#                        await self.bot.say(message)
#
#                    elif len(js) > 60:
#                        await self.bot.say("{} Sorry Master, I found too many items matching ``{}``. Please try a more specific search.".format(ctx.message.author.mention, itemname))
#
#                else:
#                    await self.bot.say("{} Sorry Master, I couldn't find ``{}``.".format(itemname))
#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
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
                    if len(js) >= 1 and len(js) <= 35:
                        for result in js:
                            if result["EnName"]:
                                iteminfo.append("``EN Name:`` {} || ``JP Name:`` {}".format(result["EnName"], result["JpName"]))
                                
                        string = "\n".join(iteminfo)
                        
                        message = "{} Here are the results of your ``+ item`` query:\n\n{}".format(ctx.message.author.mention, string)
                        await self.bot.say(message)

                    elif len(js) > 99:
                        await self.bot.say("{} Sorry Master, I found too many items matching ``{}``. Please try a more specific search.".format(ctx.message.author.mention, itemname))

                else:
                    await self.bot.say("{} Sorry Master, I couldn't find ``{}``, Please check your spelling or pasted item name.".format(ctx.message.author.mention, itemname))

def setup(bot):
    bot.add_cog(PSO2(bot))
