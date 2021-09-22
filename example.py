import click
import logging
import json
from datetime import datetime

from offensity_api_client import OffensityApiClient

log = logging.getLogger(__name__)


"""
    Offensity API Python3 Script - Please note: currently only "GET"-requests are supported!
"""


def export_to_json(filename: str, data: list):
    time_now = datetime.now()
    timestamp = f"{time_now.year}{time_now.month}{time_now.day}_{time_now.hour}{time_now.minute}{time_now.second}"

    filename += f"_{timestamp}.json"

    with open(filename, "w") as outfile:
        outfile.write(
            json.dumps(data, sort_keys=True, indent=4)
        )
    log.info(f"Successfully exported to: {filename}")


@click.command()
@click.option("--token", required=True, type=str, help="Offensity API Token")
@click.option("--verbose", required=False, is_flag=True, help="Set the logging level to INFO")
def main(token, verbose):
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)

    api_client = OffensityApiClient(token=token)

    enabled_scanprofiles = api_client.scanprofiles_list(is_enabled=True)

    amount_of_running_scans = len(list(api_client.report_list(status="started")))
    log.info(f"Currently are {amount_of_running_scans} scan(s) in progress!")

    for scanprofile in enabled_scanprofiles:
        tld_domain = scanprofile.get("domain")
        scanprofile_id = scanprofile.get("id")

        all_reports_per_scanprofile_finished = api_client.report_list_for_scanprofile(scanprofile_id=scanprofile_id)

        for report in all_reports_per_scanprofile_finished:
            report_id = report.get("id")
            issue_count = report.get("issue_count")

            log.info(f"The report with ID: {report_id} ({tld_domain}) has {issue_count} issues!")
            issues_per_report = api_client.issues(report_id=report_id)
            for issue in issues_per_report:
                log.info(f"\t\t*) {issue.get('data', dict()).get('title', '')}")

            systems_with_open_port_21 = api_client.infrastructure_data(
                report_id=report_id,
                query="port:21"
            )
            log.info(f"The scanprofile >>{tld_domain}<< has {len(list(systems_with_open_port_21))} open port 21!")

            # export as .json file
            export_to_json(report_id, report)


if __name__ == "__main__":
    main()
