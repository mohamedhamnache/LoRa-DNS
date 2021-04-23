import coloredlogs, logging

logger = logging.getLogger("LA")
coloredlogs.install(level="DEBUG", logger=logger)
