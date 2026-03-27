
import discord
from discord.ext import commands 
from google import genai


class KuroAI:

    def __init__(self , API_KEY):
        self.client = genai.Client(api_key = API_KEY)

    async def ask(self , prompt):
        try:
            p_text = f"You are Kuro, a helpful discord bot, give greetings , be very genz coded and have a dark humor.\n User : {prompt}"
            response = self.client.models.generate_content(model='gemini-2.5-flash' , contents  = p_text)
            text = response.text
        
            if len(text) > 4000:
                text = text[:4000]

            embed = discord.Embed(
                title = "KuroAI",
                description= f"User Prompt: {prompt} \n\n {text}",
                color = discord.Color.blue()
            )

            return embed 
        
        except Exception as e:
            return discord.Embed(
                title = "Error" ,
                description= "Something went wrong",
                color = discord.Color.red()
            )
         
