from datetime import datetime
from time import time

class bcolors:
    WHITE = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

all_context = {
    'progress':bcolors.HEADER,
    'white':bcolors.WHITE,
    'info':bcolors.WARNING,
    'flag':bcolors.OKGREEN,
    'log':bcolors.OKBLUE,
    'error':bcolors.FAIL,
    'warning':bcolors.OKCYAN,
    '':''
}


def logger(message,context='',newline=0,tab=0,json=False,time=True):
    final = ""
    if(json):
        final = '{"%s":"%s"}'%(context,message)
    else:
        final += '\n'*newline
        if(time):
            now = datetime.now()
            final += now.strftime("%H:%M:%S")
            final += " | "
        else:
            final += " " * 8
            final += " |  "
        final += (all_context[context] if context in all_context.keys() else '')
        final += '\t'*tab
        if(time and tab == 0):
            final += ' '
        final += message
        final += bcolors.ENDC

    print(final)
