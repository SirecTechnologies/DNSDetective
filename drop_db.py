# test_dns_resolver.py
import sys

from dns_detective_database_service import DNSDetectiveDatabase

if __name__ == "__main__":

    database = DNSDetectiveDatabase(db_name='dns_detective.db')
    drop_table = database.drop_table()
    print(drop_table)
    database.close()