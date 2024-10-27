from datetime import datetime, timezone
import logging
import os
from cloudflare import Cloudflare


class CloudflareClient:
    def __init__(self) -> None:
        self._client = Cloudflare(
            api_email=os.environ.get("CLOUDFLARE_EMAIL"),
            api_key=os.environ.get("CLOUDFLARE_API_KEY"),
            max_retries=3,
        )
        self._zone_id = os.environ.get("CLOUDFLARE_ZONE_ID")
        self._dns_names_to_update = os.environ.get(
            "CLOUDFLARE_DOMAINS_TO_UPDATE", ""
        ).split(",")
        self._logger = logging.getLogger("dynamic_ip_updater")

    def get_current_ip_alias_in_website_dns(self, web_domain_name: str) -> str:
        dns_record = self._client.dns.records.list(
            zone_id=self._zone_id, type="A", name=web_domain_name
        ).to_dict()

        if len(dns_record.get("result", [])) <= 0:
            self._logger.info(f"Records not found for webdomain: {web_domain_name}")
            raise Exception(f"Records not found for webdomain {web_domain_name}")

        return dns_record["result"][0].get("content")

    def update_alias_websites_with_public_ip(self, new_ip: str):
        dns_records = self._client.dns.records.list(
            zone_id=self._zone_id, type="A"
        ).to_dict()
        current_utc_time = datetime.now(timezone.utc)

        for dns in dns_records["result"]:
            if dns["name"] in self._dns_names_to_update:
                self._logger.info(f"Updating domain {dns["name"]} with new ip {new_ip}")
                self._client.dns.records.update(
                    dns_record_id=dns["id"],
                    zone_id=self._zone_id,
                    name=dns["name"],
                    content=new_ip,
                    type="A",
                    proxied=dns["proxied"],
                    comment=f"Updated by cloudflare_dynamic_ip_updater script at {current_utc_time.ctime()}",
                )
