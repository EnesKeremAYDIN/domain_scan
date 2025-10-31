# Domain Scan

Command-line domain scanning toolkit written in Python. This tool allows you to perform basic reconnaissance and DNS-level investigation on any domain using only native Python libraries and DNS queries.

## Features

- **DNS Records Lookup**: Fetch A, MX, and TXT records.
- **Zone Transfer Test**: Try AXFR zone transfers on nameservers.
- **Certificate Transparency Log Check**: View certificate history via crt.sh (no API key required).
- **Subdomain Brute-force**: Attempt subdomain discovery using a live wordlist from GitHub.
- **Run All**: Execute all features in sequence for a full scan.

## Installation and Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EnesKeremAYDIN/domain-scan.git
   cd domain-scan
   ```

2. **Install dependencies**:
   - The tool uses `dnspython`. Install it via pip:
   ```bash
   pip install dnspython
   ```

3. **Run the tool**:
   ```bash
   python domain_scan.py
   ```

## Menu Options

```
1. DNS Records Lookup
2. Zone Transfer Test
3. Certificate Transparency Log Check
4. Subdomain Brute-force (online list)
5. Run All Tasks
0. Exit
```

## Files

- **`domain_scan.py`** – The main script file for running domain analysis tasks.
- **Online Wordlist Source** – Subdomains are pulled live from:
  [`SecLists`](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/subdomains-top1million-5000.txt)

## Requirements

- Python 3.x
- Internet access (for fetching subdomain wordlist and CT logs)
- `dnspython` library

## Disclaimer

This tool is intended for educational and personal use. Use responsibly and only on domains you have permission to scan.
