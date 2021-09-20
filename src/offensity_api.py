import click
import sys
import logging
from datetime import datetime

import utils


log = logging.getLogger(__name__)


"""
    Offensity API Python3 Script - Please note: currently only "GET"-requests are supported!
"""


@click.command()
@click.option("--token", required=True, type=str, help="Offensity API Token")
@click.option("--rate-limit", required=False, type=int, default=100,
              help="Maximum allowed rate-limit is: 100 requests per second per user")
@click.option("--latest-report-only", is_flag=True, required=False, default=False, help="Get only the latest report")
@click.option("--get-only-reports", required=False, is_flag=True, help="Get only reports")
@click.option("--get-only-scanprofiles", required=False, is_flag=True, help="Get only scanprofiles")
@click.option("--verbose", required=False, is_flag=True, help="Set the logging level to INFO")
def main(token, rate_limit, latest_report_only, get_only_reports, get_only_scanprofiles, verbose):
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    found_reports_list = list()
    found_scanprofiles_list = list()

    utils.API_TOKEN = token

    try:
        if rate_limit:
            if 0 < rate_limit <= 100:
                utils.RATE_LIMIT = rate_limit
            else:
                raise ValueError
    except ValueError:
        log.error("Please make sure that the rate-limit is within the range: 0 < X <= 100")
        sys.exit(-1)

    if not get_only_reports and not get_only_scanprofiles:
        found_reports_list = utils.get_reports(latest_report_only)
        found_scanprofiles_list = utils.get_scanprofiles()

    if get_only_reports:
        found_reports_list = utils.get_reports(latest_report_only)

    if get_only_scanprofiles:
        found_scanprofiles_list = utils.get_scanprofiles()

    # Here you are able to work with the list of report objects the way you prefer :)
    # For demonstration purpose it will be saved as .json file -> therefore we need each Report object as dict
    time_now = datetime.now()
    timestamp = f"{time_now.year}{time_now.month}{time_now.day}_{time_now.hour}{time_now.minute}{time_now.second}"

    final_reports = [
        report.get_dict() for report in found_reports_list
    ]

    if final_reports:
        reports_file_name = f"offensity_api_reports_{timestamp}.json"
        utils.export_to_json(filename=reports_file_name, data=final_reports)

    final_scanprofiles = [
        scanprofile.get_dict() for scanprofile in found_scanprofiles_list
    ]

    if final_scanprofiles:
        scanprofiles_file_name = f"offensity_api_scanprofiles_{timestamp}.json"
        utils.export_to_json(filename=scanprofiles_file_name, data=final_scanprofiles)


if __name__ == "__main__":
    main()
