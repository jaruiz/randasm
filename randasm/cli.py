#!/usr/bin/env python

import argparse
import yaml
import glob
import os
import sys
import pkg_resources

import srcgen


# Name of package subdirectory that contains the package data.
TARGETS_DIR = "targets"


def _parse_cmdline():

    targets = _find_available_targets()

    parser = argparse.ArgumentParser(
        description='Build random assembly program source for the specified target (CPU/Assembler)',
        epilog="See README.md for a longer description, including an explanation of the target file format.")
    parser.add_argument('--target', 
        help="select one of the predefined targets", 
        choices=targets)
    parser.add_argument('--target-def', metavar="FILE", type=str,
        help="select user-supplied target definition file")
    parser.add_argument('-n', '--num', metavar="NUM", type=int, default=100,
        help="number of instructions")
    parser.add_argument('--raw', action="store_true", default=False,
        help="emit only random instructions with no assembly wrapper")

    args = parser.parse_args()
    if not args.target and not args.target_def:
        print >> sys.stderr, "Missing target; either '--target' or '--target-def' options must be supplied.\n"
        parser.print_help()
        sys.exit(1)

    return args


def _find_available_targets():
    # Target names are just the target file names with no extension.
    target_filenames = pkg_resources.resource_listdir(__name__, TARGETS_DIR)
    target_names = [os.path.splitext(x)[0] for x in target_filenames]
    return target_names


def _load_target_data(target_path):

    try:
        fs = pkg_resources.resource_stream(__name__, target_path)
        data = yaml.load(fs)
        data['filename'] = target_path
    except IOError as e:
        print >> sys.stderr, str(e)
        sys.exit(1)
    except yaml.scanner.ScannerError as e:
        print >> sys.stderr, "Error in target declaration YAML file: " + str(e)
        sys.exit(2)
    finally:
        fs.close()
    return data

def main():
    opts = _parse_cmdline()
    if opts.target:
        target_path = os.path.join(TARGETS_DIR, opts.target) + ".yaml"
    else:
        target_path = ""
    target_data = _load_target_data(target_path)
    asm = srcgen.build_source(target_data, opts.num, opts.raw)
    print asm

    

    
