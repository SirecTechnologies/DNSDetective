# dns_detective_database_service.py
import sqlite3

class DNSDetectiveDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS dns_lookups (id INTEGER PRIMARY KEY AUTOINCREMENT, domain TEXT, dns_server TEXT, request_timestamp TEXT, response_timestamp TEXT, response TEXT)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS dmarc_reports (id INTEGER PRIMARY KEY AUTOINCREMENT, domain TEXT, policy TEXT, subdomain_policy TEXT, spf_alignment TEXT, dkim_alignment  TEXT, percent_pass TEXT, report_timestamp TEXT, report TEXT)"
        )
        self.conn.commit()

    def store_dmarc_report(self, domain, policy, subdomain_policy, spf_alignment, dkim_alignment, percent_pass, report_timestamp, report):
        self.cursor.execute(
            "INSERT INTO dmarc_reports (domain, policy, subdomain_policy, spf_alignment, dkim_alignment, percent_pass, report_timestamp, report) VALUES (?,?,?,?,?,?,?)",
            (domain, policy, subdomain_policy, spf_alignment, dkim_alignment, percent_pass, report_timestamp, report)
        )
        self.conn.commit()

    def add_dns_lookup(self, domain, dns_server, request_timestamp, response_timestamp, response):
        cursor = self.conn.cursor()
        self.cursor.execute("""INSERT INTO dns_lookups (domain, dns_server, request_timestamp, response_timestamp, response)
            VALUES (?, ?, ?, ?, ?)""", (domain, dns_server, request_timestamp, response_timestamp, response))
        self.conn.commit()

    def get_dns_lookups(self, table):
        table_name = table
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM " + table_name)
            lookups = cursor.fetchall()
            print(f"Number of rows returned: {len(lookups)}")
            return lookups
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def drop_table(self,table):
        table_name = table
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.commit()
            message = (f"Table '{table_name}' was dropped successfully.")
        except Exception as e:
            message = (f"An error occurred while dropping the table '{table_name}': {e}")
        return message

    def close(self):
        self.conn.close()
