from dataclasses import dataclass, asdict
import logging

log = logging.getLogger(__name__)


@dataclass()
class Report:
    # init
    id: str = ""
    status: str = ""
    issue_count: int = 0
    created: str = ""
    started: str = ""
    finished: str = ""
    risk_scores: dict = None
    infrastructure_url: str = ""
    details_url: str = ""
    scanprofile_url: str = ""

    # more information -> will not be fetched during init
    report_issues: list = None
    report_infrastructure: list = None

    @classmethod
    def from_query_result(cls, report_result):
        init_kwargs = {
            "id": report_result.get("id"),
            "status": report_result.get("status"),
            "issue_count": report_result.get("issue_count", 0),
            "created": report_result.get("created"),
            "started": report_result.get("started"),
            "finished": report_result.get("finished"),
            "risk_scores": report_result.get("risk_scores", dict()),
            "infrastructure_url": report_result.get("infrastructure"),
            "details_url": report_result.get("detail"),
            "scanprofile_url": report_result.get("scanprofile"),
        }
        return Report(**init_kwargs)

    def get_dict(self):
        return asdict(self)


@dataclass()
class ScanProfile:
    # init
    id: str = ""
    name: str = ""
    is_verified: bool = ""
    is_enabled: bool = ""
    domain: str = ""
    subdomains: list = None
    report_count: int = 0
    reports_url: str = ""

    @classmethod
    def from_query_result(cls, scanprofile_result):
        init_kwargs = {
            "id": scanprofile_result.get("id"),
            "name": scanprofile_result.get("name"),
            "is_verified": scanprofile_result.get("is_verified"),
            "is_enabled": scanprofile_result.get("is_enabled"),
            "domain": scanprofile_result.get("domain"),
            "subdomains": scanprofile_result.get("subdomains", list()),
            "report_count": scanprofile_result.get("report_count", 0),
            "reports_url": scanprofile_result.get("reports"),
        }
        return ScanProfile(**init_kwargs)

    def get_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class ReportInfrastructure:
    # init
    domain: str = ""
    subdomain: str = ""
    enabled: bool = False
    ports: list = None
    nameservers: list = None
    mailservers: list = None
    cnames: list = None
    infrastructure_type: str = ""
    report_id: str = ""
    time: str = ""
    ips: list = None

    @classmethod
    def from_query_result(cls, infrastructure_result):
        init_kwargs = {
            "domain": infrastructure_result.get("domain"),
            "subdomain": infrastructure_result.get("subdomain"),
            "enabled": infrastructure_result.get("enabled", False),
            "ports": infrastructure_result.get("ports", list()),
            "nameservers": infrastructure_result.get("nameservers", list()),
            "mailservers": infrastructure_result.get("mailservers", list()),
            "cnames": infrastructure_result.get("cnames", list()),
            "infrastructure_type": infrastructure_result.get("type"),
            "report_id": infrastructure_result.get("report_id"),
            "time": infrastructure_result.get("time"),
            "ips": infrastructure_result.get("ips", list()),
        }
        return ReportInfrastructure(**init_kwargs)

    def get_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Issue:
    # init
    id: str = ""
    plugin_name: str = ""
    vulnerability_id: str = ""
    client_status: str = ""
    risk_scores: dict = None
    cvss: str = ""
    cvss_score: float = 0.0
    data: dict = None

    @classmethod
    def from_query_result(cls, issue_data_result):
        init_kwargs = {
            "id": issue_data_result.get("id"),
            "plugin_name": issue_data_result.get("plugin_name"),
            "vulnerability_id": issue_data_result.get("vulnerability_id"),
            "client_status": issue_data_result.get("client_status"),
            "risk_scores": issue_data_result.get("risk_scores", dict()),
            "cvss": issue_data_result.get("cvss"),
            "cvss_score": issue_data_result.get("cvss_score", 0.0),
            "data": issue_data_result.get("data", dict()),
        }
        return Issue(**init_kwargs)

    def get_dict(self):
        return asdict(self)
    