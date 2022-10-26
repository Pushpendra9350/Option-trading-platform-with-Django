import logging
from pathlib import Path
from datetime import datetime
from pytz import timezone
tz = timezone('Asia/Kolkata')
def timetz(*args):
    return datetime.now(tz).timetuple()
logging.Formatter.converter = timetz

logging.basicConfig(filename=Path('log/error.log').resolve(),
                        level=logging.INFO,
                        format="[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
                        datefmt="%d-%b-%Y %H:%M:%S",)
logger=logging.getLogger()
