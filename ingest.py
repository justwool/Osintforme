import os
import json
import feedparser
import time
from datetime import datetime

SOURCES = [
    {"name": "OSINTtechnical", "url": "https://bsky.app/profile/osinttechnical.bsky.social/rss", "platform": "bluesky", "category": "analysis", "region": "global"},
    {"name": "GeoConfirmed", "url": "https://bsky.app/profile/geoconfirmed.bsky.social/rss", "platform": "bluesky", "category": "geolocation", "region": "global"},
    {"name": "Nathan Ruser", "url": "https://bsky.app/profile/nathanruser.bsky.social/rss", "platform": "bluesky", "category": "geolocation", "region": "global"},
    {"name": "OSINT Techniques", "url": "https://bsky.app/profile/osinttechniques.bsky.social/rss", "platform": "bluesky", "category": "analysis", "region": "global"},
    {"name": "Bellingcat (BSky)", "url": "https://bsky.app/profile/bellingcat.bsky.social/rss", "platform": "bluesky", "category": "investigation", "region": "global"},
    {"name": "NRG8000", "url": "https://bsky.app/profile/nrg8000.bsky.social/rss", "platform": "bluesky", "category": "analysis", "region": "global"},
    {"name": "Aric Toler", "url": "https://bsky.app/profile/aric.toler.bsky.social/rss", "platform": "bluesky", "category": "analysis", "region": "global"},
    {"name": "Benjamin Strick", "url": "https://bsky.app/profile/benjaminstrick.bsky.social/rss", "platform": "bluesky", "category": "analysis", "region": "global"},
    {"name": "Eliot Higgins", "url": "https://bsky.app/profile/eliothiggins.bsky.social/rss", "platform": "bluesky", "category": "investigation", "region": "global"},
    {"name": "BNO News", "url": "https://bnonews.com/index.php/feed/", "platform": "rss", "category": "alerts", "region": "global"},
    {"name": "AP Middle East", "url": "https://apnews.com/hub/middle-east?outputType=xml", "platform": "rss", "category": "news", "region": "middle_east"},
    {"name": "Reuters ME", "url": "https://www.reuters.com/world/middle-east/rss", "platform": "rss", "category": "news", "region": "middle_east"},
    {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "platform": "rss", "category": "news", "region": "global"},
    {"name": "Al Jazeera ME", "url": "https://www.aljazeera.com/xml/rss/middleeast.xml", "platform": "rss", "category": "news", "region": "middle_east"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/world/rss", "platform": "rss", "category": "news", "region": "global"},
    {"name": "The Guardian ME", "url": "https://www.theguardian.com/world/middle-east/rss", "platform": "rss", "category": "news", "region": "middle_east"},
    {"name": "Bellingcat", "url": "https://www.bellingcat.com/feed", "platform": "rss", "category": "investigations", "region": "global"},
    {"name": "ISW", "url": "https://www.understandingwar.org/rss.xml", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Long War Journal", "url": "https://www.longwarjournal.org/feed", "platform": "rss", "category": "analysis", "region": "middle_east"},
    {"name": "Defence Blog", "url": "https://defence-blog.com/feed", "platform": "rss", "category": "defense_news", "region": "global"},
    {"name": "Defense Post", "url": "https://www.thedefensepost.com/feed", "platform": "rss", "category": "defense_news", "region": "global"},
    {"name": "Janes", "url": "https://www.janes.com/feeds/news", "platform": "rss", "category": "defense_intel", "region": "global"},
    {"name": "Naval News", "url": "https://www.navalnews.com/feed", "platform": "rss", "category": "naval", "region": "global"},
    {"name": "TWZ", "url": "https://www.twz.com/feed", "platform": "rss", "category": "defense_analysis", "region": "global"},
    {"name": "Breaking Defense", "url": "https://breakingdefense.com/feed", "platform": "rss", "category": "defense_news", "region": "global"},
    {"name": "Covert Shores", "url": "http://www.covertshores.net/1/feed", "platform": "rss", "category": "naval", "region": "global"},
    {"name": "Amwaj Media", "url": "https://amwaj.media/rss", "platform": "rss", "category": "regional_media", "region": "iran_gulf"},
    {"name": "Tasnim News", "url": "https://www.tasnimnews.com/en/rss/feed/0/7/0/service/0", "platform": "rss", "category": "regional_media", "region": "iran"},
    {"name": "Fars News", "url": "https://www.farsnews.ir/en/rss", "platform": "rss", "category": "regional_media", "region": "iran"},
    {"name": "Mehr News", "url": "https://en.mehrnews.com/rss", "platform": "rss", "category": "regional_media", "region": "iran"}
]

def fetch_intel():
    history = []
    if os.path.exists("data.json"):
        with open("data.json", 'r') as f: history = json.load(f)
    seen_urls = {item['url'] for item in history}
    new_entries = []
    for src in SOURCES:
        try:
            feed = feedparser.parse(src['url'])
            for entry in feed.entries[:5]:
                if entry.link not in seen_urls:
                    new_entries.append({
                        "id": str(time.time()) + entry.link,
                        "timestamp": datetime.now().isoformat(),
                        "source": src['name'],
                        "platform": src['platform'],
                        "category": src['category'],
                        "region": src['region'],
                        "text": entry.title,
                        "url": entry.link
                    })
                    seen_urls.add(entry.link)
        except: continue
    with open("data.json", 'w') as f:
        json.dump((new_entries + history)[:200], f, indent=2)

if __name__ == "__main__":
    fetch_intel()
