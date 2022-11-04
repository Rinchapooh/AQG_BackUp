import logging
import socket
import urllib.request

import file_handler

# logging.basicConfig(
#     filename='AQG_backup.log',
#     level=logging.DEBUG,
#     format='%(asctime)s:%(levelname)s:%(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S')


def health_check(hc_key: str):
    try:
        urllib.request.urlopen(f'https://hc-ping.com/{hc_key}', timeout=10)
    except socket.error as e:
        print(e)


def main():
    print("From Main")


if __name__ == '__main__':
    config = file_handler.load_config('config.json')

    health_check(hc_key=config.hc_key)
    print("DONE")

