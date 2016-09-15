#!/usr/bin/python
# -*- coding: utf8 -*-

import argparse
import os
import fnmatch
import re
import shutil

# PARSER

DEFAULT_MODE = 1
DEFAULT_WRAP = "__"

parser = argparse.ArgumentParser(
    description='Rename/remove files according to environment code before deploy'
)
parser.add_argument(
    '-e',
    '--environment',
    required=True,
    help='Selected environment'
)
parser.add_argument(
    '-p',
    '--path',
    required=True,
    help='Project root path'
)
parser.add_argument(
    '-w',
    '--wrap',
    type=str,
    nargs='?',
    const=DEFAULT_WRAP,
    default=DEFAULT_WRAP,
    help='Character wrapping environment name'
)
parser.add_argument(
    '-m',
    '--mode',
    type=int,
    nargs='?',
    const=DEFAULT_MODE,
    default=DEFAULT_MODE,
    help='Location of environment code in filename. 0 is before, 1 is just before the extension and 2 is at the end.'
)
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Print what has been renamed or deleted'
)
args = parser.parse_args()

# Generate codes from wrap character and environment name
CODE_ENV = "{}{}{}".format(
    args.wrap,
    args.environment,
    args.wrap
)
CODE_WILDCARD_ENV = "{}{}{}".format(
    args.wrap,
    "*",
    args.wrap
)

# FUNCTIONS


def lremove(pattern, string):
    """
    Remove 'pattern' in 'string' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, '', string)


def rremove(pattern, string):
    """
    Remove 'pattern' in 'string' if 'pattern' ends 'string'.
    """
    return re.sub('%s$' % pattern, '', string)


def deletePath(path):
    """
    Same function to remove either file or folder
    """
    if os.path.exists(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except:
            pass


def doBeginning(path, file_path, file_name, file_extension):
    """
    Rename or delete files when environment code is at the
    beginning of the file name
    """
    if fnmatch.fnmatch(file_name, CODE_ENV + "*"):
        new_file_name = lremove(CODE_ENV, file_name)
        new_path = file_path + "/" + new_file_name + file_extension
        if args.verbose:
            print("rename {} to {}".format(path, new_path))
        deletePath(new_path)
        os.rename(path, new_path)
    elif fnmatch.fnmatch(file_name, CODE_WILDCARD_ENV + "*"):
        if args.verbose:
            print("delete {}".format(path))
        deletePath(path)


def doBeforeExtension(path, file_path, file_name, file_extension):
    """
    Rename or delete files when environment code is before
    extension in file name
    """
    if fnmatch.fnmatch(file_name, "*" + CODE_ENV):
        new_file_name = rremove(CODE_ENV, file_name)
        new_path = file_path + "/" + new_file_name + file_extension
        if args.verbose:
            print("rename {} to {}".format(path, new_path))
        deletePath(new_path)
        os.rename(path, new_path)
    elif fnmatch.fnmatch(file_name, "*" + CODE_WILDCARD_ENV):
        if args.verbose:
            print("delete {}".format(path))
        deletePath(path)


def doEnd(path, file_path, file_name, file_extension):
    """
    Rename or delete files when environment code is at the
    end of file name
    """
    file_name_extension = file_name + file_extension
    if fnmatch.fnmatch(file_name_extension, "*" + CODE_ENV):
        new_file_name = rremove(CODE_ENV, file_name_extension)
        new_path = file_path + "/" + new_file_name
        if args.verbose:
            print("rename {} to {}".format(path, new_path))
        deletePath(new_path)
        os.rename(path, new_path)
    elif fnmatch.fnmatch(file_name_extension, "*" + CODE_WILDCARD_ENV):
        if args.verbose:
            print("delete {}".format(path))
        deletePath(path)


def processPath(path):
    """
    Process path and choose the good method
    """
    file_path = path.rpartition("/")[0]
    file_name = path.rpartition("/")[2]
    file_extension = ""
    if "." in file_name:
        file_extension = file_name.rpartition(".")[1] + file_name.rpartition(".")[2]
    file_name = rremove(file_extension, file_name)

    # Code at the beginning of the filename
    if args.mode == 0:
        doBeginning(path, file_path, file_name, file_extension)
    # Code just before extension
    elif args.mode == 1:
        doBeforeExtension(path, file_path, file_name, file_extension)
    # Code at the end of the filename
    elif args.mode == 2:
        doEnd(path, file_path, file_name, file_extension)

# PROCESS FILES

for root, dirs, files in os.walk(args.path, topdown=False):
    for name in files:
        processPath(os.path.join(root, name))
    for name in dirs:
        processPath(os.path.join(root, name))
