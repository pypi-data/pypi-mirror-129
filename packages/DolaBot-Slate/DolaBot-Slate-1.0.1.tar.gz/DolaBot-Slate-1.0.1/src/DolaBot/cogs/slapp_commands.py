"""Slapp commands cog."""
import asyncio
import io
import logging
import re
import traceback
from collections import namedtuple, deque, OrderedDict
from typing import Optional, List, Tuple, Dict, Deque, Union, Coroutine

from DolaBot.helpers.discord_renderer_helper import safe_backticks, close_backticks_if_unclosed, wrap_in_backticks
from DolaBot.helpers.supports_send import SupportsSend
from battlefy_toolkit.downloaders.org_downloader import get_tournament_ids
from slapp_py.core_classes.builtins import UNKNOWN_PLAYER
from slapp_py.core_classes.division import Division
from slapp_py.core_classes.name import Name
from slapp_py.core_classes.player import Player
from slapp_py.core_classes.skill import Skill
from slapp_py.core_classes.team import Team

from discord import Color, Embed, File, Message, RawReactionActionEvent, errors
from discord.ext import commands
from discord.ext.commands import Context, Bot

from slapp_py.misc.download_from_battlefy_result import download_from_battlefy
from slapp_py.misc.models.battlefy_team import BattlefyTeam
from slapp_py.slapp_runner.simple_source import SimpleSource
from slapp_py.slapp_runner.slapipes import MAX_RESULTS, SlapPipe
from slapp_py.slapp_runner.slapp_response_object import SlappResponseObject

from DolaBot.constants import emojis
from DolaBot.constants.bot_constants import COMMAND_PREFIX
from DolaBot.constants.emojis import TOP_500, TROPHY, TICK, TURTLE, RUNNING, LOW_INK, NUMBERS_KEY_CAPS, TYPING, CROSS, \
    NUMBERS_KEY_CAPS_LEN
from DolaBot.constants.footer_phrases import get_random_footer_phrase
from DolaBot.helpers.embed_helper import to_embed
from DolaBot.helpers.processed_slapp_object import ProcessedSlappObject
from slapp_py.helpers.str_helper import join, truncate, escape_characters

from operator import itemgetter


SlappQueueItem = namedtuple('SlappQueueItem', ('SupportsSend', 'str'))
slapp_ctx_queue: Deque[SlappQueueItem] = deque()
slapp_reacts_queue: OrderedDict[str, Dict[str, Union[Player, Team]]] = OrderedDict()
module_autoseed_list: Optional[Dict[str, List[SlappResponseObject]]] = dict()
module_html_list: Optional[Dict[str, List[SlappResponseObject]]] = dict()
module_predict_team_1: Optional[dict] = None
slapp_started: bool = False
slapp_caching_finished: bool = False


async def add_to_queue(ctx: Union[None, SupportsSend, Context], description: str):
    if isinstance(ctx, Context):
        await ctx.message.add_reaction(RUNNING if slapp_caching_finished else TURTLE)
    slapp_ctx_queue.append(SlappQueueItem(ctx, description))


