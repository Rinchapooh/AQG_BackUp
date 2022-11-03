import logging
import socket
import urllib.request



logging.basicConfig(
    filename='AQG_backup.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


def health_check(hc_key: str):

    try:
        urllib.request.urlopen(f'https://hc-ping.com/{hc_key}', timeout=10)
    except socket.error as e:
        print(e)


def main():
    print("From Main")

key_hc = 'f46c0d1a-fb63-4a36-9ed7-f951eea35de9'

if __name__ == '__main__':
    health_check(hc_key=key_hc)


