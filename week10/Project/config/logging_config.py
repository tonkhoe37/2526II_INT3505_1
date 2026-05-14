import logging
import logging.handlers
import os
from pythonjsonlogger import jsonlogger
from flask import request


def setup_logging():
    """
    Cấu hình logging cho ứng dụng
    - Log ra console
    - Log ra file JSON
    """

    # Tạo thư mục logs nếu chưa tồn tại
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Formatter JSON
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    # Formatter Console
    console_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File Handler - JSON
    file_handler = logging.handlers.RotatingFileHandler(
        filename="logs/app.log",
        maxBytes=10485760,
        backupCount=10,
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(json_formatter)
    root_logger.addHandler(file_handler)

    # Error File Handler
    error_handler = logging.handlers.RotatingFileHandler(
        filename="logs/app_error.log",
        maxBytes=10485760,
        backupCount=10,
    )

    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(json_formatter)
    root_logger.addHandler(error_handler)

    return root_logger


class RequestLogging:
    """
    Log các HTTP request/response
    """

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.setup_request_logging()

    def setup_request_logging(self):

        @self.app.before_request
        def log_before_request():
            self.logger.info(
                "Incoming request",
                extra={
                    "method": request.method,
                    "path": request.path,
                    "remote_addr": request.remote_addr,
                    "user_agent": str(request.user_agent),
                },
            )

        @self.app.after_request
        def log_after_request(response):
            self.logger.info(
                "Response sent",
                extra={
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "content_length": response.content_length,
                },
            )

            return response

        @self.app.teardown_request
        def teardown_logging(exc=None):
            if exc is not None:
                self.logger.error(
                    "Request failed",
                    extra={"error": str(exc)},
                    exc_info=True,
                )