async def handle_html(ctx: Optional[SupportsSend], description: str, response: Optional[dict]):
    global module_html_list

    if description.startswith("html_start"):
        module_html_list.clear()
        return
    elif not description.startswith("html_end"):
        team_name = description.rpartition(':')[2]  # take the right side of the colon
        if module_html_list.get(team_name):
            module_html_list[team_name].append(SlappResponseObject(response))
        else:
            module_html_list[team_name] = [SlappResponseObject(response)]
        return

    # End, do the thing
    message = ''

    # Team name, list of players, clout, confidence, emoji str
    teams_by_clout: List[Tuple[str, Dict[Player, SlappResponseObject], int, int, str]] = []

    if module_html_list:
        for team_name in module_html_list:
            team_players = {}
            team_awards = []
            for r in module_html_list[team_name]:
                if r.matched_players_len == 0:
                    p = Player(names=[Name(value=r.query or UNKNOWN_PLAYER, sources=r.sources.keys())])
                    pass
                elif r.matched_players_len > 1:
                    p = Player.soft_merge_from_multiple(r.matched_players)
                    message += f"Soft merged player with query {r.query} with " \
                               f"({r.matched_players_len} results\n"
                else:
                    p = r.matched_players[0]

                team_players[p] = r
                team_awards.append(r.get_first_placements(p))

            player_skills = [player.skill for player in team_players]
            player_skills.sort(reverse=True)
            awards = TROPHY * len({award for award_line in team_awards for award in award_line})
            awards += TOP_500 * len([player for player in team_players if player.top500])
            (_, _), (max_clout, max_confidence) = Skill.team_clout(player_skills)
            teams_by_clout.append(
                (team_name,
                 team_players,
                 max_clout,
                 max_confidence,
                 awards)
            )
    else:
        message = "Err... I didn't get any teams back from Slapp."

    if message:
        await ctx.send(message)

    # Free free to ignore this LOL
    row_count = 1
    html_begin = f"""<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><link type="text/css" rel="stylesheet" href="resources/sheet.css"><style type="text/css">.ritz .waffle a {{ color: inherit; }}.ritz .waffle .s8{{background-color:#9900ff;text-align:right;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s0{{background-color:#fce5cd;text-align:center;font-weight:bold;color:#000000;font-family:'Arial';font-size:14pt;vertical-align:middle;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s7{{background-color:#25c274;text-align:right;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s12{{background-color:#fbbc04;text-align:left;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s1{{background-color:#4a86e8;text-align:right;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s6{{background-color:#34a853;text-align:left;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;color:#1155cc;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s2{{background-color:#34a853;text-align:left;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s3{{background-color:#ffffff;text-align:left;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s10{{background-color:#9900ff;text-align:right;color:#000000;font-family:'docs-Roboto',Arial;font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s4{{background-color:#ffffff;text-align:center;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s5{{background-color:#00ff00;text-align:right;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s14{{background-color:#4285f4;text-align:left;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s13{{background-color:#ff6d01;text-align:left;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s9{{background-color:#ea4335;text-align:left;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}}.ritz .waffle .s11{{background-color:#4a86e8;text-align:right;color:#000000;font-family:'docs-Roboto',Arial;font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}} .tooltip {{ position: relative;  display: inline-block;  border-bottom: 1px dotted black;}} .tooltip .tooltiptext {{visibility: hidden; background-color: black;  color: #fff;  text-align: center;  padding: 5px 0;  border-radius: 6px;  position: absolute;  z-index: 1;}} .tooltip:hover .tooltiptext {{visibility: visible;}}</style></head>\n<body><div class="ritz grid-container" dir="ltr"><table class="waffle" cellspacing="0" cellpadding="0"><thead><tr><th class="row-header freezebar-origin-ltr"></th><th id="810171351C0" style="width:30px;" class="column-headers-background">A</th><th id="810171351C1" style="width:170px;" class="column-headers-background">B</th><th id="810171351C2" style="width:150px;" class="column-headers-background">C</th><th id="810171351C3" style="width:150px;" class="column-headers-background">D</th><th id="810171351C4" style="width:150px;" class="column-headers-background">E</th><th id="810171351C5" style="width:150px;" class="column-headers-background">F</th><th id="810171351C6" style="width:150px;" class="column-headers-background">G</th><th id="810171351C7" style="width:150px;" class="column-headers-background">H</th><th id="810171351C8" style="width:150px;" class="column-headers-background">I</th><th id="810171351C9" style="width:150px;" class="column-headers-background">J</th><th id="810171351C10" style="width:150px;" class="column-headers-background">K</th><th id="810171351C11" style="width:150px;" class="column-headers-background">L</th><th id="810171351C12" style="width:150px;" class="column-headers-background">M</th><th id="810171351C13" style="width:150px;" class="column-headers-background">N</th><th id="810171351C14" style="width:150px;" class="column-headers-background">O</th><th id="810171351C15" style="width:150px;" class="column-headers-background">P</th><th id="810171351C16" style="width:150px;" class="column-headers-background">Q</th><th id="810171351C17" style="width:150px;" class="column-headers-background">R</th><th id="810171351C18" style="width:150px;" class="column-headers-background">S</th><th id="810171351C19" style="width:150px;" class="column-headers-background">T</th><th id="810171351C20" style="width:150px;" class="column-headers-background">U</th><th id="810171351C21" style="width:150px;" class="column-headers-background">V</th><th id="810171351C22" style="width:150px;" class="column-headers-background">W</th><th id="810171351C23" style="width:150px;" class="column-headers-background">X</th><th id="810171351C24" style="width:150px;" class="column-headers-background">Y</th><th id="810171351C25" style="width:150px;" class="column-headers-background">Z</th></tr></thead><tbody><tr style="height: 30px"><th id="810171351R0" style="height: 30px;" class="row-headers-background"><div class="row-header-wrapper" style="line-height: 30px">{row_count}</div></th><td class="s0" dir="ltr">#</td><td class="s0" dir="ltr">Team Name<br></td><td class="s0" dir="ltr">Player 1</td><td class="s0" dir="ltr">Player 2</td><td class="s0" dir="ltr">Player 3</td><td class="s0" dir="ltr">Player 4</td><td class="s0" dir="ltr">Player 5</td><td class="s0" dir="ltr">Player 6</td><td class="s0" dir="ltr">Player 7</td><td class="s0" dir="ltr">Player 8</td><td class="s0" dir="ltr">Last Updated</td><td class="s0" dir="ltr">Removed 1<br></td><td class="s0" dir="ltr">Removed 2<br></td><td class="s0" dir="ltr">Removed 3<br></td><td class="s0" dir="ltr">Removed 4<br></td><td class="s0" dir="ltr">Removed 5<br></td><td class="s0" dir="ltr">Removed 6<br></td><td class="s0" dir="ltr">Removed 7<br></td><td class="s0" dir="ltr">Removed 8<br></td><td class="s0" dir="ltr">Removed 9<br></td><td class="s0" dir="ltr">Removed 10<br></td><td class="s0" dir="ltr">Removed 11<br></td><td class="s0" dir="ltr">Removed 12<br></td><td class="s0" dir="ltr">Removed 13<br></td><td class="s0" dir="ltr">Removed 14<br></td><td class="s0" dir="ltr">Removed 15<br></td></tr>\n"""
    html_end = """</tbody></table></div></body></html>"""
    style_good = "s2"
    style_banned = "s9"
    style_needs_checking = "s12"
    style_exception = "s14"

    # Order by clout for the team seed
    ordered = sorted(teams_by_clout, key=itemgetter(2), reverse=True)
    output = html_begin
    for tup in teams_by_clout:
        team_name, team_players, max_clout, max_confidence, awards = tup
        row_count += 1
        output += f"""<tr style="height: 20px">\n<th id="810171351R{row_count}" style="height: 20px;" class="row-headers-background"><div class="row-header-wrapper" style="line-height: 20px">{row_count}</div></th>\n"""

        # 1. break down team into the players
        # 2. calculate the seed from those players
        # 3. for each player, write a cell and style by that player's eligibility
        player_output = ''
        player_styles = []
        for player in team_players:
            style = style_needs_checking

            r = team_players[player]
            best_div = r.get_best_division_for_player(player)
            low_ink_placements = r.get_low_ink_placements(player)
            best_li_placement = r.best_low_ink_placement(player)
            if r.placement_is_winning_low_ink(best_li_placement):
                style = style_banned
            elif best_div.normalised_value == 4:
                style = style_exception
            elif best_div.normalised_value <= 3:
                style = style_banned
            # Considering adding this, but if we're in December and the last result was at the beginning of the year,
            # or indeed years ago, then this wouldn't be a good indication.
            # elif best_li_placement is not None:
            #     style = STYLE_GOOD
            elif not best_div.is_unknown:
                style = style_good

            player_styles.append(style)
            names = list(set([name.value for name in player.names if name and name.value]))
            names = truncate(', '.join(names[0:]), 1000, "…")

            player_detail = f"Names: {names} \n"
            player_detail += f"Best Div: {best_div} \n"
            if best_li_placement:
                player_detail += f"Best LI: Came {best_li_placement[0]} in {best_li_placement[1]} in {best_li_placement[2]} \n"
            if len(low_ink_placements) > 1:
                for placement in low_ink_placements:
                    if placement != best_li_placement:
                        player_detail += f"LI placements: Came {placement[0]} in {placement[1]} in {placement[2]} \n"
            player_detail += f"Teams: {join(', ', r.get_teams_for_player(player))} \n"
            player_output += f"""<td class="{style}" dir="ltr"><div class="tooltip">{player.name}<pre class="tooltiptext">{player_detail}</pre></div></td>\n"""

        team_seed_colour = style_good if max_confidence > 70 else style_needs_checking
        team_name_colour = style_good if all(style == style_good for style in player_styles) else style_needs_checking

        team_seed = ordered.index(tup) + 1
        team_detail = f"Clout: {max_clout} ({max_confidence}% confidence) {awards}"
        output += f"""<td class="{team_seed_colour}" dir="ltr">{team_seed}</td>\n"""
        output += f"""<td class="{team_name_colour}" dir="ltr"><div class="tooltip">{team_name}<pre class="tooltiptext">{team_detail}</pre></div></td>\n"""
        output += player_output

        output += """</tr>\n"""

    output += html_end
    f = io.StringIO(output)
    await ctx.send(content="Here ya go! 🎈", file=File(fp=f, filename="Verifications.html"))


