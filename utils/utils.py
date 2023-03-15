import argparse
from os.path import exists

def parse_args():
    parser = argparse.ArgumentParser(add_help=True, description='This tool is used to debug brainfuck code')
    parser.add_argument("-f","--file",dest="file",type=str,required=True,help="File: *.bf")
    return parser.parse_args()

def check_file(file):
    return exists(file)

def check_content(code):
    return len([x for x in code 
        if x not in '<>+-.,][']) == 0
