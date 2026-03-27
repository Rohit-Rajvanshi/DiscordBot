from discord.ext import commands
from discord import app_commands
import discord 



class TTTView(discord.ui.View):
    def __init__(self , player_X , player_O):

        super().__init__()
        self.player_X = player_X
        self.player_O = player_O
        for i in range(9):
            self.add_item(TTTButton(i))
        self.player_list = [(player_X , "❌") , (player_O , "⭕")]
        self.current_player = self.player_list[0][0]
        self.current_symbol = self.player_list[0][1]
        self.board = ["⬜" for i in range (9)]

    

class TTTButton(discord.ui.Button):
    def __init__(self, index):
        super().__init__(label = "⬜" , style = discord.ButtonStyle.gray , row = index//3)
        self.index = index
    
    async def callback(self, interaction : discord.Interaction):
        view = self.view

        if interaction.user != view.current_player:
            await interaction.response.defer()
            await interaction.followup.send("Not ur turn", ephemeral=True)
            return 
        
        if view.board[self.index] != "⬜":
            await interaction.response.send_message("Already occupied" , ephemeral=True)
            return 
        
        self.label = view.current_symbol
        view.board[self.index] = self.label
        self.disabled = True

        winning_condition_list = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

        for win_list in winning_condition_list:
            win = False
            for idx in win_list:
                if view.board[idx] == view.current_symbol:
                    win = True
                else:
                    win = False
                    break
            if win == True:
                for button in view.children:
                    button.disabled = True
                await interaction.response.edit_message(content = f"{interaction.user.mention} Wins!" , view = view)
                return 
        
                

        if "⬜" not in view.board:
            for button in view.children:
                button.disabled = True
            await interaction.response.edit_message(content = "Draw" , view = view)
            return 

        
        view.player_list[0] , view.player_list[1] = view.player_list[1] , view.player_list[0]
        view.current_player = view.player_list[0][0]
        view.current_symbol = view.player_list[0][1]
        
       

        await interaction.response.edit_message(view = view)





class ButtonCommands(commands.Cog):
    def __init__(self , bot):
        self.bot = bot

    @app_commands.command(name="ttt")
    @app_commands.guilds(discord.Object(id=1104576336690937928))
    async def ttt(self , interaction : discord.Interaction , opponent : discord.Member):
        try:
            player_X = interaction.user
            player_O = opponent
            await interaction.response.send_message(content = f"**Tic Tac Toe started!** {interaction.user.mention} V/S {opponent.mention}" ,view=TTTView(player_X , player_O))
        
        except Exception as e:
            print("ERROR:", e)
            await interaction.response.send_message("Error occurred", ephemeral=True)

    
async def setup(bot):
    await bot.add_cog(ButtonCommands(bot))
    




    
