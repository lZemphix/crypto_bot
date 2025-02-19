#! /usr/bin/env python
from cfg import logger_config
from bot.bot import Bot
import random
from modules.notifies_manager import TeleNotify
import logging


def main():
    try: 
        logger = logging.getLogger(__name__)
        logging.getLogger('_http_manager').setLevel(logging.CRITICAL)
        Bot().activate()
    except Exception as e:
        eid = random.randint(100000, 9999999)
        TeleNotify(True).error(f"Error id: {eid}.\nReport the error to the developer, naming the error id")
        logger.error("Error id: %s. Message: %s", eid, e)


if __name__ == "__main__":
    main()