# -*- coding: utf-8 -*-

# Thank you http://sametmax.com/ecrire-des-logs-en-python/

import os
import shutil
import sys
import logging
import logging.config

path_logs = os.path.join(os.path.expanduser("~"), "myLogs", "Logs")
dictconf = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'complete': {
            'format': '%(asctime)s\t%(filename)s:%(lineno)d\t%(name)s\t%(levelname)s\t%(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'standard': {
            'format': '%(asctime)s\t%(message)s',
            'datefmt': "%H:%M:%S",
        },
        'basic': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': 'DEBUG',
            'formatter': 'complete',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(path_logs, 'LiteATS_U500.log'),
            'encoding': 'utf8',
            'maxBytes': 10240000,
            'backupCount': 1,
        },
        'scenario_file': {
            'level': 'INFO',
            'formatter': 'basic',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(path_logs, 'scenario.log'),
            'encoding': 'utf8',
            'maxBytes': 10240000,
            'backupCount': 1,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': 'DEBUG',
        },
        'console': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'file': {
            'handlers': ['rotate_file'],
            'level': 'DEBUG',
        },
        'logs_scenario': {
            'handlers': ['scenario_file'],
            'level': 'DEBUG',
        },
    }
}

# Cleans logging directory
if os.path.exists(path_logs):
    shutil.rmtree(path_logs)
os.makedirs(path_logs)

# logger = logging.getLogger()
logging.config.dictConfig(dictconf)
logger = logging.getLogger()


def en_cas_de_plantage(type_except, value, tb):
    # Traceback permettra de formater l'exception.
    import traceback
    # Mise en forme de l'exception. Retourne la trace
    #  sous forme de str avec numéros de lignes et tout
    trace = "".join(traceback.format_exception(type_except, value, tb))
    # On loggue l'exception au niveau "critique",
    #  elle sera donc envoyée par email
    logger.critical(u"Erreur inattendue:\n%s", trace)
    # ... et on laisse le script se planter...
    sys.__excepthook__(type_except, value, tb)

# on remplace sys.excepthook, et le tour est joué
sys.excepthook = en_cas_de_plantage



