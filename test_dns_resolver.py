# test_dns_resolver.py
import sys

from dns_detective_resolver_service import DNSDetectiveResolver

if __name__ == "__main__":
    domain_name = sys.argv[1]
    record_type = sys.argv[2]
    debug = False
    if len(sys.argv) > 3 and sys.argv[3] == "debug":
        debug = True

    dns_detective = DNSDetectiveResolver(domain_name, record_type, debug)
    dns_detective.run()
    dns_detective.database.close()
