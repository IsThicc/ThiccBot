#
#                            ThiccBot Github.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import aiohttp, config, github
from discord import Embed as em, Colour
from typing import List, Dict
from datetime import datetime, timedelta
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github = github.Github(config.github_access)

        self.repo_cache = None
        self.repo_cache_time = None
        self.full_repo_cache = None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def _get_isthicc_repos(self, public: bool = True) -> List[github.Repository.Repository]:
        async def update_caches():
            self.repo_cache = []
            self.full_repo_cache = {}
            for repo in self.github.get_organization("IsThicc") \
                            .get_repos(type=("public" if public else "all")):
                self.repo_cache.append(repo)
                self.full_repo_cache[repo] = {}

        now = datetime.now()
        if self.repo_cache_time is not None:
            if (self.repo_cache_time + timedelta(minutes=10)) <= now:
                self.repo_cache_time = now
                await update_caches()
                return self.repo_cache

            elif self.repo_cache is None:
                await update_caches()
                return self.repo_cache  # noqa - self.repo_cache is updated in update_caches
            return self.repo_cache

        await update_caches()
        self.repo_cache_time = now
        return self.repo_cache

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def _get_prs(self, public: bool = True) -> \
            Dict[github.Repository.Repository, List[github.PullRequest.PullRequest]]:
        repos = await self._get_isthicc_repos(public=public)
        return_dict = {}
        for repo in repos:
            repo_cache = self.full_repo_cache.get(repo, {})
            rc_pulls = repo_cache.get('pulls')
            if rc_pulls is None:
                pulls = repo.get_pulls(state="open")
                if pulls.totalCount == 0:
                    rc_pulls = []

                else:
                    rc_pulls = [pull for pull in pulls]
                    return_dict[repo] = rc_pulls
                repo_cache['pulls'] = rc_pulls

            self.full_repo_cache[repo] = repo_cache
        return return_dict

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def send_prs(self, ctx, prs, public: bool = True):
        status = ('Public' if public else 'Private/Public')
        if len(prs) == 0:
            return await ctx.send(embed=em(
                title=f"No {status} Pull Requests are open in the IsThicc Organization!",
                colour=Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                text="IsThicc GitHub",
                icon_url=self.bot.user.avatar_url
            ))

        embed = em(
            title="Open Pull Requests in the IsThicc Organization!",
            description=f"Showing {status} pull requests!",
            timestamp=datetime.utcnow(),
            colour=Colour.red()
        ).set_footer(
            text="IsThicc GitHub",
            icon_url=self.bot.user.avatar_url
        )
        shown_prs = 0
        prs_not_shown = 0
        for repo, pulls in prs.items():
            for pull in pulls:
                if shown_prs >= 24:
                    prs_not_shown += 1
                    continue
                shown_prs += 1

                embed.add_field(
                    name=f"{repo.name} - #{pull.number}",
                    value=f"URL: [{pull.title}]({pull.html_url})"
                )

        if prs_not_shown:
            embed.add_field(
                name=f"{prs_not_shown} Pull Requests are not shown!",
                value="Find more information about them on [our GitHub](https://github.com/IsThicc)!"
            )
        await ctx.send(embed=embed)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.group(name="prs")
    async def prs(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.send_prs(ctx, (await self._get_prs(public=True)), True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @prs.command(name="private", aliases=["priv"])
    @commands.has_role(config.admin_role)
    async def private_prs(self, ctx):
        await self.send_prs(ctx, (await self._get_prs(public=False)), False)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(GitHub(bot))
