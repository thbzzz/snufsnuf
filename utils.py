import signal

import colorama
import requests
from requests.exceptions import Timeout
from urllib3 import disable_warnings

disable_warnings()


class HttpClient:
    def __init__(self, logger) -> None:
        self.headers = {
            'user-agent': 'snufsnuf'
        }
        self.timeout = 5
        self.verify = False
        self.logger = logger

    def get(self, url: str) -> requests.models.Response | None:
        r = None
        try:
            self.logger.debug(f'{colorama.Fore.CYAN}{url}{colorama.Style.RESET_ALL}')
            r = requests.get(f'{url}', headers=self.headers, allow_redirects=True, timeout=self.timeout, verify=self.verify)
        except Timeout:
            self.logger.error(f'{colorama.Fore.CYAN}{url}{colorama.Style.RESET_ALL} {colorama.Fore.RED}TIMEOUT{colorama.Style.RESET_ALL}')
        except:
            self.logger.error(f'{colorama.Fore.CYAN}{url}{colorama.Style.RESET_ALL}')
            
        return r


class GracefulKiller:

    kill_now = False

    def __init__(self, logger):
        self.logger = logger
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True
        self.logger.info('Killing gracefully...')