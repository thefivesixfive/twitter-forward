#imports
from discord.ext import commands
from tweepy import API, OAuthHandler
from dotenv import load_dotenv
from os import getenv

import tweepy

# grab .env vars
load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = getenv("TWITTER_ACCESS_SECRET")

# create bots
discord = commands.Bot(command_prefix="tf ")
oauth = OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
oauth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter = API(oauth)

# logging
@discord.event
async def on_ready():
    print('[+] Connected to Discord')

# tweet command
@discord.command(name="tweet")
async def tweet(ctx, *args):
    # get message ready by merging args
    tweet = ""
    for arg in args:
        tweet += arg+" "
    # set tweet size
    tweet = tweet[0:140]
    # send tweet
    try:
        # send tweet
        tweeted = twitter.update_status(tweet)
        # add reaction and DM ID
        await ctx.message.add_reaction("👍")
        await ctx.author.send(f"Tweeted! The ID is {tweeted.id_str}")
        # log
        print(f"[+] Tweeted {tweet} with ID {tweeted.id_str}")
    except Exception as e:
        # add reaction and DM error
        await ctx.author.send("Unable to Tweet! Sorry.")
        await ctx.message.add_reaction("👎")
        # log
        print(f"[-] Error in Tweet {e}")

# delete tweet
@discord.command(name="untweet")
async def untweet(ctx, id):
    # try to delete tweet
    try:
        twitter.destroy_status(id)
        # add reaction and confirm deletion
        await ctx.message.add_reaction("👍")
        await ctx.author.send(f"Untweeted Tweet with ID {id}")
        # log
        print(f"[+] Untweeted Tweet with ID {id}")
    except Exception as e:
        # add reaction and DM error
        await ctx.message.add_reaction("👎")
        await ctx.author.send("Unable to Untweet! Sorry.")
        # log
        print("[-] Error in Untweet {e}")   

# run
if __name__ == "__main__":
    discord.run(DISCORD_TOKEN)