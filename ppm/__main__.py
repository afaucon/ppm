import argparse

from ppm import __info__
from ppm import module


def main_procedure():
    parser = argparse.ArgumentParser(prog=__info__.__package_name__, description=__info__.__description__)

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('type', choices=['package', 'app'])
    parser_create.add_argument('name')

    # List command
    subparsers.add_parser('list')

    # Report command
    parser_report = subparsers.add_parser('report')
    parser_report.add_argument('name')

    # Reports command
    parser_reports = subparsers.add_parser('reports')

    # Develop command
    parser_vscode = subparsers.add_parser('develop')
    parser_vscode.add_argument('program')
    parser_vscode.add_argument('name')

    args = parser.parse_args()

    module.run()

if __name__ == "__main__":
    main_procedure()