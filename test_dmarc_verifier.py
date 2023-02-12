# test_dmarc_verification.py
import sys
from dns_detective_dmarc_service import DNSDetectiveDMARC

if __name__ == "__main__":
    domain_name = sys.argv[1]
    debug = False
    if len(sys.argv) > 2 and sys.argv[2] == "debug":
        debug = True

    dns_detective = DNSDetectiveDMARC(domain_name, debug)
    dns_detective.run()
    dns_detective.database.close()
