import argparse

from ppm import __info__
from ppm import module


def main_procedure():
    parser = argparse.ArgumentParser(description=__info__.__description__)

    subparsers = parser.add_subparsers()

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('type', choices=['package', 'app'])
    parser_create.add_argument('name')

    parser_create = subparsers.add_parser('list')

    parser_create = subparsers.add_parser('report')
    parser_create.add_argument('name')

    parser_create = subparsers.add_parser('reports')

    module.run()

if __name__ == "__main__":
    main_procedure()