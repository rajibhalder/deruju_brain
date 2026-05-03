from apscheduler.schedulers.blocking import BlockingScheduler
from logger import logger
from app import main


def run_brain():
    logger.info("scheduled deruju brain started")
    try:
        main()
        logger.info("scheduled deruju brain finished")
    except Exception as ex:
        logger.exception(f"brain failed: {ex}")


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(
        run_brain,
        trigger="interval",
        hours=6,
        id="deruju_brain_job",
        max_instances=1,
        coalesce=True,
        misfire_grace_time=3600,
    )
    logger.info("deruju brain scheduler started")

    # run once immediately
    run_brain()

    # keep process alive
    scheduler.start()