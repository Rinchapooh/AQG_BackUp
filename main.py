import logging.config
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


if __name__ == '__main__':

    cfg = file_handler.load_config('config.json')

    try:
        my_conn = file_handler.get_connection(cfg)
    except Exception as e:
        print('first')

    try:
        list_files = my_conn.listPath(cfg.shared_folder, cfg.root_folder, pattern=cfg.file_mask)
    except Exception as e:
        print('second')



    for x in list_files:
        print(x.filename)
