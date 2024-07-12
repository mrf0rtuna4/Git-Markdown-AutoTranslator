import asyncio
import os
from dotenv import load_dotenv

from app import LocalizationManager, log_info, log_error

load_dotenv()

async def main():
    log_info("💚 AutoLocalizator | by mr_f0rtuna4")
    selected_langs = os.getenv("LANGS")
    if not selected_langs:
        log_error("❌ LANGS environment variable not set.")
        return
    manager = LocalizationManager(selected_langs)
    await manager.update_localizations()

if __name__ == "__main__":
    asyncio.run(main())
