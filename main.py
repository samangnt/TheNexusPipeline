import asyncio
import logging
import os
from datetime import datetime

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

from models.studio_asset import StudioAsset
from utils.crawler import crawl_directory
from utils.database import init_database, is_already_processed, save_asset
from utils.decorators import time_it
from services.gemini_service import analyze_asset
from services.webhook_service import send_notification

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

# Load .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---- STEP 1: Async analyzer ----
async def analyze_asset_async(asset: StudioAsset) -> StudioAsset:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, analyze_asset, asset.name, asset.path)
    asset.mark_processed(result["tags"], result["critique"])
    return asset

# ---- STEP 2: Batch processor ----
@time_it
def run_batch(assets: list) -> list:
    return asyncio.run(_async_batch(assets))

async def _async_batch(assets: list) -> list:
    tasks = [analyze_asset_async(asset) for asset in assets]
    return await asyncio.gather(*tasks)

# ---- STEP 3: Main pipeline ----
def main():
    logging.info("🚀 Nexus Pipeline started")
    
    # Initialize database
    init_database()
    
    # Crawl directory
    scan_path = "./test_assets"
    all_assets = crawl_directory(scan_path)
    logging.info(f"Found {len(all_assets)} assets")
    
    # Filter unprocessed using list comprehension
    unprocessed = [a for a in all_assets if not is_already_processed(a.path)]
    logging.info(f"{len(unprocessed)} new assets to process")
    
    if not unprocessed:
        logging.info("Nothing new to process. Exiting.")
        return
    
    # Run async batch
    processed = run_batch(unprocessed)
    
    # Save to database
    for asset in processed:
        save_asset(asset)
    
    # Export CSV report
    date_str = datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame([a.to_dict() for a in processed])
    csv_filename = f"daily_report_{date_str}.csv"
    df.to_csv(csv_filename, index=False)
    logging.info(f"Report saved: {csv_filename}")
    
    # Send webhook notification
    send_notification(
        f"Nexus Pipeline Complete - {date_str}",
        f"{len(processed)} assets processed",
        priority="HIGH",
        channel="Art-Team"
    )
    
    logging.info("✅ Pipeline complete!")

if __name__ == "__main__":
    main()