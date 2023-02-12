import checkdmarc
import json
from collections import OrderedDict
from tabulate import tabulate

domain = "microsoft.com"

# Retrieve and parse DMARC record
result = checkdmarc.get_dmarc_record(domain, include_tag_descriptions=True)

# Extract parsed data
parsed_data = result['parsed']['tags']

# DMARC tag descriptions
descriptions = {
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

# Create an ordered dictionary with tag keys, values, short descriptions, and explicit flag
table_dict = OrderedDict()
for key in parsed_data:
    value = parsed_data[key]['value']
    if isinstance(value, list):
        if len(value) > 0:
            value = value[0]
            if isinstance(value, dict) and 'mailto' in value.get('scheme', ''):
                value = value['address']
            elif '1' in value:
                value = True
    description = descriptions[key]
    explicit = "✓" if parsed_data[key]['explicit'] else "🞩"
    table_dict[key] = (key, value, description, explicit)

# Print table of parsed DMARC tags and values with short descriptions and explicit flag
print(tabulate(table_dict.items(), headers=['DMARC Tag', 'Value', 'Description', 'Explicit'], tablefmt='orgtbl'))
#print(table_dict)