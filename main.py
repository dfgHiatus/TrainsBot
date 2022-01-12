import os
import re
import json
import discord
import requests

discordToken = os.environ['TOKEN']
headers = {"Username" : "rttapi_dfgHiatus",
           "Password"  : "2d5f33850a19f59bc597b65ba2052f21810544f1"}
endpoint =  "api.rtt.io/api/v1/json/"

client = discord.Client()

@client.event
async def on_message(ctx, *, message):
    if message.author == client.user:
        return

    if message.content.startswith('!search'):
        try:
          keywords = re.split("( )", message)
          response = json.loads(requests.get(endpoint + "/json/search/" + keywords[0],    headers))
          msg = response(["destination"])
          await client.send_message(message.channel, msg)
        except Exception:
            await client.send_message(message.channel, "Something bad happened, please try again.")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(discordToken)