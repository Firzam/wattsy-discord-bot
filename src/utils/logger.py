import logging

# Disable logging for the root logger to prevent default/basic logs
logging.getLogger().handlers.clear()

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

logger = logging.getLogger(__name__)