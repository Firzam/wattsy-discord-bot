import logging

class Logger():
    def __init__(self, name):
        logging.getLogger().handlers.clear()

        FORMAT = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO)

        self.logger = logging.getLogger(name)
    
    def getLogger(self):
        return self.logger