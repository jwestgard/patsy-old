#!/usr/bin/env python3 

import argparse
import csv
import logging
import os
import sqlite3
import sys
import subcommands


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    '''Parse args and set the chosen sub-command as the default function.'''
    # main parser for command line arguments
    parser = argparse.ArgumentParser(
                    description='PATSy: Preservation Asset Tracking System.'
                    )
    parser.add_argument('-v', '--version', 
                    action='version', 
                    help='Print version number and exit',
                    version='PATSy v0.1'
                    )
    parser.add_argument('-c', '--config',
                    action='store',
                    help='Path to the database configuration',
                    required=True
                    )
    subparsers = parser.add_subparsers(title='subcommands', 
                    description='valid subcommands', 
                    help='-h additional help',
                    dest='cmd',
                    required=True
                    )
    # parser for the "create" sub-command
    create_parser = subparsers.add_parser('create', 
                    help='Load assets to the database',
                    description='Load manifest of assets to the database.'
                    )
    create_parser.add_argument('path',
                    help='path to data file',
                    action='store'
                    )
    # parser for the "read" sub-command
    create_parser = subparsers.add_parser('read', 
                    help='Query the database and display results list',
                    description='.'
                    )
    create_parser.add_argument('path',
                    help='path to data file',
                    action='store'
                    )
    # parser for the "update" sub-command
    create_parser = subparsers.add_parser('update', 
                    help='Modify records of assets in the database',
                    description='.'
                    )
    create_parser.add_argument('path',
                    help='path to data file',
                    action='store'
                    )
    # parser for the "delete" sub-command
    create_parser = subparsers.add_parser('delete', 
                    help='Remove assets from the database',
                    description='.'
                    )
    create_parser.add_argument('path',
                    help='path to data file',
                    action='store'
                    )
    # parse the args and call the subcommand as specified
    args = parser.parse_args()
    subcommand = getattr(subcommands, args.cmd)
    subcommand(args)

if __name__ == '__main__':
    main()