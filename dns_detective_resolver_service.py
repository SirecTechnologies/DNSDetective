import dns.resolver
import socket
import sys
import time

from dns_detective_database_service import DNSDetectiveDatabase
from dns_detective_local import get_local_dns_server

class DNSDetectiveResolver:
    def __init__(self, domain_name, record_type, debug=False):
        self.domain_name = domain_name
        self.type = record_type
        self.debug = debug
        self.database = DNSDetectiveDatabase(db_name='dns_detective.db')
        self.dns_providers = []
        self.local_dns_server = self.get_local_dns_server()
        self.get_dns_providers()

    get_local_dns_server = get_local_dns_server

    def get_dns_providers(self):
        """Get the DNS providers from a file or default list"""
        dns_providers_file = "dns_providers.csv"
        if os.path.exists(dns_providers_file):
            with open(dns_providers_file, "r") as file:
                for line in file:
                    provider, primary_dns, secondary_dns = line.strip().split(",")
                    self.dns_providers.append((provider, primary_dns, secondary_dns))
        else:
            # Default DNS providers
            self.dns_providers.extend([("Google", "8.8.8.8", "8.8.4.4"), ("Cloudflare", "1.1.1.1", "1.0.0.1")])

    def resolve_dns(self, dns_server):
        """Resolve the DNS for the domain and server"""
        resolver = dns.resolver.Resolver()
        try:
            start_time = time.time()
            response = dns.resolver.query(self.domain_name,self.type)
            end_time = time.time()
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            response = None
        except dns.exception.Timeout:
            response = None
        return response, start_time, end_time

    def run(self):
        for provider in self.dns_providers:
            for dns in provider[1:]:
                response, start_time, end_time = self.resolve_dns(dns)
                if response:
                    answers = response.response.answer
                    if answers:
                        for rdata in answers:
                            dns_lookup = {
                                'domain': self.domain_name,
                                'dns_server': dns,
                                'request_timestamp': str(start_time),
                                'response_timestamp': str(end_time),
                                'response': rdata.to_text()
                            }
                        # Check for empty fields before adding to database
                        if all(dns_lookup.values()):
                            if self.debug:
                                print("DNS Provider:", provider[0])
                                print("DNS Server:", dns)
                                print("Domain:", self.domain_name)
                                print("Response:", rdata.to_text())
                                print("Time:", end_time - start_time)
                            self.database.add_dns_lookup(**dns_lookup)
