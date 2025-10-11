import logging

from fastapi import Request


class LogHandler:
    __logger: logging.Logger | None = None

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if not cls.__logger:
            cls.__logger = logging.getLogger(name)
            cls.__logger.setLevel(logging.DEBUG)
            cls.__logger.addHandler(logging.StreamHandler())

        return cls.__logger


def get_logger(request: Request) -> logging.Logger:
    return LogHandler.get_logger(request.scope["route"].name)
