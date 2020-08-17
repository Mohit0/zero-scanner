from nslookup import Nslookup

domain = "optum.com"

# set optional Cloudflare public DNS server
dns_query = Nslookup(dns_servers=["1.1.1.1"])

ips_record = dns_query.dns_lookup(domain)
print(ips_record.response_full, ips_record.answer)