"""
Fix: Re-populate vector store from database
"""
import logging
from langchain.schema import Document
from db_handler import SermonDatabase
from utils import rag_engine
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🔧 Fixing vector store...")
print("=" * 50)

# Get all sermons from database
db = SermonDatabase(config.DB_PATH)
sermons = db.get_all_sermons()

print(f"📊 Found {len(sermons)} sermons in database")

# Convert to documents with clean metadata (no None values)
documents = []
for sermon in sermons:
    content = f"{sermon['title']}\n\n{sermon['description']}"
    
    doc = Document(
        page_content=content,
        metadata={
            'title': sermon['title'],
            'description': sermon['description'],
            'channel': sermon['channel'],
            'message_link': sermon['message_link'],
            'image_url': sermon.get('image_url') or '',  # Replace None with empty string
            'date': sermon.get('date') or '',
            'theme': sermon.get('theme') or ''
        }
    )
    documents.append(doc)

print(f"📝 Created {len(documents)} documents")

# Clear existing vector store
print("🗑️  Clearing old vector store...")
rag_engine.clear_all()

# Add all documents
print("➕ Adding documents to vector store...")
# Add in batches to avoid memory issues
batch_size = 50
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    rag_engine.add_documents(batch)
    print(f"   Added batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")

print("\n" + "=" * 50)
print("✅ Vector store fixed!")
print(f"📊 Total documents: {len(documents)}")
print("=" * 50)

# Test search
print("\n🧪 Testing search...")
results = rag_engine.search("faith", k=5)
print(f"Found {len(results)} results for 'faith'")
if results:
    print(f"First result: {results[0]['title']}")