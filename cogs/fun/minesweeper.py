import random
from itertools import repeat
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import time

class RowButton(discord.ui.Button):
    def __init__(self, ctx, label, custom_id, bombs, board, opponent=None):
        super().__init__(label=label, style=discord.ButtonStyle.grey, custom_id=custom_id)
        self.ctx = ctx
        self.bombs = bombs
        self.board = board
        self.opponent = opponent

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
        
        if view.opponent:
            if interaction.user.id not in [self.ctx.author.id, view.opponent.id]:
                return await interaction.followup.send(
                    "You cannot interact with these buttons.", ephemeral=True
                )
            if interaction.user.id != view.current_player.id:
                return await interaction.followup.send(
                    f"It's {view.current_player.mention}'s turn!", ephemeral=True
                )
        else:
            if interaction.user.id != self.ctx.author.id:
                return await interaction.followup.send(
                    "You cannot interact with these buttons.", ephemeral=True
                )

        b_id = self.custom_id
        if int(b_id[5:]) in view.moves:
            return await interaction.followup.send("That part is already taken.", ephemeral=True)
        
        if not view.bombs_generated:
            view.generate_bombs(int(b_id[5:]))
            self.bombs = view.bombs
        
        if int(b_id[5:]) in self.bombs:
            await view.RevealBombs(b_id, view.board, interaction)
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
            
            if view.opponent:
                if interaction.user.id == view.ctx.author.id:
                    view.player1_score += 1
                else:
                    view.player2_score += 1
            
            if number == 0:
                await view.auto_reveal_safe_squares(rawpos, interaction)
            
            if view.opponent:
                view.current_player = view.opponent if view.current_player.id == view.ctx.author.id else view.ctx.author
            
            if len(view.moves) + len(self.bombs) == 25:
                await view.EndGame()
            else:
                try:
                    await view.update_embed(interaction)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(1)
                    else:
                        raise

