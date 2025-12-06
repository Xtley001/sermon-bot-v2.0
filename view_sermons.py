"""
View all scraped sermons from the database
"""
from db_handler import SermonDatabase
import config

db = SermonDatabase(config.DB_PATH)

# Get all sermons
sermons = db.get_all_sermons()

print(f"\n{'='*80}")
print(f"TOTAL SERMONS: {len(sermons)}")
print(f"{'='*80}\n")

for i, sermon in enumerate(sermons, 1):
    print(f"{i}. {sermon['title']}")
    print(f"   Channel: {sermon['channel']}")
    print(f"   Date: {sermon['date']}")
    print(f"   Theme: {sermon['theme']}")
    print(f"   Link: {sermon['message_link']}")
    print(f"   Description: {sermon['description'][:100]}...")
    print()

# Summary by channel
channels = {}
for sermon in sermons:
    channel = sermon['channel']
    channels[channel] = channels.get(channel, 0) + 1

print(f"\n{'='*80}")
print("SERMONS BY CHANNEL:")
print(f"{'='*80}")
for channel, count in channels.items():
    print(f"{channel}: {count} sermons")