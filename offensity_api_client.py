from typing import Optional
from urllib.parse import urljoin
import logging
import requests
from ratelimit import limits, sleep_and_retry

log = logging.getLogger(__name__)


class OffensityApiClient:
    API_ROOT_URL = "https://staging-reporting.offensity.com/api/v1/"
    MAX_PAGE_SIZE = 100

    def __init__(self, token: str):
        self.token = token

    @sleep_and_retry
    @limits(calls=100, period=60)
    def _get(self, url: str, **kwargs):
        if not url.startswith("http"):
            url = urljoin(self.API_ROOT_URL, url)

        res = requests.get(
            url=url,
            params=filter(lambda t: t[1] is not None, kwargs.items()),
            headers={
                "Authorization": f"Token {self.token}",
                "Accept": "application/json",
            }
        )
        if res.status_code == 429:
            log.warning("You exceeded your ratelimit! Only a 100 requests per second per user are allowed!")

        res.raise_for_status()
        return res.json()

    def _get_list(self, url: str, limit: Optional[int] = None, **kwargs):
        while (limit is None or limit > 0) and url is not None:
            if limit is not None:
                page_size = min(limit, self.MAX_PAGE_SIZE)
            else:
                page_size = self.MAX_PAGE_SIZE

            page = self._get(url, page_size=page_size, **kwargs)

            if limit is not None:
                limit -= page_size
            url = page.get("next")

            yield from page.get("results", [])
    
    # SCANPROFILES
    def scanprofiles_list(self, is_enabled: Optional[bool] = None, **kwargs):
        return self._get_list("scanprofiles/", is_enabled=is_enabled, **kwargs)

    def scanprofile_details(self, scanprofile_id: str, **kwargs):
        return self._get(f"scanprofiles/{scanprofile_id}/", **kwargs)
    
    # REPORTS
    def report_list(self, status: Optional[str] = "success", **kwargs):
        return self._get_list("reports/", status=status, **kwargs)

    def report_list_for_scanprofile(self, scanprofile_id: str, status: Optional[str] = "success", **kwargs):
        return self._get_list(f"scanprofiles/{scanprofile_id}/reports/", status=status, **kwargs)

    def latest_report_for_scanprofile(self, scanprofile_id: str, status: Optional[str] = "success", **kwargs):
        return next(self.report_list_for_scanprofile(scanprofile_id, status=status, limit=1, **kwargs), None)

    def report_details(self, report_id: str):
        return self._get(f"reports/{report_id}/")

    def issues(self, report_id: str):
        return self.report_details(report_id).get("issues", [])

    def infrastructure_data(self, report_id: str, query: Optional[str] = "", **kwargs):
        return self._get_list(f"reports/{report_id}/infrastructure/", query=query, **kwargs)
