import asyncio
import logging
import os
import sys

import discord
from discord import RawReactionActionEvent
from discord.ext import commands
from discord.ext.commands import Bot, CommandNotFound, UserInputError, MissingRequiredArgument, Context

from DolaBot.helpers.channel_logger import ChannelLogHandler

from DolaBot.cogs.bot_util_commands import BotUtilCommands
from DolaBot.cogs.meme_commands import MemeCommands
from DolaBot.cogs.sendou_commands import SendouCommands
from DolaBot.cogs.server_commands import ServerCommands
from DolaBot.cogs.slapp_commands import SlappCommands
from DolaBot.cogs.splatoon_commands import SplatoonCommands
from DolaBot.constants.bot_constants import COMMAND_PREFIX


class DolaBot(Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Subscribe to the privileged members intent for roles and reactions.
        intents.presences = False
        intents.typing = False
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents
        )

        # Load Cogs
        self.try_add_cog(BotUtilCommands)
        self.try_add_cog(MemeCommands)
        self.try_add_cog(SendouCommands)
        self.try_add_cog(ServerCommands)
        self.slapp_commands: SlappCommands = self.try_add_cog(SlappCommands)
        self.try_add_cog(SplatoonCommands)

    def try_add_cog(self, cog: commands.cog):
        try:
            new_cog = cog(self)
            self.add_cog(new_cog)
            return new_cog
        except Exception as e:
            logging.error(f"Failed to load {cog=}: {e=}")

    async def on_command_error(self, ctx: Context, error, **kwargs):
        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, UserInputError):
            await ctx.send(error.__str__())
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(error.__str__())
        else:
            raise error

    async def on_message(self, message, **kwargs):
        # We do not want the bot to reply to itself
        if message.author == self.user:
            return
        await self.process_commands(message)

    async def on_ready(self):
        ChannelLogHandler(self)
        logging.info(f'Logged in as {self.user.name}, id {self.user.id}')

        # noinspection PyUnreachableCode
        if __debug__:
            presence = "--=IN DEV=--"
        else:
            presence = "with Slate"

        if 'pydevd' in sys.modules or 'pdb' in sys.modules or '_pydev_bundle.pydev_log' in sys.modules:
            presence += ' (Debug Attached)'

        await self.change_presence(activity=discord.Game(name=presence))

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.user_id != self.user.id:
            await self.slapp_commands.handle_reaction(payload)

    def do_the_thing(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(
                self.slapp_commands.initialise_slapp(),
                self.start(os.getenv("BOT_TOKEN"))
            )
        )
