"""
Test if all imports work correctly
"""
import sys

print("Testing imports...")

try:
    import os
    print("✅ os")
except Exception as e:
    print(f"❌ os: {e}")

try:
    import asyncio
    print("✅ asyncio")
except Exception as e:
    print(f"❌ asyncio: {e}")

try:
    import logging
    print("✅ logging")
except Exception as e:
    print(f"❌ logging: {e}")

try:
    from dotenv import load_dotenv
    print("✅ dotenv")
except Exception as e:
    print(f"❌ dotenv: {e}")

try:
    import config
    print("✅ config")
    print(f"   - TELEGRAM_TOKEN: {'SET' if config.TELEGRAM_TOKEN else 'NOT SET'}")
    print(f"   - OPENAI_API_KEY: {'SET' if config.OPENAI_API_KEY else 'NOT SET'}")
    print(f"   - TELEGRAM_API_ID: {'SET' if config.TELEGRAM_API_ID else 'NOT SET'}")
except Exception as e:
    print(f"❌ config: {e}")

try:
    from db_handler import SermonDatabase
    print("✅ db_handler")
except Exception as e:
    print(f"❌ db_handler: {e}")

try:
    from utils import rag_engine
    print("✅ utils")
except Exception as e:
    print(f"❌ utils: {e}")

try:
    from rag_ingest import ChannelScraper, MaterialsLoader
    print("✅ rag_ingest")
except Exception as e:
    print(f"❌ rag_ingest: {e}")

try:
    from telethon import TelegramClient
    print("✅ telethon")
except Exception as e:
    print(f"❌ telethon: {e}")

try:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    print("✅ langchain_openai")
except Exception as e:
    print(f"❌ langchain_openai: {e}")

try:
    from langchain_chroma import Chroma
    print("✅ langchain_chroma")
except Exception as e:
    print(f"❌ langchain_chroma: {e}")

print("\n✅ All imports successful!" if all else "\n⚠️ Some imports failed")