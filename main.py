import os
import re
import json
import discord
import requests
from requests.auth import HTTPBasicAuth

discordToken = os.environ['TOKEN']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
endpoint =  "https://api.rtt.io/api/v1/json/search/"

outputTxt = """
`{0}` from `{1}`
Expected platform: `{2}`
This service is currently at `{3}`.
Expected at: `{4}`"""""
formatStringList= []

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.content)
    if message.content.startswith('!search'):
        try:
          print("Starting search...")
          # Mildly cursed message assertion
          # ['!search',' ','BMH', ' ', ...]
          keywords = re.split("( )", message.content)
          # ['!search','BMH']
          keywords = [elem for elem in keywords if elem != " "]
          if len(keywords) != 2:
            await message.channel.send("Invalid input, try again")
          else:  
            print("Invoking API")
            print(endpoint + keywords[1])
            response = requests.get(endpoint + keywords[1],
                        auth = HTTPBasicAuth(username, password))
            if (response.status_code == 200):
              response = json.loads(response.text)
              counter = 0;
              nameCounter = 0;
              # Print the first 5 services for this train
              for serv in response["services"]:
                if nameCounter < 1:
                  await message.channel.send("**Next trains at " + serv["locationDetail"].get("description") + "**")
                  nameCounter += 1
                if counter > 4:
                  break;
                else:  
                  for orgDet in serv["locationDetail"].get("origin"):
                      for locDet in serv["locationDetail"].get("destination"):
                          formatStringList.append(orgDet["publicTime"][:2] + ':' + orgDet["publicTime"][2:])
                          formatStringList.append(orgDet["description"])
                          formatStringList.append(serv["locationDetail"].get("platform"))
                          formatStringList.append(serv["locationDetail"].get("description"))
                          formatStringList.append(serv["locationDetail"].get("realtimeDeparture")[:2] + ':' + serv["locationDetail"].get("realtimeDeparture")[2:])
                          print("Got response from API:") 
                          print(outputTxt.format(formatStringList[0],
                                    formatStringList[1],
                                    formatStringList[2],
                                    formatStringList[3],
                                    formatStringList[4]))
                          await message.channel.send(outputTxt.format(formatStringList[0],
                                    formatStringList[1],
                                    formatStringList[2],
                                    formatStringList[3],
                                    formatStringList[4]))
                          formatStringList.clear()
                          counter += 1
                          break;
                  
            else:
              await message.channel.send("Bad Status from API " + str(response.status_code))
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
# Will throw a HTTPException if we are being rate limited by Repl.it
except Exception:
  print("HTTPException - Rate limited")
