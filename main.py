import os
import re
import json
import discord
import requests
from requests.auth import HTTPBasicAuth

discordToken = os.environ['TOKEN']
# username = os.environ['USERNAME']
# password = os.environ['PASSWORD']
endpoint =  "https://api.rtt.io/api/v1/json/search/"

outputTxt = """**Next trains at {0}**:

`{1}` from `{2}`
Expected platform: `{3}`
This service is currently at `{4}`.
Expected at: `{5}`"""""
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
          keywords = re.split("( )", message.content)
          # This is cursed - Assert message is formatted !search BMH -. ['!search','','BMH']
          if len(keywords) != 3:
            await message.channel.send("Invalid input, try again")
          else:  
            print("Invoking API")
            print(endpoint + keywords[0])
            # Somehow, this refuses to work unless you put the secret key in as a string
            response = requests.get(endpoint + keywords[2],
                        auth = HTTPBasicAuth('rttapi_dfgHiatus', '2d5f33850a19f59bc597b65ba2052f21810544f1'))
            if (response.status_code == 200):
              response = json.loads(response.text)
              for serv in response["services"]:
                  for orgDet in serv["locationDetail"].get("origin"):
                      for locDet in serv["locationDetail"].get("destination"):

                          formatStringList.append(serv["locationDetail"].get("description"))
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
                                    formatStringList[4],
                                    formatStringList[5]))
                          await message.channel.send(outputTxt.format(formatStringList[0],
                                    formatStringList[1],
                                    formatStringList[2],
                                    formatStringList[3],
                                    formatStringList[4],
                                    formatStringList[5]))
                          formatStringList.clear()

                          break;
                      break;
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
# HTTPException  
except Exception:
  print("Rate limited")