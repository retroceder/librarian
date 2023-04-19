import colorama

from colorama import Fore
from colorama import Style

colorama.init()


def process(text: str):
    return text\
        .replace('|sbr|', Style.BRIGHT)\
        .replace('|sdm|', Style.DIM)\
        .replace('|rst|', Style.RESET_ALL)\
        .replace('|crst|', Fore.RESET)\
        .replace('|cgr|', Fore.GREEN)\
        .replace('|crd|', Fore.RED)


def colprint(text: str):
    print(process(text) + Style.RESET_ALL)
