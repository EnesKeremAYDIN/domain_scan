import dns.resolver
import dns.query
import dns.zone
import socket
import ssl
import http.client
import re
import urllib.request

def separator():
    print("\n" + "=" * 50 + "\n")

def get_dns_records(domain):
    separator()
    print(f"[+] DNS Records for {domain}")
    record_types = ['A', 'MX', 'TXT']
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for rdata in answers:
                print(f"{rtype}: {rdata.to_text()}")
        except Exception as e:
            print(f"{rtype}: Lookup failed ({e})")

def try_zone_transfer(domain):
    separator()
    print(f"[+] Attempting Zone Transfer for {domain}")
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        for ns in ns_records:
            ns_address = str(ns.target)
            print(f"[*] Trying nameserver: {ns_address}")
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(ns_address, domain, timeout=5))
                names = zone.nodes.keys()
                for n in names:
                    print(zone[n].to_text(n))
                return
            except Exception as xe:
                print(f"[-] Zone transfer failed on {ns_address}: {xe}")
    except Exception as e:
        print(f"[!] Could not get NS records: {e}")

def check_ct_logs(domain):
    separator()
    print(f"[+] Certificate Transparency (CT) Log check for {domain}")
    conn = http.client.HTTPSConnection("crt.sh")
    path = f"/?q=%25.{domain}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        if res.status != 200:
            print("[-] Could not fetch CT logs.")
            return
        data = res.read().decode('utf-8')
        matches = set(re.findall(r'\"common_name\":\"([^\"]+)\"', data))
        for d in matches:
            print(f"[+] {d}")
    except Exception as e:
        print(f"[!] Error fetching CT log data: {e}")
    finally:
        conn.close()

def subdomain_bruteforce(domain):
    separator()
    print(f"[+] Subdomain Brute Force on {domain}")
    
    wordlist_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt"
    
    try:
        response = urllib.request.urlopen(wordlist_url)
        words = response.read().decode().splitlines()
    except Exception as e:
        print(f"[-] Failed to fetch subdomain list: {e}")
        return

    for sub in words:
        subdomain = f"{sub.strip()}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            print(f"[FOUND] {subdomain} -> {ip}")
        except socket.gaierror:
            continue

def run_all(domain):
    print("\n[+] Running All Tasks...\n")
    get_dns_records(domain)
    try_zone_transfer(domain)
    check_ct_logs(domain)
    subdomain_bruteforce(domain)

def main():
    print("=" * 50)
    print("🛠️  DOMAIN SCAN TOOLKIT".center(50))
    print("=" * 50)
    domain = input("Enter a domain (e.g., example.com): ").strip()

    while True:
        separator()
        print("Choose an option:")
        print("1. DNS Records Lookup")
        print("2. Zone Transfer Test")
        print("3. Certificate Transparency Log Check")
        print("4. Subdomain Brute-force (online list)")
        print("5. Run All Tasks")
        print("0. Exit")
        print()

        choice = input("Your choice: ").strip()
        if choice == "1":
            get_dns_records(domain)
        elif choice == "2":
            try_zone_transfer(domain)
        elif choice == "3":
            check_ct_logs(domain)
        elif choice == "4":
            subdomain_bruteforce(domain)
        elif choice == "5":
            run_all(domain)
        elif choice == "0":
            print("\n[+] Goodbye.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
