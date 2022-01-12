import os
import re
import json
import discord
import requests
from requests.auth import HTTPBasicAuth

discordToken = os.environ['TOKEN']
# username = os.environ['USERNAME']
# password = os.environ['PASSWORD']
endpoint =  "https://api.rtt.io/api/v1/json/"

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.content)
    if message.content.startswith('!search'):
        try:
          print("Starting search...")
          keywords = re.split("( )", message.content)
          # Assert message is formatted !search BMH -. ['!search','','BMH']
          if len(keywords) != 3:
            await message.channel.send("Invalid input, try again")
          print("Invoking API")
          # Somehow, this refuses to work unless you put the api key in as a string
          response = requests.get(endpoint + "search/" + keywords[2],
                                  auth = HTTPBasicAuth('rttapi_dfgHiatus', '2d5f33850a19f59bc597b65ba2052f21810544f1'))
          status_code = response.status_code
          if (status_code == 200):
              response = json.loads(response.text)
              for serv in response["services"]:
                  for locDet in serv["locationDetail"].get("destination"):
                          msg = serv["locationDetail"].get("tiploc") + ", " + serv["locationDetail"].get("description") + "'s next destinaiton is " + locDet["tiploc"] + ", " + locDet["description"] + "."
              print("Got response from API:") 
              print(msg)
              await message.channel.send(msg)
          else:
            await message.channel.send("Bad Status from API " + str(status_code))
        except Exception:
            await message.channel.send("That sign wasn't found, please try again.")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

try:
  client.run(discordToken)
# HTTPException  
except Exception:
  print("Rate limited")