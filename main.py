import datetime
import socket
import urllib.request
import file_handler


# logging.basicConfig(
#     filename='AQG_backup.log',
#     level=logging.DEBUG,
#     format='%(asctime)s:%(levelname)s:%(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S')

def from_timestamp(date):
    return datetime.datetime.fromtimestamp(date).date()


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

    for file in list_files:
        if from_timestamp(file.create_time).day == 1:
            with open(cfg.daily_folder_test + file.filename, 'wb') as fp:
                my_conn.retrieveFile(cfg.shared_folder, cfg.root_folder + file.filename, fp)
                my_conn.close()
                exit()
        elif from_timestamp(file.create_time) <= (datetime.datetime.now() - datetime.timedelta(1)).date():
            with open(cfg.daily_folder_test + file.filename, 'wb') as fp:
                my_conn.retrieveFile(cfg.shared_folder, cfg.root_folder + file.filename, fp)
    my_conn.close()
