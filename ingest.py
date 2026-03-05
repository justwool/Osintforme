import feedparser
import json
import os
import time
from datetime import datetime

# FULL SOURCE LIST RESTORED
SOURCES = [
    {"name": "BNO News", "url": "https://hnrss.org/newest?q=BNO+News", "platform": "rss", "category": "alerts", "region": "global"},
    {"name": "Liveuamap", "url": "https://liveuamap.com/en/feed/rss", "platform": "rss", "category": "analysis", "region": "ua"},
    {"name": "OSINTtechnical", "url": "https://bsky.rss.average.icu/profile/osinttechnical.bsky.social", "platform": "bluesky", "category": "naval", "region": "global"},
    {"name": "Sentdefender", "url": "https://bsky.rss.average.icu/profile/sentdefender.bsky.social", "platform": "bluesky", "category": "alerts", "region": "global"},
    {"name": "CIG Telegram", "url": "https://rsshub.app/telegram/channel/CIG_telegram", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Intel Crater", "url": "https://rsshub.app/telegram/channel/intelcrater", "platform": "rss", "category": "alerts", "region": "global"},
    {"name": "RawsGlobal", "url": "https://bsky.rss.average.icu/profile/rawsglobal.bsky.social", "platform": "bluesky", "category": "alerts", "region": "global"},
    {"name": "Faytuks", "url": "https://bsky.rss.average.icu/profile/faytuksnews.bsky.social", "platform": "bluesky", "category": "alerts", "region": "global"},
    {"name": "DefconLevel", "url": "https://www.defconlevel.com/index.xml", "platform": "rss", "category": "alerts", "region": "global"},
    {"name": "US Navy News", "url": "https://www.navy.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=720", "platform": "rss", "category": "naval", "region": "global"},
    {"name": "USNI News", "url": "https://news.usni.org/feed", "platform": "rss", "category": "naval", "region": "global"},
    {"name": "UK MoD", "url": "https://www.gov.uk/government/organisations/ministry-of-defence.atom", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "South China Morning Post", "url": "https://www.scmp.com/rss/91/feed.xml", "platform": "rss", "category": "analysis", "region": "asia"},
    {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "platform": "rss", "category": "analysis", "region": "mena"},
    {"name": "The Drive WarZone", "url": "https://www.twz.com/feed", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Janes Defence", "url": "https://www.janes.com/rss/news", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Euromaidan Press", "url": "https://euromaidanpress.com/feed/", "platform": "rss", "category": "analysis", "region": "ua"},
    {"name": "Kyiv Independent", "url": "https://kyivindependent.com/rss/", "platform": "rss", "category": "analysis", "region": "ua"},
    {"name": "ISW Ukraine", "url": "https://www.understandingwar.org/rss.xml", "platform": "rss", "category": "analysis", "region": "ua"},
    {"name": "Naval News", "url": "https://www.navalnews.com/feed/", "platform": "rss", "category": "naval", "region": "global"},
    {"name": "Maritime Executive", "url": "https://www.maritime-executive.com/rss", "platform": "rss", "category": "naval", "region": "global"},
    {"name": "TASS English", "url": "https://tass.com/rss/v2.xml", "platform": "rss", "category": "analysis", "region": "ru"},
    {"name": "Reuters World", "url": "https://www.reutersagency.com/feed/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "AP News", "url": "https://apnews.com/hub/world-news.rss", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Defense News", "url": "https://www.defensenews.com/arc/outboundfeeds/rss/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Breaking Defense", "url": "https://breakingdefense.com/feed/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Air Force Mag", "url": "https://www.airandspaceforces.com/feed/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Aerospace Forces", "url": "https://bsky.rss.average.icu/profile/afms.bsky.social", "platform": "bluesky", "category": "analysis", "region": "global"},
    {"name": "KofmanOSINT", "url": "https://bsky.rss.average.icu/profile/michaelkofman.bsky.social", "platform": "bluesky", "category": "analysis", "region": "ua"},
    {"name": "LeeOSINT", "url": "https://bsky.rss.average.icu/profile/rob-lee.bsky.social", "platform": "bluesky", "category": "analysis", "region": "ua"},
    {"name": "Tendar", "url": "https://bsky.rss.average.icu/profile/tendar.bsky.social", "platform": "bluesky", "category": "analysis", "region": "ua"},
    {"name": "War_Mapper", "url": "https://bsky.rss.average.icu/profile/warmapper.bsky.social", "platform": "bluesky", "category": "analysis", "region": "ua"},
    {"name": "Global Guardian", "url": "https://www.globalguardian.com/intelligence-reports/rss.xml", "platform": "rss", "category": "alerts", "region": "global"},
    {"name": "Crisis24", "url": "https://crisis24.garda.com/rss-feeds", "platform": "rss", "category": "alerts", "region": "global"},
    {"name": "Flashpoint", "url": "https://flashpoint.io/feed/", "platform": "rss", "category": "alerts", "region": "global"},
    {"name": "Defense Post", "url": "https://www.thedefensepost.com/feed/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Naval Gazing", "url": "https://bsky.rss.average.icu/profile/navalgazing.bsky.social", "platform": "bluesky", "category": "naval", "region": "global"},
    {"name": "H I Sutton", "url": "https://bsky.rss.average.icu/profile/hisutton.bsky.social", "platform": "bluesky", "category": "naval", "region": "global"},
    {"name": "Navy Lookout", "url": "https://bsky.rss.average.icu/profile/navylookout.bsky.social", "platform": "bluesky", "category": "naval", "region": "global"},
    {"name": "War on the Rocks", "url": "https://warontherocks.com/feed/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Small Wars Journal", "url": "https://smallwarsjournal.com/rss.xml", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "RealClearDefense", "url": "https://www.realcleardefense.com/index.xml", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "SOFREP", "url": "https://sofrep.com/feed/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Task & Purpose", "url": "https://taskandpurpose.com/feed/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Defense One", "url": "https://www.defenseone.com/rss/all/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Military Times", "url": "https://www.militarytimes.com/arc/outboundfeeds/rss/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Stripes News", "url": "https://www.stripes.com/rss/news/", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Radio Free Europe", "url": "https://www.rferl.org/rss", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "France24", "url": "https://www.france24.com/en/rss", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "DW World", "url": "https://rss.dw.com/xml/rss-en-all", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "platform": "rss", "category": "analysis", "region": "global"},
    {"name": "Guardian World", "url": "https://www.theguardian.com/world/rss", "platform": "rss", "category": "analysis", "region": "global"}
]

def fetch_intel():
    history = []
    if os.path.exists("data.json"):
        with open("data.json", 'r') as f:
            try:
                history = json.load(f)
            except:
                history = []
    
    # DUPLICATE PROTECTION: Track URLs and Titles already in history
    seen_urls = {item['url'] for item in history}
    seen_titles = {item['text'].strip().lower() for item in history}
    
    new_entries = []
    
    for src in SOURCES:
        try:
            target_url = src['url']
            if "bsky.app" in target_url:
                target_url = target_url.replace("bsky.app/profile/", "bsky.rss.average.icu/profile/")
            
            feed = feedparser.parse(target_url)
            for entry in feed.entries[:15]:
                title_clean = entry.title.strip().lower()
                
                # FILTER: If URL or Title is a duplicate, skip it
                if entry.link not in seen_urls and title_clean not in seen_titles:
                    raw_date = entry.get('published_parsed') or entry.get('updated_parsed')
                    if raw_date:
                        timestamp = datetime(*raw_date[:6]).isoformat()
                    else:
                        timestamp = datetime.now().isoformat()
                    
                    new_entries.append({
                        "id": entry.link,
                        "timestamp": timestamp,
                        "source": src['name'],
                        "platform": src['platform'],
                        "category": src['category'],
                        "region": src['region'],
                        "text": entry.title,
                        "url": entry.link
                    })
                    seen_urls.add(entry.link)
                    seen_titles.add(title_clean)
        except:
            continue
    
    # SORT: Newest first
    updated_history = sorted(new_entries + history, key=lambda x: x['timestamp'], reverse=True)
    
    # LIMIT: Keep latest 500
    with open("data.json", 'w') as f:
        json.dump(updated_history[:500], f, indent=2)

if __name__ == "__main__":
    fetch_intel()
