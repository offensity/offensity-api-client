import sys
import logging
import requests
from ratelimit import limits, sleep_and_retry
from ratelimit.exception import RateLimitException
from urllib.parse import urljoin
import json

from models import Report, ScanProfile, ReportInfrastructure, Issue

log = logging.getLogger(__name__)


# GLOBAL VARS
API_ROOT_URL = "https://reporting.offensity.com/api/v1/"
TOKEN_MANAGEMENT_URL = "https://reporting.offensity.com/accounts/apitokens/"

ONE_MINUTE = 60
LATEST_RESULT_ONLY = False
API_TOKEN = ""
RATE_LIMIT = 100


@sleep_and_retry
@limits(calls=RATE_LIMIT, period=ONE_MINUTE)
def send_request(url: str) -> dict:
    # Set needed headers
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Accept": "application/json"
    }

    try:
        # Send request to API endpoint
        api_response = requests.get(url, headers=headers, verify=True, allow_redirects=True)

        # Check if authentication failed
        if api_response.status_code == 401:
            log.error(f"401 Unauthorized: Please check your API-Token @ {TOKEN_MANAGEMENT_URL}")
            sys.exit(-1)

        # Check if ratelimit was exceeded
        elif api_response.status_code == 429:
            log.warning("You exceeded your ratelimit! Only a 100 requests per second per user are allowed!")
            raise RateLimitException

        # Return json object if SUCCESS
        elif api_response.status_code == 200:
            return api_response.json()

        # Show error message in any other case
        else:
            log.error(f"Received the following status_code: {api_response}. Please troubleshoot!")

    except Exception as exception_message:
        log.error(f"An Exception occurred while sending the request:\n{exception_message}")


def more_results_available(result_list: dict) -> tuple:
    if result_list.get("next"):
        log.info(f"More results are available - go to next page!\n")
        return True, result_list.get("next")

    log.info("No more results available")
    return False, None


def get_results(page_url, object_class_type, results_set=None, **kwargs) -> list:
    page_results = send_request(page_url)
    results_set = results_set if results_set else list()

    latest_report_only = kwargs.get("latest_report_only", False)  # TODO

    # iterate results json and add each object type to list
    for result in page_results.get("results", []):
        results_set.append(
            object_class_type.from_query_result(result)  # object init
        )
    else:
        # check if more results are available -> 10 results per page
        # more_pages_available, next_page_url = more_results_available(page_results)
        # if more_pages_available:
        #     # Recursive function call!
        #     return get_results(
        #         page_url=next_page_url,
        #         object_class_type=object_class_type,
        #         results_set=results_set,
        #     )
        pass

    return results_set


def get_reports(latest_report_only: bool) -> list:
    reports_start_url = urljoin(API_ROOT_URL, "reports/?status=success")

    log.info("Start fetching reports...")
    report_results = get_results(
        page_url=reports_start_url,
        object_class_type=Report,
        latest_report_only=latest_report_only,
    )
    log.info(f"{len(report_results)} reports fetched!")

    for report_object in report_results:
        log.info(f"Fetching infrastructure data & issues for report: {report_object.id}")
        report_object.report_infrastructure = get_report_infrastructure(report_object.infrastructure_url)
        log.info("Gathered all infrastructure data!")
        report_object.report_issues = get_report_issues(report_object.details_url)
        log.info(f"Found {len(report_object.report_issues)} issues!\n")

    return report_results


def get_report_infrastructure(report_infrastructure_url: str) -> list:
    report_infrastructure = get_results(
        page_url=report_infrastructure_url,
        object_class_type=ReportInfrastructure
    )

    return report_infrastructure or list()


def get_report_issues(report_details_url: str) -> list:
    issues_set = list()

    # single page result, therefore no recursive calls necessary
    report_details = send_request(report_details_url)

    report_issues = report_details.get("issues", list())
    if not report_issues:
        log.info("No issues found.")

    for issue in report_issues:
        issues_set.append(
            Issue.from_query_result(issue)  # object init
        )

    return issues_set


def get_scanprofiles() -> list:
    scanprofiles_start_url = urljoin(API_ROOT_URL, "scanprofiles/")

    log.info("Start fetching scanprofiles...")
    scanprofiles_results = get_results(
        page_url=scanprofiles_start_url,
        object_class_type=ScanProfile
    )

    log.info(f"{len(scanprofiles_results)} scanprofiles fetched!")

    return scanprofiles_results


def export_to_json(filename: str, data: list):
    with open(filename, "w") as outfile:
        outfile.write(
            json.dumps(data, sort_keys=True, indent=4)
        )
    log.info(f"Exported reports to: {filename}")
