import datetime
import json
import socket
import urllib.request
from types import SimpleNamespace
from smb.SMBConnection import SMBConnection


def from_timestamp(date):
    return datetime.datetime.fromtimestamp(date).date()


def load_config(filename: str) -> object:
    try:
        with open(filename, 'r') as fb:
            return json.load(fb, object_hook=lambda d: SimpleNamespace(**d))
    except FileNotFoundError as e:
        print('File not found', e)
        # logging.debug(f'Load config file: {e.strerror}')
        return
    except json.decoder.JSONDecodeError as e:
        print('parsing error', e)
        # logging.debug(f'Parsing config file: {e.msg}')
        return


def health_check(hc_key: str):
    try:
        urllib.request.urlopen(f'https://hc-ping.com/{hc_key}', timeout=10)
    except socket.error as sock_error:
        print('Socket_error', sock_error)


def get_connection(cfg_file_name):
    try:
        conn = SMBConnection(cfg_file_name.user, cfg_file_name.password, cfg_file_name.client_pc_name,
                             cfg_file_name.server_name)
        conn.connect(cfg_file_name.server_ip, timeout=5)
        # logging.debug(conn)
        return conn
    except Exception as get_connection_except:
        print('Error_get_connection', get_connection_except)


if __name__ == '__main__':

    config = load_config('config_DEV.json')
    my_conn = get_connection(config)

    if my_conn:
        try:
            list_files = my_conn.listPath(config.shared_folder, config.root_folder, pattern=config.file_mask)
        except Exception as e:
            print(e)
            exit()
        if list_files:
            for file in list_files:
                if from_timestamp(file.create_time).day == 1:
                    with open(config.daily_folder + file.filename, 'wb') as fp:
                        my_conn.retrieveFile(config.shared_folder, config.root_folder + file.filename, fp)
                        my_conn.close()
                        health_check(config.hc_key)
                        exit()
                elif from_timestamp(file.create_time) == (datetime.datetime.now() - datetime.timedelta(1)).date():
                    # print('DELTA', (datetime.datetime.now() - datetime.timedelta(1)).date())
                    # print(file.filename, from_timestamp(file.create_time))
                    with open(config.daily_folder + file.filename, 'wb') as fp:
                        my_conn.retrieveFile(config.shared_folder, config.root_folder + file.filename, fp)
                        health_check(config.hc_key)

            my_conn.close()
