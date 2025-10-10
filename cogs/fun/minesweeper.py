import random
from itertools import repeat
import discord
from discord.ext import commands
import asyncio
import time

class RowButton(discord.ui.Button):
    def __init__(self, ctx, label, custom_id, bombs, board):
        super().__init__(label=label, style=discord.ButtonStyle.grey, custom_id=custom_id)
        self.ctx = ctx
        self.bombs = bombs
        self.board = board

    async def callback(self, interaction):
        assert self.view is not None
        view: MsView = self.view
        
        current_time = time.time()
        if current_time - view.last_interaction < 0.5:
            try:
                return await interaction.response.send_message("Please wait before clicking again.", ephemeral=True)
            except:
                return
        
        view.last_interaction = current_time
        
        try:
            await interaction.response.defer()
        except discord.errors.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(1)
                return
            raise
        
        if interaction.user.id != self.ctx.author.id:
            return await interaction.followup.send(
                "You cannot interact with these buttons.", ephemeral=True
            )

        b_id = self.custom_id
        if int(b_id[5:]) in view.moves:
            return await interaction.followup.send("That part is already taken.", ephemeral=True)
        if int(b_id[5:]) in self.bombs:
            await view.RevealBombs(b_id, view.board)
        else:
            count = []
            rawpos = int(b_id[5:])
            pos = view.GetBoardPos(rawpos)

            def checkpos(count, rawpos, pos):
                pos = view.GetBoardPos(rawpos)
                if not rawpos - 1 in self.bombs or pos == 0:
                    count.append(rawpos - 1)
                if not rawpos + 1 in self.bombs or pos == 4:
                    count.append(rawpos + 1)
                if not rawpos - 6 in self.bombs or pos == 0:
                    count.append(rawpos - 6)
                if not rawpos - 4 in self.bombs or pos == 4:
                    count.append(rawpos - 4)
                if not rawpos + 6 in self.bombs or pos == 4:
                    count.append(rawpos + 6)
                if not rawpos + 4 in self.bombs or pos == 0:
                    count.append(rawpos + 4)
                if not rawpos - 5 in self.bombs:
                    count.append(rawpos - 5)
                if not rawpos + 5 in self.bombs:
                    count.append(rawpos + 5)
                return count

            count = checkpos(count, rawpos, pos)
            number = 8-len(count)
            self.label = str(number) if number > 0 else "0"
            self.style = discord.ButtonStyle.green
            pos = int(b_id[5:])
            view.board[view.GetBoardRow(pos)][
                view.GetBoardPos(pos)
            ] = str(number) if number > 0 else "0"
            view.moves.append(pos)
            if len(view.moves) + len(self.bombs) == 25:
                await view.EndGame()
            else:
                try:
                    await interaction.edit_original_response(view=view)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(1)
                    else:
                        raise

class MsView(discord.ui.View):
    def __init__(self, ctx, options, bombs, board):
        super().__init__(timeout=300)
        for i, op in enumerate(options):
            self.add_item(RowButton(ctx, op, f"block{i}", bombs, board))
        self.board = board
        self.bombs = bombs
        self.moves = []
        self.ctx = ctx
        self.message = None
        self.last_interaction = 0
    
    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        embed = discord.Embed(
            title="Minesweeper", 
            description="Game timed out!", 
            color=0xFF0000
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        try:
            await self.message.edit(embed=embed, view=self)
        except:
            pass

    async def EndGame(self):
        for button in self.children:
            button.disabled = True
            pos = int(button.custom_id[5:])
            if pos in self.bombs:
                button.label = "💣"
                button.style = discord.ButtonStyle.red
                self.board[self.GetBoardRow(pos)][self.GetBoardPos(pos)] = "💣"
        
        embed = discord.Embed(
            title="Minesweeper",
            description="Game Ended. You won!",
            color=0x00FF00
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        
        try:
            await self.message.edit(embed=embed, view=self)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(1)
            else:
                raise
        self.stop()

    def GetBoardRow(self, pos):
        if pos in [0, 1, 2, 3, 4]:
            return 0
        if pos in [5, 6, 7, 8, 9]:
            return 1
        if pos in [10, 11, 12, 13, 14]:
            return 2
        if pos in [15, 16, 17, 18, 19]:
            return 3
        if pos in [20, 21, 22, 23, 24]:
            return 4
        return False

    def GetBoardPos(self, pos):
        if pos in [0, 1, 2, 3, 4]:
            return pos
        if pos in [5, 6, 7, 8, 9]:
            for i, num in enumerate(range(5, 10)):
                if pos == num:
                    return i
        if pos in [10, 11, 12, 13, 14]:
            for i, num in enumerate(range(10, 15)):
                if pos == num:
                    return i
        if pos in [15, 16, 17, 18, 19]:
            for i, num in enumerate(range(15, 20)):
                if pos == num:
                    return i
        if pos in [20, 21, 22, 23, 24]:
            for i, num in enumerate(range(20, 25)):
                if pos == num:
                    return i
        return False

    async def RevealBombs(self, b_id, board):
        bombemo = "💣"
        
        for button in self.children:
            button.disabled = True
            if button.custom_id == b_id:
                button.label = bombemo
                button.style = discord.ButtonStyle.red
                pos = int(b_id[5:])
                self.board[self.GetBoardRow(pos)][self.GetBoardPos(pos)] = bombemo

        for button in self.children:
            if int(button.custom_id[5:]) in self.bombs:
                button.label = bombemo
                button.style = discord.ButtonStyle.red
                pos = int(button.custom_id[5:])
                self.board[self.GetBoardRow(pos)][
                    self.GetBoardPos(pos)
                ] = bombemo
        
        embed = discord.Embed(
            title="Minesweeper",
            description=f"💥 BOOM! You hit a bomb. Game Over!\n-# gg {self.ctx.author.mention}",
            color=0xE02B2B
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        
        try:
            await self.message.edit(embed=embed, view=self)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(1)
            else:
                raise
        self.stop()

def minesweeper_command():
    @commands.hybrid_command(
        name="minesweeper", 
        description="Play a buttoned minesweeper mini-game."
    )
    async def minesweeper(self, context):
        board = [["឵឵ "] * 5 for _ in range(5)]
        bombs = 0
        bombpositions = []
        for x in repeat(None, random.randint(4, 11)):
            random_index = random.randint(0, 24)
            if random_index not in bombpositions and random_index not in [
                0, 4, 20, 24
            ]:
                bombpositions.append(random_index)
                bombs += 1

        def ExtractBlocks():
            new_b = []
            for x in board:
                for y in x:
                    new_b.append(y)
            return new_b

        embed = discord.Embed(
            title="Minesweeper",
            description=f"💣 Total Bombs: `{len(bombpositions)}`\n\nClick the buttons to reveal the grid. Avoid the bombs!",
            color=0x7289DA
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        
        view = MsView(context, ExtractBlocks(), bombpositions, board)
        message = await context.send(embed=embed, view=view)
        view.message = message
    
    return minesweeper
