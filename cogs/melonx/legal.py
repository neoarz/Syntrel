import discord
from discord.ext import commands


def legal_command():
    @commands.hybrid_command(name="legal", description="Legality of emulators.")
    async def legal(self, context):
        embed = discord.Embed(
            color=0x963155,
            description=(
                "# Legality\n\n"
                + "---\n\n"
                + "## Overview\n"
                + "Emulators themselves are **legal**, as long as you use them with **legally dumped copies** of games **you** own, "
                + "or with **homebrew software**.\n\n"
                + "Read about the landmark case [**Sony v. Bleem!** (2000)](https://www.copyright.gov/fair-use/summaries/sonycomputer-bleem-9thcir2000.pdf), "
                + "which helped set the precedent for emulation being legal. You can also watch "
                + "[this video](https://www.youtube.com/watch?v=yj9Gk84jRiE) for more information.\n\n"
                "## Legal Basis\n"
                + "According to the [**U.S. Copyright Act**](https://www.copyright.gov/title17/92chap1.html#117) "
                + "(the law under which Discord operates), you **must own a legal copy** of any game you play on **MeloNX**.\n\n"
                + "- Downloading games you do not own is considered **piracy** and is **illegal**.\n"
                + "- Even if another copy is identical, it still belongs to someone else, you are **not entitled** to it.\n\n"
                + "## Our Stance on Piracy\n"
                + "We **do not support piracy**. Doing so would give Nintendo legal grounds to take us down.\n"
                + "And yes — **Nintendo is aware of MeloNX's existence.**\n\n"
                + "We are not required to monitor user behavior, but we **strongly encourage** everyone to use only **legally obtained copies** of games.\n\n"
                + "## Enforcement\n"
                + "If you are found using pirated games with MeloNX, you will be **banned** from this Discord server **without warning**.\n\n"
                + "## Final Note\n"
                + "Thank you for understanding and respecting the hard work that went into creating both the emulator MeloNX is built on, "
                + "and **MeloNX itself.**"
            ),
        )
        embed.set_author(
            name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
        )
        embed.set_footer(text="Last Edited by stossy11")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/melonx/legal.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="MeloNX Discord",
                style=discord.ButtonStyle.primary,
                url="https://discord.gg/EMXB2XYQgA",
                emoji="<:Discord:1428762057758474280>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return legal
