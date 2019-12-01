import logging


def setup_custom_logger(name: str):
    """
    커스텀 로그 생성
    """
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s][%(module)s] %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger