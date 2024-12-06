import logging
import logging.handlers

class Logger():
    def __init__(self):
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.DEBUG)
        logging.getLogger('discord.http').setLevel(logging.INFO)

        handler = logging.handlers.RotatingFileHandler(
            filename='discord.log',
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,
            backupCount=5,
        )
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
    
    def getLogger(self):
        return self.logger
    

logger = Logger().getLogger()