import argparse

import ppm.api
import ppm.display


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

    # Develop command
    parser_vscode = subparsers.add_parser('develop')
    parser_vscode.add_argument('program')
    parser_vscode.add_argument('name')

    args = parser.parse_args()

    if args.command == "create":
        if args.type == "package":
            ppm.api.create_package(args.name)
            ppm.display.after_create_package("Package '{}' suscessfully created.".format(args.name))
        if args.type == "app":
            ppm.api.create_app(args.name)
            ppm.display.after_create_app("App '{}' suscessfully created.".format(args.name))
    if args.command == "list":
        projects_list = ppm.api.list()
        ppm.display.after_list(projects_list)
    if args.command == "report":
        report = ppm.api.report(args.name)
        ppm.display.after_report(report)
    if args.command == "develop":
        ppm.api.develop(args.program, args.name)
        ppm.display.after_develop()

if __name__ == "__main__":
    main_procedure()