class MsView(discord.ui.View):
    def __init__(self, ctx, options, bomb_count, board, opponent=None):
        super().__init__(timeout=300)
        for i, op in enumerate(options):
            self.add_item(RowButton(ctx, op, f"block{i}", [], board, opponent))
        self.board = board
        self.bombs = []
        self.bomb_count = bomb_count
        self.bombs_generated = False
        self.moves = []
        self.ctx = ctx
        self.message = None
        self.last_interaction = 0
        self.opponent = opponent
        self.current_player = ctx.author
        self.player1_score = 0
        self.player2_score = 0
    
    def generate_bombs(self, first_move_pos):
        bombpositions = []
        excluded_positions = [0, 4, 20, 24, first_move_pos] 
        
        while len(bombpositions) < self.bomb_count:
            random_index = random.randint(0, 24)
            if random_index not in bombpositions and random_index not in excluded_positions:
                bombpositions.append(random_index)
        
        self.bombs = bombpositions
        self.bombs_generated = True
        

        for button in self.children:
            if isinstance(button, RowButton):
                button.bombs = self.bombs
    
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
        
        if self.opponent:
            if self.player1_score > self.player2_score:
                winner = self.ctx.author
            elif self.player2_score > self.player1_score:
                winner = self.opponent
            else:
                winner = None
            
            if winner:
                description = f"🎉 **{winner.mention}** won!"
            else:
                description = f"🤝 It's a tie!"
        else:
            description = "Game Ended. You won!"
        
        embed = discord.Embed(
            title="Minesweeper",
            description=description,
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

    async def update_embed(self, interaction):
        if self.opponent:
            embed = discord.Embed(
                title="Minesweeper - Multiplayer",
                description=f"💣 Total Bombs: `{self.bomb_count}`\n\n🎮 **Players:**\n{self.ctx.author.mention} vs {self.opponent.mention}\n\n**Current Turn:** {self.current_player.mention}",
                color=0x7289DA
            )
            embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        else:
            embed = discord.Embed(
                title="Minesweeper",
                description=f"💣 Total Bombs: `{self.bomb_count}`\n\nClick the buttons to reveal the grid. Avoid the bombs!",
                color=0x7289DA
            )
            embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        
        await interaction.edit_original_response(embed=embed, view=self)

    async def auto_reveal_safe_squares(self, center_pos, interaction):
        positions_to_check = [center_pos]
        revealed_positions = set()
        current_player_id = interaction.user.id
        
        while positions_to_check:
            current_pos = positions_to_check.pop(0)
            if current_pos in revealed_positions:
                continue
                
            revealed_positions.add(current_pos)
            
            adjacent_positions = []
            pos = self.GetBoardPos(current_pos)
            
            if pos > 0 and current_pos - 1 not in self.bombs:
                adjacent_positions.append(current_pos - 1)
            if pos < 4 and current_pos + 1 not in self.bombs:
                adjacent_positions.append(current_pos + 1)
            if current_pos >= 5 and current_pos - 5 not in self.bombs:
                adjacent_positions.append(current_pos - 5)
            if current_pos <= 19 and current_pos + 5 not in self.bombs:
                adjacent_positions.append(current_pos + 5)
            if pos > 0 and current_pos >= 5 and current_pos - 6 not in self.bombs:
                adjacent_positions.append(current_pos - 6)
            if pos < 4 and current_pos >= 5 and current_pos - 4 not in self.bombs:
                adjacent_positions.append(current_pos - 4)
            if pos > 0 and current_pos <= 19 and current_pos + 4 not in self.bombs:
                adjacent_positions.append(current_pos + 4)
            if pos < 4 and current_pos <= 19 and current_pos + 6 not in self.bombs:
                adjacent_positions.append(current_pos + 6)
            
            for adj_pos in adjacent_positions:
                if adj_pos not in self.moves and adj_pos not in revealed_positions:
                    adj_count = []
                    adj_pos_obj = self.GetBoardPos(adj_pos)
                    
                    def checkpos_adj(count, rawpos, pos):
                        pos = self.GetBoardPos(rawpos)
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
                    
                    adj_count = checkpos_adj(adj_count, adj_pos, adj_pos_obj)
                    adj_number = 8 - len(adj_count)
                    
                    for button in self.children:
                        if int(button.custom_id[5:]) == adj_pos:
                            button.label = str(adj_number) if adj_number > 0 else "0"
                            button.style = discord.ButtonStyle.green
                            break
                    
                    self.board[self.GetBoardRow(adj_pos)][self.GetBoardPos(adj_pos)] = str(adj_number) if adj_number > 0 else "0"
                    self.moves.append(adj_pos)
                    
                    if self.opponent:
                        if current_player_id == self.ctx.author.id:
                            self.player1_score += 1
                        else:
                            self.player2_score += 1
                    
                    if adj_number == 0:
                        positions_to_check.append(adj_pos)
        
        try:
            await self.update_embed(interaction)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(1)
            else:
                raise

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

    async def RevealBombs(self, b_id, board, interaction):
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
        
        if self.opponent:
            loser = self.ctx.author if interaction.user.id == self.ctx.author.id else self.opponent
            winner = self.opponent if loser.id == self.ctx.author.id else self.ctx.author
            description = f"💥 BOOM! {loser.mention} hit a bomb!\n🎉 **{winner.mention}** wins!"
        else:
            description = f"💥 BOOM! You hit a bomb. Game Over!\n-# gg {self.ctx.author.mention}"
        
        embed = discord.Embed(
            title="Minesweeper",
            description=description,
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
    @app_commands.describe(
        opponent="Optional user to play against in multiplayer mode."
    )
    async def minesweeper(self, context, opponent: discord.User = None):
        board = [["឵឵ "] * 5 for _ in range(5)]
        bomb_count = random.randint(4, 11)

        def ExtractBlocks():
            new_b = []
            for x in board:
                for y in x:
                    new_b.append(y)
            return new_b

        if opponent:
            if opponent.id == context.author.id:
                embed = discord.Embed(
                    title="Error!",
                    description="You cannot play against yourself!",
                    color=0xE02B2B
                )
                embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
                return await context.send(embed=embed, ephemeral=True)
            
            embed = discord.Embed(
                title="Minesweeper - Multiplayer",
                description=f"💣 Total Bombs: `{bomb_count}`\n\n🎮 **Players:**\n{context.author.mention} vs {opponent.mention}\n\n{context.author.mention} goes first! Click the buttons to reveal the grid. Avoid the bombs!",
                color=0x7289DA
            )
            embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        else:
            embed = discord.Embed(
                title="Minesweeper",
                description=f"💣 Total Bombs: `{bomb_count}`\n\nClick the buttons to reveal the grid. Avoid the bombs!",
                color=0x7289DA
            )
            embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        
        view = MsView(context, ExtractBlocks(), bomb_count, board, opponent)
        message = await context.send(embed=embed, view=view)
        view.message = message
    
    return minesweeper
