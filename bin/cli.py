#!/usr/bin/env python3 

import argparse
import csv
import logging
import os
import sqlite3
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def load(args):
    print(f'load with args: {args}')

def main():

    '''Parse args and set the chosen sub-command as the default function.'''

    # main parser for command line arguments
    parser = argparse.ArgumentParser(
                    description='PATSy: Preservation Asset Tracking System.'
                    )
    parser.add_argument(
                    '-v', '--version', 
                    action='version', 
                    help='Print version number and exit',
                    version='PATSy v0.1'
                    )
    parser.add_argument(
                    '-c', '--config',
                    action='store',
                    help='Path to the database configuration'
                    )
    subparsers = parser.add_subparsers(
                    title='subcommands', 
                    description='valid subcommands', 
                    help='-h additional help', 
                    metavar='{load}',
                    dest='cmd',
                    required=True
                    )

    # parser for the "load" sub-command
    load_parser = subparsers.add_parser(
                    'load', 
                    help='Load assets to the database',
                    description='Read a spreadsheet of data and it load to the database.'
                    )
    load_parser.add_argument(
                    'path',
                    help='path to data file',
                    action='store'
                    )
    load_parser.set_defaults(func=load)

    # parse the args and call the default sub-command function
    args = parser.parse_args()
    # print_header(args.func.__name__)
    args.func(args)

if __name__ == '__main__':
    main()