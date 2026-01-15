import requests
import xml.etree.ElementTree as ET

# 1. Get the latest scores (JSON format)
# Using a community NCAA API (FBS scores)
api_url = "https://ncaa-api.henrygd.me/scoreboard/football/fbs"
response = requests.get(api_url)
data = response.json()

# 2. Build your custom XML structure
# Change the tags (ticker, game, etc.) to match what your ticker expects
root = ET.Element("rss", version="2.0")
channel = ET.SubElement(root, "channel")
ET.SubElement(channel, "title").text = "CFB Scores Ticker"

for game in data.get('games', []):
    home_team = game['home']['names']['short']
    home_score = game['home']['score']
    away_team = game['away']['names']['short']
    away_score = game['away']['score']
    status = game['status']['display']

    item = ET.SubElement(channel, "item")
    # This creates the text your ticker will likely show
    ET.SubElement(item, "title").text = f"{away_team} {away_score}, {home_team} {home_score} ({status})"

# 3. Save it over your existing xml file
tree = ET.ElementTree(root)
tree.write("ticker.xml", encoding="utf-8", xml_declaration=True)
