import json
import re

import discord
from discord.ext import commands

from utils.get_server_prefix import get_server_prefix
from utils.send_embed import send_embed


class Prefix(commands.Cog):
    '''
    Change the server-wide prefix!
    Usage:
    `<prefix> prefix <new prefix>`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pf', 'changeprefix', 'newprefix'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, new_prefix=None):
        old_prefix = await get_server_prefix(self.bot, ctx)
        if not new_prefix:
            await send_embed(ctx, 'Server prefix', f'**{ctx.guild.name}**\'s current prefix is `{old_prefix}`.')
            return
        found = re.findall(r'".+"', new_prefix)
        if found:
            new_prefix = found[0][1:-1]
        else:
            raise Exception
        data = json.load(open('data\\prefixes.json', 'r'))
        data[str(ctx.guild.id)] = new_prefix
        json_data = json.dumps(data)
        f = open('data\\prefixes.json', 'w')
        f.write(json_data)
        f.close()
        await send_embed(ctx, 'Server prefix set',
                         f'**New prefix:** `{new_prefix}`\n'
                         f'**Old prefix:** `{old_prefix}`')

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await send_embed(ctx, 'Could not set prefix', 'You\'re missing administrator permissions to use '
                                                          'this command.')
        else:
            await send_embed(ctx, 'Could not set prefix', f'Surround your new prefix in double quotes.\n'
                                                          f'(ex: `{await get_server_prefix(self.bot, ctx)}prefix "td"`)')


def setup(bot):
    bot.add_cog(Prefix(bot))
