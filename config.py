
import logging


DB_NAME = "golden-eye.db"


HTTP_TIMEOUT = 15

IP_LIST = ['82.117.234.127', '127.0.0.2', '127.0.0.1', '176.115.99.211', '10.41.255.55', '192.168.1.46']

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': "[%(asctime)s] [%(levelname)s] - %(name)s: %(message)s"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'new.log'
        },
    },
    'loggers': {
        'GoldenEye': {
            'handlers': ['file', ],
            'level': logging.DEBUG
        },
        'Api': {
            'handlers': ['file', ],
            'level': logging.DEBUG
        },
        'Tasks': {
            'handlers': ['file', ],
            'level': logging.DEBUG
        }
    }
}










