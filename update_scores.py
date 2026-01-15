import requests
import xml.etree.ElementTree as ET

def update_scores():
    # ESPN Endpoint for all FBS College Football games
    url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=100"
    
    try:
        # 10-second timeout to prevent "hanging" if ESPN is slow
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Build the RSS structure
        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")
        ET.SubElement(channel, "title").text = "Live CFB Scores"
        
        for event in data.get('events', []):
            comp = event['competitions'][0]
            status = event['status']['type']['detail']
            
            # Identify Home and Away teams
            t1 = comp['competitors'][0]
            t2 = comp['competitors'][1]
            
            away = t1 if t1['homeAway'] == 'away' else t2
            home = t1 if t1['homeAway'] == 'home' else t2
            
            # Format: Team 10, Team 7 (Final)
            score_line = f"{away['team']['shortDisplayName']} {away['score']}, {home['team']['shortDisplayName']} {home['score']} ({status})"
            
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = score_line
            
        # Save to ticker.xml
        tree = ET.ElementTree(root)
        tree.write("ticker.xml", encoding="utf-8", xml_declaration=True)
        print("Successfully updated ticker.xml")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_scores()
