# Sets up logging.
import os, sys
import logging

sLogLevel = os.environ.get('LOG_LEVEL', 'INFO').upper()
log_level    = 20

if (sLogLevel == 'CRITICAL'):
    log_level = 50
if (sLogLevel == 'ERROR'):
    log_level = 40
if (sLogLevel == 'WARNING'):
    log_level = 30
if (sLogLevel == 'INFO'):
    log_level = 20
if (sLogLevel == 'DEBUG'):
    log_level = 10

logging.basicConfig(stream=sys.stdout, level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")