import json

from discord.ext import commands
from numpy.random import choice

from utils.choose_random_member import choose_random_member
from utils.get_server_prefix import get_server_prefix
from utils.send_embed import send_embed


class Dare(commands.Cog):
    '''
    Ask a dare question in chat!
    Usage:
    `<prefix> dare [pg | pg13 | r]` (If category not specified, I choose a pg or pg13 question.)
    '''

    def __init__(self, bot):
        self.bot = bot

    async def list_extend(self, list1, list2):
        list1.extend(list2)
        return list1

    @commands.command(aliases=['d'])
    @commands.guild_only()
    async def dare(self, ctx, *, category=None):
        data = json.load(open('data\\questions\\dares.json', 'r'))
        if not category:
            default_category = json.load(open('data\\default_category.json', 'r'))
            if str(ctx.guild.id) in default_category:
                category = default_category[str(ctx.guild.id)]
            else:
                category = 'pg'
        category = category.lower()

        data2 = json.load(open('data\\questions\\serverdares.json', 'r'))
        if str(ctx.guild.id) in data2:
            questions = data2[str(ctx.guild.id)][category]
        else:
            questions = []

        if category == 'add':
            await send_embed(ctx, f'Wrong command?', f'Did you mean to use the add command?'
                                                     f'\n(`{await get_server_prefix(self.bot, ctx)}add '
                                                     f'<truth | dare | wyr> <pg | pg13 | r> <question>`)')
            return

        question_chosen = choice(await self.list_extend(questions, data[category]))
        question_chosen = question_chosen.replace('[random user]', f'{choose_random_member(ctx)}')
        if category in ['pg', 'pg13', 'r']:
            await send_embed(ctx, f'Dare ({category})', question_chosen)

    @dare.error
    async def dare_error(self, ctx, error):
        await send_embed(ctx, 'Invalid category', f'Use `{await get_server_prefix(self.bot, ctx)}dare '
                                                  f'[pg | pg13 | r]`')


def setup(bot):
    bot.add_cog(Dare(bot))
