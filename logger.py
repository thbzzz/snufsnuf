import logging
from random import choice, shuffle

import colorama

colors = [getattr(colorama.Fore, x) for x in [
    'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN',
    'LIGHTRED_EX', 'LIGHTGREEN_EX', 'LIGHTYELLOW_EX', 'LIGHTBLUE_EX', 'LIGHTMAGENTA_EX', 'LIGHTCYAN_EX'
]]


class CustomFormatter(logging.Formatter):

    fmt = '%(asctime)s %(name)-10s %(levelname)-8s %(message)s'

    FORMATS = {
        logging.DEBUG: fmt.replace('%(levelname)-8s', f'%(levelname)-8s{colorama.Style.RESET_ALL}'),
        logging.INFO: fmt.replace('%(levelname)-8s', f'{colorama.Fore.GREEN}%(levelname)-8s{colorama.Style.RESET_ALL}'),
        logging.WARNING: fmt.replace('%(levelname)-8s', f'{colorama.Fore.YELLOW}%(levelname)-8s{colorama.Style.RESET_ALL}'),
        logging.ERROR: fmt.replace('%(levelname)-8s', f'{colorama.Fore.RED}%(levelname)-8s{colorama.Style.RESET_ALL}'),
        logging.CRITICAL: fmt.replace('%(levelname)-8s', f'{colorama.Fore.RED+colorama.Style.BRIGHT}%(levelname)-8s{colorama.Style.RESET_ALL}')
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logging.getLogger("urllib3").setLevel(logging.WARNING)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())

logger = logging.getLogger(f'{choice(colors)}SNUFSNUF{colorama.Style.RESET_ALL}')
logger.addHandler(ch)
logger.setLevel(logging.INFO)