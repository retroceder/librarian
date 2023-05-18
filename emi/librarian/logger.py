import time
from threading import Lock

import colorama
from colorama import Fore
from colorama import Style

COLOR_EXTENSIONS = [
    {"ext": "br", "sub_open": Style.BRIGHT, "sub_close": Style.RESET_ALL},
    {"ext": "dim", "sub_open": Style.DIM, "sub_close": Style.RESET_ALL},
    {"ext": "gr", "sub_open": Fore.GREEN, "sub_close": Fore.RESET},
    {"ext": "rd", "sub_open": Fore.RED, "sub_close": Fore.RESET},
    {"ext": "bl", "sub_open": Fore.BLUE, "sub_close": Fore.RESET},
]


def local_time_str():
    """Метод получения отформатированного локального времени."""
    return time.strftime("%d %b %Y %H:%M:%S", time.localtime())


def process_color_extensions(text: str):
    """Обработка цветовых расширений текста."""
    for params in COLOR_EXTENSIONS:
        text = text.replace('<{}>'.format(params["ext"]), params["sub_open"])
        text = text.replace('</{}>'.format(params["ext"]), params["sub_close"])

    return text


def remove_color_extensions(text: str):
    """Удаление цветовых расширений текста."""
    for params in COLOR_EXTENSIONS:
        text = text.replace('<{}>'.format(params["ext"]), "")
        text = text.replace('</{}>'.format(params["ext"]), "")

    return text


class Logger:
    """Объект для синхронизированного вывода в консоль."""
    def __init__(self, add_timestamp=False):
        """Конструктор.

        Аргументы:
        path -- путь до файла журнала
        """
        self.lock = Lock()
        self.add_timestamp = add_timestamp
        colorama.init()

    def log(self, message: str, end: str = '\n'):
        """Синхронизированная запись в журнал (консоль)."""
        with self.lock:
            print(process_color_extensions("{}{}".format('[{}] '.format(local_time_str()) if self.add_timestamp else '',
                                                         message)), end=end)
