import asyncio
import logging
from bot import build_application
from scheduler import setup_scheduler
import database as db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting Social Media Agent...")
    db.initialize_db()
    logger.info("Database ready.")

    app = build_application()
    scheduler = setup_scheduler(app.bot)
    scheduler.start()
    logger.info("Scheduler started.")
    logger.info("Bot running. Open Telegram and send /generate to create content now.")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        scheduler.shutdown()
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
