# test_dns_resolver.py
import sys

from dns_detective_database_service import DNSDetectiveDatabase

if __name__ == "__main__":
    table = sys.argv[1]
    debug = False
    if len(sys.argv) > 2 and sys.argv[2] == "debug":
        debug = True
    database = DNSDetectiveDatabase(db_name='dns_detective.db')
    dns_lookups = database.get_dns_lookups(table)
    print(dns_lookups)
    database.close()