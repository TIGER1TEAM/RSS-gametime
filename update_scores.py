import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pytz

def update_scores():
    # Set to US/Central time
    tz = pytz.timezone('US/Central')
    today = datetime.now(tz).strftime('%Y%m%d')
    
    # ESPN API (Groups 80 = FBS Division 1)
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&dates={today}"
    
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
            ET.SubElement(item, "title").text = "No games scheduled today."
        else:
            for event in events:
                comp = event['competitions'][0]
                status = event['status']['type']['detail']
                
                # Get the two teams
                t1 = comp['competitors'][0]
                t2 = comp['competitors'][1]
                away = t1 if t1['homeAway'] == 'away' else t2
                home = t1 if t1['homeAway'] == 'home' else t2
                
                # --- CHOOSE YOUR NAME STYLE HERE ---
                # Use ['abbreviation'] for: "UGA 21, ALA 14"
                # Use ['shortDisplayName'] for: "Georgia 21, Alabama 14"
                away_name = away['team']['abbreviation'] 
                home_name = home['team']['abbreviation']
                
                score_line = f"{away_name} {away['score']}, {home_name} {home['score']} ({status})"
                
                item = ET.SubElement(channel, "item")
                ET.SubElement(item, "title").text = score_line
            
        tree = ET.ElementTree(root)
        tree.write("ticker.xml", encoding="utf-8", xml_declaration=True)
        print(f"Ticker updated for {today} (Central Time)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_scores()
