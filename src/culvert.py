import os
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Ensure this intent is enabled in the Developer Portal

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store user scores
user_scores = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def gpq(ctx, score: int):
    user = ctx.author
    if user.id not in user_scores:
        user_scores[user.id] = []
    user_scores[user.id].append(score)
    await ctx.send(f'{user.mention} has submitted a GPQ score of {score}!')

@bot.command()
async def gpq_view(ctx):
    user = ctx.author
    if user.id in user_scores:
        scores = user_scores[user.id][-10:]  # Get the last 10 scores
        if scores:
            scores_str = '\n'.join(map(str, scores))
            await ctx.send(f'Scores for {user.display_name}:\n{scores_str}')
        else:
            await ctx.send(f"{user.mention}, you don't have any GPQ scores yet.")
    else:
        await ctx.send(f"{user.mention}, you haven't submitted any GPQ scores yet.")

@bot.command()
async def gpq_graph(ctx):
    user = ctx.author
    if user.id in user_scores:
        scores = user_scores[user.id]
        if scores:
            plt.figure(figsize=(10, 5), facecolor='none', edgecolor='none')
            plt.plot(scores, marker='o', linestyle='-', color='b')
            plt.title(f'GPQ Scores Over Time for {user.display_name}', color='white')
            plt.xlabel('Attempts', color='white')
            plt.ylabel('Score', color='white')
            plt.grid(True)

            # Set face color to none for transparency
            plt.gca().patch.set_facecolor('none')

            # Set tick colors to white
            plt.tick_params(colors='white')

            buf = io.BytesIO()
            plt.savefig(buf, format='png', transparent=True)
            buf.seek(0)
            file = discord.File(buf, filename='gpq_scores.png')
            await ctx.send(file=file)
            buf.close()
            plt.close()
        else:
            await ctx.send(f"{user.mention}, you don't have any GPQ scores yet.")
    else:
        await ctx.send(f"{user.mention}, you haven't submitted any GPQ scores yet.")

# Get the bot token from the environment variable
bot_token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(bot_token)
