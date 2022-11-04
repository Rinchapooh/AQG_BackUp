import json
import logging
from types import SimpleNamespace
from smb.SMBConnection import SMBConnection


ERROR_LOG_FILENAME = 'AQG_backup.log'
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
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
        'smb': {
            'level': 'DEBUG',
            'handlers': ['verbose_output']
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


def load_config(filename: str) -> object:
    try:
        with open(filename, 'r') as fb:
            return json.load(fb, object_hook=lambda d: SimpleNamespace(**d))
    except FileNotFoundError as e:
        print('fnf')
        logging.debug(f'Load config file: {e.strerror}')
        return
    except json.decoder.JSONDecodeError as e:
        print('pars')
        logging.debug(f'Parsing config file: {e.msg}')
        return


def get_connection(cfg):

    try:

        conn = SMBConnection(cfg.user1, cfg.password, cfg.client_pc_name, cfg.server_name)
        conn.connect(cfg.server_ip, timeout=5)
        logging.debug(conn)

        return conn


    except Exception as e:
        print(e)
        logging.getLogger('smb')
        logging.debug(e)

