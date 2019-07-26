import argparse

from ppm import __info__
from ppm import module


def main_procedure():
    parser = argparse.ArgumentParser(description=__info__.__description__)

    subparsers = parser.add_subparsers(required=True)

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('type', choices=['package', 'app'])
    parser_create.add_argument('name')

    parser_list = subparsers.add_parser('list')

    parser_report = subparsers.add_parser('report')
    parser_report.add_argument('name')

    parser_reports = subparsers.add_parser('reports')

    parser_vscode = subparsers.add_parser('vscode')
    parser_vscode.add_argument('name')

    args = parser.parse_args()

    module.run()

if __name__ == "__main__":
    main_procedure()