class SlappCommands(commands.Cog):
    """A grouping of Slapp-related commands."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.slappipe = SlapPipe()
        self.restart_context = None

    def initialise_slapp(self) -> Coroutine:
        return self.slappipe.initialise_slapp(self.receive_slapp_response)

    @staticmethod
    def has_slapp_started():
        return slapp_started

    @staticmethod
    def has_slapp_caching_finished():
        return slapp_caching_finished

    @staticmethod
    def get_slapp_queue_length():
        return len(slapp_ctx_queue)

    async def handle_reaction(self, payload: RawReactionActionEvent):
        channel = await self.bot.fetch_channel(payload.channel_id)
        response = slapp_reacts_queue.get(payload.message_id, {}).get(payload.emoji.name)

        handled = False
        if response:
            logging.info(f"Reaction received matching message {payload.message_id=}, {payload.emoji.name=}")
            if isinstance(response, Player) or isinstance(response, Team):
                await add_to_queue(channel, "full")
                await self.slappipe.slapp_describe(str(response.guid))
                handled = True
            else:
                await channel.send(f"Something went wrong with handling the react: {response=}")

        if handled:
            slapp_reacts_queue[payload.message_id].pop(payload.emoji.name)
            message: Message = await channel.fetch_message(payload.message_id)
            try:
                await message.clear_reaction(payload.emoji.name)
            except errors.Forbidden:
                pass

    @staticmethod
    def prepare_bulk_slapp(teams_to_search: List[dict]) -> Tuple[str, List[Tuple[str, str]]]:
        verification_message = ''
        players_to_queue: List[(str, str)] = []

        for team in teams_to_search:
            team_name = team.get('name', None)
            team_id = team.get('persistentTeamID', None)

            if not team_name or not team_id:
                continue

            players = team.get('players', None)
            if not players:
                verification_message += f'Ignoring team {team_name} ({team_id}) because they have no players!\n'
                continue

            ignored_players = [truncate(player.get("inGameName", "(unknown player)"), 25, '…')
                               for player in players if not player.get('persistentPlayerID')]

            players = [player for player in players if player.get('persistentPlayerID')]
            if len(players) < 4:
                verification_message += f"Ignoring the player(s) from team {team_name} ({team_id}) as they don't have a persistent id: [{', '.join(ignored_players)}]\n"
                verification_message += f"The team {team_name} ({team_id}) only has {len(players)} players with persistent ids, not calculating.\n"
                continue

            for player in players:
                player_slug = player['persistentPlayerID']  # We've already verified this field is good
                players_to_queue.append((team_name, player_slug))

        return verification_message, players_to_queue

    @commands.command(
        name='autoseed',
        description="Auto seed the teams that have signed up to the tourney",
        help=f'{COMMAND_PREFIX}autoseed <tourney_id>',
        pass_ctx=True)
    async def autoseed(self, ctx: Context, tourney_id: Optional[str]):
        if not tourney_id:
            tourney_id = '6019b6d0ce01411daff6bca6'

        tournament = list(download_from_battlefy(tourney_id, force=True))
        if isinstance(tournament, list) and len(tournament) == 1:
            tournament = tournament[0]

        if len(tournament) == 0:
            await ctx.send(f"I couldn't download the latest tournament data 😔 (id: {tourney_id})")
            return

        if not any(team.get('players', None) for team in tournament):
            await ctx.send(f"There are no teams in this tournament 😔 (id: {tourney_id})")
            return

        verification_message, players_to_queue = SlappCommands.prepare_bulk_slapp(tournament)

        # Do the autoseed list
        await add_to_queue(None, 'autoseed_start')
        for pair in players_to_queue:
            await add_to_queue(None, 'autoseed:' + pair[0])
            await self.slappipe.query_slapp(pair[1])
        await add_to_queue(ctx, 'autoseed_end')

        if verification_message:
            await ctx.send(verification_message)

        # Finished in handle_autoseed

    @commands.command(
        name='verify',
        description="Verify a signed-up team.",
        help=f'{COMMAND_PREFIX}verify <team_slug>',
        pass_ctx=True)
    async def verify(self, ctx: Context, team_slug_or_name_or_confirmation: Optional[str], tourney_id: Optional[str]):
        if not slapp_started:
            await ctx.send(f"⏳ Slapp is not running yet.")
            return

        if not tourney_id:
            tourney_id = SlappCommands.get_latest_ipl()

        tournament = list(download_from_battlefy(tourney_id, force=True))
        if isinstance(tournament, list) and len(tournament) == 1:
            tournament = tournament[0]

        if len(tournament) == 0:
            await ctx.send(f"I couldn't download the latest tournament data 😔 (id: {tourney_id})")
            return

        if not team_slug_or_name_or_confirmation:
            await ctx.send(f"Found {len(tournament)} teams for tourney {tourney_id}.\n"
                           f"To verify all these teams use `{COMMAND_PREFIX}verify all`.\n"
                           f"Or verify individual teams with `{COMMAND_PREFIX}verify team_slug_or_name`")
            return

        if not any(team.get('players', None) for team in tournament):
            await ctx.send(f"There are no teams in this tournament 😔 (id: {tourney_id})")
            return

        do_all: bool = team_slug_or_name_or_confirmation.lower() == "all"
        verification_message: str = ""

        if do_all:
            await self.begin_slapp_html(ctx, tournament)
        else:
            team_slug = team_slug_or_name_or_confirmation
            for team in tournament:
                t = BattlefyTeam.from_dict(team)
                if not t.name or not t.persistent_team_id or not t.name:
                    verification_message += f'The team data is incomplete or in a bad format.\n'
                    break

                if team_slug in (team['_id'], t.persistent_team_id, t.name):
                    if not t.players:
                        verification_message += f'The team {t.name} ({t.persistent_team_id}) has no players!\n'
                        continue
                    await ctx.send(content=f'Checking team: {t.name} ({t.persistent_team_id})')

                    for player in t.players:
                        if not player.user_slug:
                            verification_message += f'The team {t.name} ({t.persistent_team_id}) has a player with no slug!\n'
                            continue
                        else:
                            await add_to_queue(ctx, 'verify')
                            await self.slappipe.query_slapp(player.user_slug)
                else:
                    continue

        if verification_message:
            await ctx.send(verification_message)

    @commands.command(
        name='restartslapp',
        description="Restarts Slapp",
        help=f'{COMMAND_PREFIX}restartslapp',
        pass_ctx=True)
    async def restartslapp(self, ctx):
        import discord
        # DolaPro role
        has_perm = await ctx.bot.is_owner(ctx.author) or await discord.utils.get(ctx.author.roles, id=900869242767966228)
        if has_perm:
            await self._restart_slapp(ctx)
            await ctx.message.add_reaction(TYPING)
        else:
            await ctx.send("Get a DolaPro to restart Slapp.")

    @commands.command(
        name='patchslapp',
        description="Patches Slapp with new data",
        help=f'{COMMAND_PREFIX}patchslapp',
        pass_ctx=True)
    async def patchslapp(self, ctx: Context, *, urls: Optional[str]):
        import discord
        # DolaPro role
        has_perm = await ctx.bot.is_owner(ctx.author) or await discord.utils.get(ctx.author.roles, id=900869242767966228)
        if has_perm:
            await self._patch_slapp(ctx, urls)
            await ctx.message.add_reaction(TYPING)
        else:
            await ctx.send("Get a DolaPro to patch Slapp.")

    @commands.command(
        name='Slapp',
        description="Query the slapp for a Splatoon player, team, tag, or other information",
        brief="Splatoon player and team lookup",
        aliases=['slapp', 'splattag', 'search'],
        help=f'{COMMAND_PREFIX}search <mode_to_translate>',
        pass_ctx=True)
    async def slapp(self, ctx: Context, *, query):
        if not slapp_started:
            await ctx.send(f"⏳ Slapp is not running yet.")
            return

        if len(query) < 3:
            await ctx.send("💡 Your query is small so might take a while. "
                           "You can help by specifying `--exactcase` and/or `--clantag`, `--player`, `--team` as appropriate.")

        logging.debug('slapp called with query ' + query)
        await add_to_queue(ctx, 'slapp')
        query_sent = await self.slappipe.query_slapp(query, limit=20)
        if re.search(r"(\s+|^)(--|–|—)\S+", query_sent):
            await ctx.send("💡 It looks like you have an option but is misspelled or not recognised. "
                           "If so, please retype your query. Otherwise, ignore this message and Slapp will run.")

    @commands.command(
        name='Slapp (Full description)',
        description="Fully describe the given id.",
        brief="Splatoon player or team full description",
        aliases=['full', 'describe'],
        help=f'{COMMAND_PREFIX}full <slapp_id>',
        pass_ctx=True)
    async def full(self, ctx: Context, slapp_id: str):
        logging.info('full called with slapp_id ' + slapp_id)
        await add_to_queue(ctx, 'full')
        await self.slappipe.slapp_describe(slapp_id)

    @commands.command(
        name='Fight',
        description="Get a match rating and predict the winner between two teams or two players.",
        brief="Two Splatoon teams/players to fight and rate winner",
        aliases=['fight', 'predict'],
        help=f'{COMMAND_PREFIX}predict <slapp_id_1> <slapp_id_2>',
        pass_ctx=True)
    async def predict(self, ctx: Context, slapp_id_team_1: str, slapp_id_team_2: str):
        logging.info(f'predict called with teams {slapp_id_team_1=} {slapp_id_team_2=}')
        await add_to_queue(ctx, 'predict_1')
        await self.slappipe.slapp_describe(slapp_id_team_1)
        await add_to_queue(ctx, 'predict_2')
        await self.slappipe.slapp_describe(slapp_id_team_2)
        # This comes back in the receive_slapp_response -> handle_predict

    @staticmethod
    async def send_slapp(ctx: SupportsSend, success_message: str, response: SlappResponseObject):
        if success_message == "OK":
            try:
                processed = await process_slapp(response)
            except Exception as e:
                if ctx:
                    await ctx.send(content=f'Something went wrong processing the result from Slapp. Blame Slate. 😒🤔 '
                                           f'({e.__str__()})')
                logging.exception(exc_info=e, msg=traceback.format_exc())
                return

            await SlappCommands.send_built_slapp(ctx, processed)

        elif ctx:
            await ctx.send(content=f'Unexpected error from Slapp 🤔: {success_message}')
        else:
            logging.error(f'Unexpected error from Slapp and no context to post to. 🤔: {success_message}')

    @staticmethod
    async def send_built_slapp(ctx: SupportsSend, processed: ProcessedSlappObject) -> None:
        builder = processed.embed
        last_message_sent = None

        try:
            removed_fields: List[dict] = []
            message = 1
            # Only send 10 messages tops
            while message <= 10:
                # While the message is more than the allowed 6000, or
                # The message has more than 20 fields, or
                # The removed fields has one only (the footer cannot be alone)
                while builder.__len__() > 6000 or len(builder.fields) > 20 or len(removed_fields) == 1:
                    index = len(builder.fields) - 1
                    removed: dict = builder._fields[index]
                    builder.remove_field(index)
                    removed_fields.append(removed)

                if ctx and builder:
                    last_message_sent = await ctx.send(embed=builder)
                    # Let other async processes do their things
                    await asyncio.sleep(0.001)  # 1ms yield

                if len(removed_fields):
                    message += 1
                    removed_fields.reverse()
                    builder = Embed(title=f'Page {message}', colour=processed.colour, description='')
                    for field in removed_fields:
                        try:
                            builder._fields.append(field)
                        except AttributeError:
                            builder._fields = [field]
                    removed_fields.clear()
                else:
                    break

            # Now we're at the end, react to the last message
            if last_message_sent is not None:
                for react in processed.reacts:
                    await last_message_sent.add_reaction(react)

                # and record in a buffer
                add_to_reacts_buffer(last_message_sent.id, processed.reacts)

        except Exception as e:
            if ctx:
                await ctx.send(content=f'Too many results, sorry 😔 ({e.__str__()})')
            logging.exception(exc_info=e, msg=traceback.format_exc())
            logging.info(f'Attempted to send:\n{builder.to_dict()}')

    @staticmethod
    async def handle_autoseed(ctx: Optional[SupportsSend], description: str, response: Optional[dict]):
        global module_autoseed_list

        if description.startswith("autoseed_start"):
            module_autoseed_list.clear()
        elif not description.startswith("autoseed_end"):
            team_name = description.rpartition(':')[2]  # take the right side of the colon
            if module_autoseed_list.get(team_name):
                module_autoseed_list[team_name].append(SlappResponseObject(response))
            else:
                module_autoseed_list[team_name] = [SlappResponseObject(response)]
        else:
            # End, do the thing
            message = ''

            # Team name, list of players, clout, confidence, emoji str
            teams_by_clout: List[Tuple[str, List[str], int, int, str]] = []

            if module_autoseed_list:
                for team_name in module_autoseed_list:
                    team_players = []
                    team_awards = []
                    for r in module_autoseed_list[team_name]:
                        if r.matched_players_len == 0:
                            p = Player(names=[Name(value=r.query or UNKNOWN_PLAYER, sources=r.sources.keys())])
                            pass
                        elif r.matched_players_len > 1:
                            p = Player(names=[Name(value=r.query or UNKNOWN_PLAYER, sources=r.sources.keys())])
                            message += f"Too many matches for player {r.query} 😔 " \
                                       f"({r.matched_players_len=})\n"
                        else:
                            p = r.matched_players[0]

                        team_players.append(p)
                        team_awards.append(r.get_first_placements(p))

                    player_skills = [player.skill for player in team_players]
                    player_skills.sort(reverse=True)
                    awards = TROPHY * len({award for award_line in team_awards for award in award_line})
                    awards += TOP_500 * len([player for player in team_players if player.top500])
                    (_, _), (max_clout, max_confidence) = Skill.team_clout(player_skills)
                    teams_by_clout.append(
                        (team_name,
                         [truncate(player.name.value, 25, '…') for player in team_players],
                         max_clout,
                         max_confidence,
                         awards)
                    )
                teams_by_clout.sort(key=itemgetter(2), reverse=True)
            else:
                message = "Err... I didn't get any teams back from Slapp."

            if message:
                if ctx:
                    await ctx.send(message)
                else:
                    logging.warning("Sending a message without context: ")
                    logging.info(message)

            message = ''
            lines: List[str] = ["Here's how I'd order the teams and their players from best-to-worst, and assuming each team puts its best 4 players on:\n```"]
            for line in [f"{truncate(tup[0], 50, '…')} (Clout: {tup[2]} with {tup[3]}% confidence) [{', '.join(tup[1])}] {tup[4]}" for tup in teams_by_clout]:
                lines.append(line)

            for line in lines:
                if len(message) + len(line) > 1996:
                    if ctx:
                        await ctx.send(message + "\n```")
                    else:
                        logging.warning("Sending a message without context: ")
                        logging.info(message + "\n```")
                    message = '```\n'
                message += line + '\n'

            if message:
                message = close_backticks_if_unclosed(message + "\n")
                if ctx:
                    await ctx.send(message)
                else:
                    logging.warning("Sending a message without context: ")
                    logging.info(message)

    @staticmethod
    async def handle_predict(ctx: SupportsSend, description: str, response: dict):
        global module_predict_team_1
        is_part_2 = description == "predict_2"
        if not is_part_2:
            module_predict_team_1 = response
        else:
            response_1 = SlappResponseObject(module_predict_team_1)
            response_2 = SlappResponseObject(response)

            if response_1.matched_players_len == 1 and response_2.matched_players_len == 1:
                matching_mode = 'players'
            elif response_1.matched_teams_len == 1 and response_2.matched_teams_len == 1:
                matching_mode = 'teams'
            else:
                await ctx.send(content=f"I didn't get the right number of players/teams back 😔 "
                                       f"({response_1.matched_players_len=}/{response_1.matched_teams_len=}, "
                                       f"{response_2.matched_players_len=}/{response_2.matched_teams_len=})")
                return

            message = ''
            if matching_mode == 'teams':
                team_1 = response_1.matched_teams[0]
                team_1_skills = response_1.get_team_skills(team_1.guid).values()
                if team_1_skills:
                    (_, _), (max_clout_1, max_conf_1) = Skill.team_clout(team_1_skills)
                    message += Skill.make_message_clout(max_clout_1, max_conf_1, truncate(team_1.name.value, 25, "…")) + '\n'
                else:
                    max_conf_1 = 0

                team_2 = response_2.matched_teams[0]
                team_2_skills = response_2.get_team_skills(team_2.guid).values()
                if team_2_skills:
                    (_, _), (max_clout_2, max_conf_2) = Skill.team_clout(team_2_skills)
                    message += Skill.make_message_clout(max_clout_2, max_conf_2, truncate(team_2.name.value, 25, "…")) + '\n'
                else:
                    max_conf_2 = 0

                if team_1_skills and team_2_skills:
                    if max_conf_1 > 2 and max_conf_2 > 2:
                        favouring_team_1, favouring_team_2 = Skill.calculate_quality_of_game_teams(team_1_skills, team_2_skills)
                        if favouring_team_1 != favouring_team_2:
                            message += "Hmm, it'll depend on who's playing, but... "
                        message += Skill.make_message_fairness(favouring_team_1) + '\n'
                        favouring_team_1, favouring_team_2 = Skill.calculate_win_probability(team_1_skills, team_2_skills)
                        message += Skill.make_message_win(favouring_team_1, favouring_team_2, team_1, team_2) + '\n'

                else:
                    message += "Hmm, I don't have any skill information to make a good guess on the outcome.\n"

            elif matching_mode == 'players':
                p1 = response_1.matched_players[0]
                message += Skill.make_message_clout(p1.skill.clout, p1.skill.confidence, truncate(p1.name.value, 25, "…")) + '\n'
                p2 = response_2.matched_players[0]
                message += Skill.make_message_clout(p2.skill.clout, p2.skill.confidence, truncate(p2.name.value, 25, "…")) + '\n'
                quality = Skill.calculate_quality_of_game_players(p1.skill, p2.skill)
                message += Skill.make_message_fairness(quality) + '\n'
            else:
                message += f"WTF IS {matching_mode}?!"

            await ctx.send(message)

    async def receive_slapp_response(self, success_message: str, response: dict):
        global slapp_started, slapp_caching_finished

        if success_message == "Caching task done.":
            slapp_caching_finished = True
            logging.info(f"ACK caching done.")
            return
        elif success_message.startswith('Connection established.'):
            if self.restart_context:
                logging.info(f"Slapp connection re-established. {success_message=}, {response=}.")
                await self.restart_context.add_reaction(TICK)
                self.restart_context = None
            else:
                logging.info(f"Slapp connection established. {success_message=}.")

            while len(slapp_ctx_queue):
                ctx, description = slapp_ctx_queue.popleft()
                if isinstance(ctx, Context):
                    await ctx.message.add_reaction(CROSS)

            if "0 players and 0 teams loaded" in success_message:
                logging.error("Slapp did not load its database correctly.")
                await self._restart_slapp(None)
            else:
                slapp_started = True
        elif not slapp_started:
            logging.error(f"Slapp is out-of-sync! Received unexpected message without a connection established message."
                          f" Discarding result. {success_message=}, {response=}")
            await self._restart_slapp(None)
        elif len(slapp_ctx_queue) == 0:
            logging.warning(f"receive_slapp_response but queue is empty. Discarding result: {success_message=}, {response=}")
        else:
            send_tick = False
            ctx, description = slapp_ctx_queue.popleft()

            if isinstance(ctx, Context):
                await ctx.message.add_reaction(TYPING)
                await asyncio.sleep(0.001)  # 1ms yield

            if description.startswith('predict_'):
                if success_message != "OK":
                    await SlappCommands.send_slapp(
                        ctx=ctx,
                        success_message=success_message,
                        response=SlappResponseObject(response))
                else:
                    await SlappCommands.handle_predict(ctx, description, response)
                send_tick = True
            elif description.startswith('autoseed'):
                if success_message != "OK":
                    await SlappCommands.send_slapp(
                        ctx=ctx,
                        success_message=success_message,
                        response=SlappResponseObject(response))

                # If the start, send on and read again.
                if description.startswith("autoseed_start"):
                    await SlappCommands.handle_autoseed(None, description, None)
                    ctx, description = slapp_ctx_queue.popleft()

                await SlappCommands.handle_autoseed(ctx, description, response)

                # Check if last.
                ctx, description = slapp_ctx_queue[0]
                if description.startswith("autoseed_end"):
                    await SlappCommands.handle_autoseed(ctx, description, None)
                    slapp_ctx_queue.popleft()
                    send_tick = True
            elif description.startswith('html'):
                if success_message != "OK":
                    await SlappCommands.send_slapp(
                        ctx=ctx,
                        success_message=success_message,
                        response=SlappResponseObject(response))

                # If the start, send on and read again.
                if description.startswith("html_start"):
                    await handle_html(None, description, None)
                    ctx, description = slapp_ctx_queue.popleft()

                await handle_html(ctx, description, response)

                # Check if last.
                ctx, description = slapp_ctx_queue[0]
                if description.startswith("html_end"):
                    await handle_html(ctx, description, None)
                    slapp_ctx_queue.popleft()
                    send_tick = True

            else:
                await SlappCommands.send_slapp(
                    ctx=ctx,
                    success_message=success_message,
                    response=SlappResponseObject(response))
                send_tick = True

            if isinstance(ctx, Context) and send_tick:
                await ctx.message.add_reaction(TICK)
                await asyncio.sleep(0.001)  # 1ms yield

    @staticmethod
    def get_latest_ipl():
        return get_tournament_ids('inkling-performance-labs')[0]

    async def _restart_slapp(self, ctx: Optional[Context]):
        logging.warning("Restarting Slapp...")
        self.slapp_started = False
        self.restart_context = ctx
        self.slappipe.kill_slapp()  # We started Slapp with keepOpen so this will restart
        await asyncio.sleep(0.001)  # 1ms yield  # yield/wait for a bit
        logging.info("..._restart_slapp continuing")

    async def _patch_slapp(self, ctx: Optional[Context], urls):
        if urls:
            urls = urls.split(' ')
        await self.slappipe.patch_slapp(urls)
        await ctx.message.add_reaction(TICK)

    async def begin_slapp_html(self, ctx, tournament: List[dict]):
        verification_message, players_to_queue = SlappCommands.prepare_bulk_slapp(tournament)

        # Do the autoseed list
        await add_to_queue(None, 'html_start')
        for pair in players_to_queue:
            await add_to_queue(None, 'html:' + pair[0])
            await self.slappipe.query_slapp(pair[1])
        await add_to_queue(ctx, 'html_end')

        if verification_message:
            await ctx.send(verification_message)

        # Finished in handle_html


async def process_slapp(r: SlappResponseObject) -> ProcessedSlappObject:
    if r.has_matched_players and r.has_matched_teams:
        title = f"Found {r.matched_players_len} player{('' if (r.matched_players_len == 1) else 's')} " \
                f"and {r.matched_teams_len} team{('' if (r.matched_teams_len == 1) else 's')}!"
        colour = Color.green()
    elif r.has_matched_players and not r.has_matched_teams:
        title = f"Found {r.matched_players_len} player{('' if (r.matched_players_len == 1) else 's')}!"
        colour = Color.blue()
    elif not r.has_matched_players and r.has_matched_teams:
        title = f"Found {r.matched_teams_len} team{('' if (r.matched_teams_len == 1) else 's')}!"
        colour = Color.gold()
    else:
        title = f"Didn't find anything 😔"
        colour = Color.red()

    builder = to_embed('', colour=colour, title=title)
    embed_colour = colour
    reacts: Dict[str, Union[Player, Team]] = dict()

    if r.has_matched_players:
        for i in range(0, MAX_RESULTS):
            if i >= r.matched_players_len:
                break

            p = r.matched_players[i]

            # Transform names by adding a backslash to any backslashes.
            names = list(set([escape_characters(name.value) for name in p.names if name and name.value]))
            current_name = f"{names[0]}" if len(names) else "(Unnamed Player)"
            resolved_teams = r.get_teams_for_player(p)

            current_team = None
            if r.is_single_player and resolved_teams:
                emoji_num = add_to_reacts_dict(reacts, resolved_teams[0])
                if emoji_num:
                    current_team = f'Plays for:\n{emoji_num} {wrap_in_backticks(resolved_teams[0].__str__())}\n'

            if not current_team:
                current_team = f'Plays for: {wrap_in_backticks(resolved_teams[0].__str__())}\n' if resolved_teams else ''

            if len(resolved_teams) > 1:
                old_teams = 'Old teams: \n'
                resolved_old_teams = resolved_teams[1:]

                # Add reacts if for a single player entry
                if r.is_single_player:
                    for n, old_t in enumerate(resolved_old_teams):
                        emoji_num = add_to_reacts_dict(reacts, old_t)
                        if emoji_num:
                            old_teams += f"{emoji_num} {wrap_in_backticks(old_t.__str__())}\n"
                        else:
                            old_teams += f"{wrap_in_backticks(old_t.__str__())}\n"
                else:
                    old_teams += join("\n", [wrap_in_backticks(old_t.__str__()) for old_t in resolved_old_teams])

                old_teams = close_backticks_if_unclosed(truncate(old_teams, 1000, "…\n")) + "\n"
            else:
                old_teams = ''

            if len(names) > 1:
                other_names = truncate("_ᴬᴷᴬ_ ```" + '\n'.join(names[1:]) + "```\n", 1000, "…\n```\n")
            else:
                other_names = ''

            battlefy = ''
            for battlefy_profile in p.battlefy.slugs:
                battlefy += f'{emojis.BATTLEFY} [{escape_characters(battlefy_profile.value)}]' \
                            f'({battlefy_profile.uri})\n'

            discord = ''
            for discord_profile in p.discord.ids:
                did = escape_characters(discord_profile.value)
                discord += f'{emojis.DISCORD} [{did}]' \
                           f'(https://discord.id/?prefill={did}) \n🦑 [Sendou](https://sendou.ink/u/{did})\n'

            twitch = ''
            for twitch_profile in p.twitch_profiles:
                twitch += f'{emojis.TWITCH} [{escape_characters(twitch_profile.value)}]' \
                            f'({twitch_profile.uri})\n'

            twitter = ''
            for twitter_profile in p.twitter_profiles:
                twitter += f'{emojis.TWITTER} [{escape_characters(twitter_profile.value)}]' \
                            f'({twitter_profile.uri})\n'

            country_flag = p.country_flag + ' ' if p.country_flag else ''
            top500 = (TOP_500 + " ") if p.top500 else ''
            current_name = safe_backticks(current_name)
            field_head = truncate(country_flag + top500 + current_name, 256) or ' '

            notable_results = r.get_first_placements(p)
            notable_results.extend(p.plus_membership)
            won_low_ink = r.placement_is_winning_low_ink(r.best_low_ink_placement(p))
            player_sources: List[SimpleSource] = r.get_simple_sources(p)

            # Single player detailed view --
            # If there's just the one matched player, move the extras to another field.
            if r.matched_players_len == 1 and r.matched_teams_len < 14:
                field_body = f'{other_names}'
                builder.add_field(name=field_head,
                                  value=truncate(field_body, 1023, "…") or "(No other names)",
                                  inline=False)

                builder.add_field(name='FCs:',
                                  value=f"{len(p.friend_codes)} known friend code(s)",
                                  inline=False)

                if current_team or old_teams:
                    field_body = f'{current_team}{old_teams}'
                    builder.add_field(name='Teams:',
                                      value=truncate(field_body, 1023, "…") or "(Nothing else to say)",
                                      inline=False)

                if twitch or twitter or battlefy or discord:
                    field_body = f'{twitch}{twitter}{battlefy}{discord}'
                    builder.add_field(name='Socials:',
                                      value=truncate(field_body, 1023, "…") or "(Nothing else to say)",
                                      inline=False)

                if len(notable_results):
                    notable_results_str = ''
                    if won_low_ink:
                        notable_results_str += f"{LOW_INK} Low Ink Winner\n"

                    for win in notable_results:
                        notable_results_str += f"{TROPHY} Won {win}\n"

                    builder.add_field(name='Notable Wins:',
                                      value=truncate(notable_results_str, 1023, "…"),
                                      inline=False)

                if len(p.weapons):
                    builder.add_field(name='Weapons:',
                                      value=truncate(', '.join(p.weapons), 1023, "…"),
                                      inline=False)

                if not p.skill.is_default:
                    clout_message = p.skill.message
                    builder.add_field(name='Clout:',
                                      value=clout_message,
                                      inline=False)

                if len(player_sources):
                    batched_player_sources = player_sources
                    for source_batch in range(0, 15):
                        sources_count = len(batched_player_sources)
                        value = ''
                        for j in range(0, min(sources_count, 6)):
                            value += batched_player_sources[j].get_linked_name_display() + '\n'

                        batched_player_sources = player_sources[min(sources_count, 7):]

                        no_more = len(batched_player_sources) <= 0
                        only_source = no_more and source_batch == 0
                        sources_text = f'Sources:' if only_source else f'Sources ({(source_batch + 1)}):'
                        builder.add_field(name=sources_text,
                                          value=truncate(value, 1023, "…"),
                                          inline=False)
                        if no_more:
                            break

            # Multiple players summary view --
            else:
                emoji_num = add_to_reacts_dict(reacts, p)
                additional_info = (
                    f"\n More info: React {emoji_num}\n"
                    if emoji_num
                    else f"\n More info: {COMMAND_PREFIX}full {p.guid}\n")

                notable_results_str = ''
                if len(notable_results):
                    if won_low_ink:
                        notable_results_str += f"{LOW_INK} Low Ink Winner\n"
                    for win in notable_results:
                        notable_results_str += f"{TROPHY} Won {win}\n"

                sources_field: str = "Sources:\n" + "\n".join(r.get_grouped_sources_text(p))
                fcs_str = (len(p.friend_codes).__str__() + " known friend codes\n" if len(p.friend_codes) > 1
                           else "1 known friend code\n" if len(p.friend_codes) == 1
                           else "")
                field_body = (f'{other_names}{current_team}{old_teams}{fcs_str}'
                              f'{twitch}{twitter}{battlefy}{discord}'
                              f'{notable_results_str}') or "(Nothing else to say)"

                if len(field_body) + len(sources_field) + len(additional_info) < 1024:
                    field_body += sources_field
                else:
                    # If we're running over, use the truncated sources instead.
                    field_body += "Sources:\n" + "\n".join([s.truncated_name for s in player_sources])
                    field_body = truncate(field_body, 1020 - len(additional_info), indicator="…")
                    field_body = close_backticks_if_unclosed(field_body)
                field_body += additional_info

                builder.add_field(name=field_head, value=field_body, inline=False)
                await asyncio.sleep(0.001)  # 1ms yield

    if r.has_matched_teams:
        separator = ',\n' if r.matched_teams_len == 1 else ', '

        for i in range(0, MAX_RESULTS):
            if i >= r.matched_teams_len:
                break

            t = r.matched_teams[i]
            players = r.matched_players_for_teams[t.guid.__str__()]
            players_in_team: List[Player] = []
            players_objs: List[Player] = []
            player_strings = []
            for player_tuple in players:
                if player_tuple:
                    p = player_tuple["Item1"]
                    in_team = player_tuple["Item2"]
                    name = p.name.value
                    name = safe_backticks(name)
                    aka = f"_ᴬᴷᴬ_ {truncate(', '.join([truncate(safe_backticks(alt.value), 16, '…') for alt in p.names[1:]]), 198, '…')} " if len(p.names) > 1 else ""
                    player_strings.append(f'{name} {aka}{("(Most recent)" if in_team else "(Ex)" if in_team is False else "")}')
                    players_objs.append(p)
                    if in_team:
                        players_in_team.append(p)

            div_phrase = best_team_player_div_string(t, players, r.known_teams)
            if div_phrase:
                div_phrase += '\n'

            # Single team detailed view --
            # If there's just the one matched team, move the sources to the next field.
            if r.matched_teams_len == 1:
                # Show the team's alt names, if any
                if len(t.names) > 1:
                    builder.add_field(name='Other names:',
                                      value=", ".join([safe_backticks(name.value) for name in t.names]),
                                      inline=False)

                # Show the team's tags
                if len(t.clan_tags) > 0:
                    builder.add_field(name='Tags:',
                                      value=", ".join([safe_backticks(tag.value) for tag in t.clan_tags]),
                                      inline=False)

                # Add in emoji reacts
                for j, p_str in enumerate(player_strings):
                    emoji_num = add_to_reacts_dict(reacts, players_objs[j])
                    if emoji_num:
                        player_strings[j] = emoji_num + " " + p_str

                info = f'{div_phrase}Players:\n{separator.join(player_strings)}'
                builder.add_field(name=truncate(t.__str__(), 256, "") or "Unnamed Team",
                                  value=truncate(info, 1023, "…_"),
                                  inline=False)

                player_skills = [player.skill for player in players_in_team]
                (min_clout, min_conf), (max_clout, max_conf) = Skill.team_clout(player_skills)

                if min_conf > 1:  # 1%
                    if min_clout == max_clout:
                        clout_message = f"I rate the current team's clout at {min_clout} ({min_conf}% sure)"
                    else:
                        clout_message = f"I rate the current team's clout between {min_clout} ({min_conf}% sure) " \
                                        f"and {max_clout} ({max_conf}% sure)"

                    builder.add_field(name='Clout:',
                                      value=clout_message,
                                      inline=False)

                player_skills = [(player, player.skill.clout) for player in players_in_team]
                if player_skills:
                    best_player = max(player_skills, key=itemgetter(1))[0]
                    if not best_player.skill.is_default:
                        builder.add_field(name='Best player in the team by clout:',
                                          value=truncate(best_player.name.value, 500, "…") + ": " + best_player.skill.message,
                                          inline=False)

                builder.add_field(name='Sources:',
                                  value=truncate('_' + '\n'.join(r.get_grouped_sources_text(t)) + '_', 1023, "…_"),
                                  inline=False)

                builder.add_field(name='Slapp Id:',
                                  value=t.guid.__str__(),
                                  inline=False)

            # Multiple teams summary view --
            else:
                emoji_num = add_to_reacts_dict(reacts, t)
                additional_info = (
                    f"\n React {emoji_num} for more\n"
                    if emoji_num
                    else f"\n More info: {COMMAND_PREFIX}full {t.guid}\n")

                field_body = f'{div_phrase}Players: {player_strings}\n' \
                             f'_{r.get_grouped_sources_text(t)}_' or "(Nothing else to say)"

                if len(field_body) + len(additional_info) < 1024:
                    field_body += additional_info
                else:
                    field_body = truncate(field_body, 1020 - len(additional_info), indicator="…")
                    field_body = close_backticks_if_unclosed(field_body)
                    field_body += additional_info

                builder.add_field(name=truncate(t.__str__(), 256, "") or "Unnamed Team",
                                  value=truncate(field_body, 1023, "…_"),
                                  inline=False)
                await asyncio.sleep(0.001)  # 1ms yield

    builder.set_footer(
        text=get_random_footer_phrase() + (
            f'Only the first {MAX_RESULTS} results are shown for players and teams.' if r.show_limited else ''
        ),
        icon_url="https://media.discordapp.net/attachments/471361750986522647/758104388824072253/icon.png")
    await asyncio.sleep(0.001)  # 1ms yield
    return ProcessedSlappObject(builder, embed_colour, reacts)


def add_to_reacts_dict(reacts, player_or_team: Union[Player, Team]) -> Optional[str]:
    """
    Adds the player or team to the reacts dictionary. Returns the reaction that represents the addition, or None
    if there are no more reactions left in the NUMBERS_KEY_CAPS collection.
    """
    if len(reacts) < len(NUMBERS_KEY_CAPS):
        emoji_num = NUMBERS_KEY_CAPS[len(reacts)]
        reacts[emoji_num] = player_or_team
        return emoji_num
    else:
        return None


def best_team_player_div_string(
        team: Team,
        players_for_team: List[Dict[str, Union[dict, object, bool]]],
        known_teams: Dict[str, Team]):
    if not players_for_team or not known_teams:
        return ''

    highest_div: Division = team.get_best_div()
    highest_team: Team = team
    best_player: Optional[Player] = None
    for player_tuple in players_for_team:
        if player_tuple:
            in_team = player_tuple["Item2"] if "Item2" in player_tuple else False
            p: Union[dict, Player] = player_tuple["Item1"] if "Item1" in player_tuple else None
            if p is None:
                continue
            elif isinstance(p, dict):
                p: Player = Player.from_dict(p)
            elif isinstance(p, Player):
                pass
            else:
                assert False, f"Unknown Player object {p}"

            if in_team and len(p.teams) > 0:
                for team_id in p.teams:
                    player_team = known_teams[team_id.__str__()] if known_teams and team_id in known_teams else None
                    if (player_team is not None) \
                            and (not player_team.current_div.is_unknown) \
                            and (highest_div.is_unknown or (player_team.current_div < highest_div)):
                        highest_div = player_team.current_div
                        highest_team = player_team
                        best_player = p

    if highest_div.is_unknown or team.current_div.is_unknown or best_player is None:
        return ''
    elif highest_div == team.current_div:
        return 'No higher div players.'
    else:
        name: str = best_player.name.value
        return f"Highest div player is ``{name}`` who plays for {highest_team.name} ({highest_div})."


def add_to_reacts_buffer(message_id: str, reacts: Dict[str, Union[Player, Team]]):
    slapp_reacts_queue[message_id] = reacts
    if len(slapp_reacts_queue) > NUMBERS_KEY_CAPS_LEN:  # always ensure we have room for the last message.
        slapp_reacts_queue.popitem(last=False)
