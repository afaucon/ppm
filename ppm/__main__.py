import argparse

import ppm.api


def main_procedure():
    parser = argparse.ArgumentParser(prog=ppm.__info__.__package_name__, 
                                     description=ppm.__info__.__description__)

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
    subparsers.add_parser('reports')

    # Develop command
    parser_vscode = subparsers.add_parser('develop')
    parser_vscode.add_argument('program')
    parser_vscode.add_argument('name')

    args = parser.parse_args()

    if args.command == "create":
        ppm.api.create_package("package_name")
        ppm.api.create_application("application_name")
    if args.command == "list":
        ppm.api.list()
    if args.command == "report":
        ppm.api.report("package_name or application_name")
    if args.command == "reports":
        ppm.api.reports()
    if args.command == "develop":
        ppm.api.develop("vscode", "package_name or application_name")

if __name__ == "__main__":
    main_procedure()