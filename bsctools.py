import sqlite3
from discord.ext import commands

conn = sqlite3.connect('bsc.db')
c = conn.cursor()


class bsctools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='bsc', aliases=['genbsc', 'bscgen'])
    async def bsc(self, context, bscinput):

        def gen_links(contract):
            return f"""**Price History Chart:** https://charts.bogged.finance/?token={contract}
**BscScan:** https://bscscan.com/token/{contract}
**PancakeSwap:** https://exchange.pancakeswap.finance/#/swap?outputCurrency={contract}"""

        if bscinput.startswith("0x"):  # if user bscinput starts with 0x, assume it is an addr and directly make links
            await context.reply(gen_links(bscinput))
            await context.reply(bscinput)
        else:  # otherwise assume we are attempting to call an alias for a contract
            c.execute("SELECT contract FROM tokens WHERE alias=?", (bscinput.lower(),))
            result = None
            try:
                result = c.fetchone()[0]
            except TypeError:
                pass
            if result is None:
                await context.reply(f"Contract for token __**{bscinput}**__ not found.")
            else:
                await context.reply(gen_links(result))
                await context.reply(result)

    @commands.command(name='savebsc')
    async def savebsc(self, context, alias, contract):
        c.execute("DELETE FROM tokens WHERE alias=?", (alias,))
        c.execute("INSERT INTO tokens(alias, contract) VALUES (?, ?)", (alias.lower(), contract))
        conn.commit()
        await context.reply(f"Added alias __**{alias}**__ to contract __**{contract}**__.")

    @commands.command(name='delbsc')
    async def delbsc(self, context, alias):
        c.execute("SELECT contract FROM tokens WHERE alias=?", (alias.lower(),))
        try:
            result = c.fetchone()[0]
        except TypeError:
            result = None
        if result is None:
            await context.reply(f"Contract for token __**{alias}**__ not found.")
        else:
            c.execute("DELETE FROM tokens WHERE alias=?", (alias,))
            conn.commit()
            await context.reply(f"Contract __**{result}**__ for alias __**{alias}**__ deleted.")

    @commands.command(name='bscsql')
    @commands.is_owner()
    async def bscsql(self, context, command):
        try:
            c.execute(command)
            await context.reply(c.fetchall())
            conn.commit()
        except Exception as e:
            await context.reply(e)


def setup(client):
    client.add_cog(bsctools(client))
