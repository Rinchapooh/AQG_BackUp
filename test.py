import logging.config

from smb.SMBConnection import SMBConnection

import file_handler

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

# logging.config.fileConfig('logging.conf')

ERROR_LOG_FILENAME = 'AQG_backup.log'
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s:%(name)s:%(process)d:%(lineno)d %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(message)s'
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': """
                    asctime: %(asctime)s
                    created: %(created)f
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    message: %(message)s
                    module: %(module)s
                    msec: %(msecs)d
                    name: %(name)s
                    pathname: %(pathname)s
                    process: %(process)d
                    processName: %(processName)s
                    relativeCreated: %(relativeCreated)d
                    thread: %(thread)d
                    threadName: %(threadName)s
                    exc_info: %(exc_info)s
                    """,
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'logfile': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOG_FILENAME,
            'backupCount': 2,

        },
        'verbose_output': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'json': {
            'formatter': 'json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'first': {

            'level': 'DEBUG'

        }

    },
    'root': {
        'level': 'INFO',
        'handlers': [
            'verbose_output',
            'logfile'

        ]}
}
logging.config.dictConfig(LOGGING_CONFIG)

cfg = file_handler.load_config('config.json')

def get_connection():
    conn = SMBConnection(cfg.user, cfg.password, cfg.client_pc_name, cfg.server_name)
    conn.connect(cfg.server_ip)
    return conn


my_connection = get_connection()

list_path = my_connection.listPath(cfg.shared_folder, cfg.root_folder, pattern=cfg.file_mask)

for x in list_path:
    print(x.filename)
