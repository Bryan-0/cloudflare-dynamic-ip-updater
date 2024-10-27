import logging
import os
from clients.cloudflare import CloudflareClient
from helpers import env, logging_config
from clients.ip import IPv4


logger = logging.getLogger("dynamic_ip_updater")


def main():
    logger.info("Starting dynamic ip updater check process...")

    cloudflare = CloudflareClient()
    current_public_ip = IPv4.get_public_ip()
    cloudflare_dns_ip = cloudflare.get_current_ip_alias_in_website_dns(
        web_domain_name=os.environ.get("CLOUDFLARE_WEBDOMAIN_TO_CHECK")
    )

    if current_public_ip == cloudflare_dns_ip:
        logger.info(
            "Public IP matching with Cloudflare DNS configured IP, stopping process..."
        )
        return

    cloudflare.update_alias_websites_with_public_ip(current_public_ip)


if __name__ == "__main__":
    main()
