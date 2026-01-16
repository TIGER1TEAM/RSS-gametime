import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo # Standard in Python 3.9+

def update_scores():
    # Set to US/Central time using built-in library
    tz = ZoneInfo('US/Central')
    today = datetime.now(tz).strftime('%Y%m%d')
    
    # ESPN API (Groups 80 = FBS Division 1)
    # CFB Line
    #url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80"

    # NFL Line
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")
        ET.SubElement(channel, "title").text = "STATTRACK LIVE"
        
        events = data.get('events', [])
        
        if not events:
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = f"No games today ({datetime.now(tz).strftime('%m/%d')})"
        else:
            for event in events:
                comp = event['competitions'][0]
                status = event['status']['type']['detail']
                
                # Sort Home vs Away
                t1 = comp['competitors'][0]
                t2 = comp['competitors'][1]
                away = t1 if t1['homeAway'] == 'away' else t2
                home = t1 if t1['homeAway'] == 'home' else t2
                
                # Use abbreviation (UGA, ALA, etc.)
                away_name = away['team']['abbreviation']
                home_name = home['team']['abbreviation']
                
                score_line = f"{away_name} {away['score']}, {home_name} {home['score']} ({status})"
                
                item = ET.SubElement(channel, "item")
                ET.SubElement(item, "title").text = score_line
            
        tree = ET.ElementTree(root)
        tree.write("ticker.xml", encoding="utf-8", xml_declaration=True)
        print(f"Ticker updated for {today}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_scores()
