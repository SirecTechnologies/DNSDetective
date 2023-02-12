# dns_detective_dmarc_service.py

import json
import checkdmarc
from dns_detective_database_service import DNSDetectiveDatabase

class DNSDetectiveDMARC:
    def __init__(self, domain_name, debug=False):
        self.domain_name = domain_name
        self.database = DNSDetectiveDatabase(db_name='dns_detective.db')
        self.dmarc_report = None
        self.debug = debug
        self.include_descriptions = False

    def run(self):
        descriptions = {
        # dictionary of parameters to collect and display
            "v": "Version of DMARC protocol",
            "p": "Policy for email receivers to follow",
            "rua": "URI for aggregated DMARC reports",
            "ruf": "URI for forensic DMARC reports",
            "fo": "Failure reporting options",
            "adkim": "Alignment mode for DKIM signature",
            "aspf": "Alignment mode for SPF authentication",
            "pct": "Percentage of messages subject to DMARC policy",
            "rf": "Requested format for DMARC failure reports",
            "ri": "Interval in seconds for generating DMARC reports",
            "sp": "Subdomain policy for DMARC"
        }
        try:
            dmarc_record = checkdmarc.parse_dmarc_record("sirec.co.uk", include_tag_descriptions=self.include_descriptions)
            dmarc_record = json.dumps(dmarc_record)
            dmarc_record = json.loads(dmarc_record)
            print(dmarc_record)
        except Exception as e:
            print(f"Error retrieving DMARC record for {self.domain_name}: {e}")
            return

    def store_dmarc_report(self):
        # we'll store our output to the database after we get the correct information extracted and displayed to screen.
        pass

    def close(self):
        self.database.close()