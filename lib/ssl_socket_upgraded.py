from OpenSSL import SSL
import idna
from socket import socket
import sys
from datetime import datetime
from ssl import PROTOCOL_TLSv1
import json
from termcolor import colored
import os




def get_cert(hostname, port):
    hostname_idna = idna.encode(hostname)
    sock = socket()
    sock.connect((hostname, port))
    ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE
    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    sock_ssl.close()
    sock.close()
    return cert



def get_cert_info(host, cert):
    context = {}
    cert_subject = cert.get_subject()
    context['host'] = host
    context['issued_to'] = cert_subject.CN
    context['issued_o'] = cert_subject.O
    context['issuer_c'] = cert.get_issuer().countryName
    context['issuer_o'] = cert.get_issuer().organizationName
    context['issuer_ou'] = cert.get_issuer().organizationalUnitName
    context['issuer_cn'] = cert.get_issuer().commonName
    context['cert_sn'] = str(cert.get_serial_number())
    context['cert_sha1'] = cert.digest('sha1').decode()
    context['cert_alg'] = cert.get_signature_algorithm().decode()
    context['cert_ver'] = cert.get_version()
    context['cert_exp'] = cert.has_expired()

    # Valid from
    valid_from = datetime.strptime(cert.get_notBefore().decode('ascii'),'%Y%m%d%H%M%SZ')
    context['valid_from'] = valid_from.strftime('%Y-%m-%d')
    
    # Valid till
    valid_till = datetime.strptime(cert.get_notAfter().decode('ascii'),'%Y%m%d%H%M%SZ')
    context['valid_till'] = valid_till.strftime('%Y-%m-%d')
    
    # Validity days
    context['validity_days'] = (valid_till - valid_from).days
    
    # Validity in days from now
    now = datetime.now()
    context['days_left'] = (valid_till - now).days
    return context


def print_status(host, context):
    print("SSL Details for : " + host)
    if "*" in context['issued_to']:
        print(colored('Issued domain: ' + context['issued_to'],"red"))
    else:
        print('Issued domain: ' + context['issued_to'])
    #print('Issued to: ' + context['issued_o'])
    print('Issued by: {} ({})'.format(context['issuer_o'], context['issuer_c']))
    print('Valid from: ' + context['valid_from'])
    print('Valid to: ' + context['valid_till'])
    print('Validity days: ' + context['validity_days'].__str__())
    print('Certificate S/N: ' + context['cert_sn'].__str__())
    print('Certificate SHA1 FP: ' + context['cert_sha1'].__str__())
    print('Certificate version: ' + context['cert_ver'].__str__())
    print('Certificate algorithm: ' + context['cert_alg'].__str__())
    print('Expired: ' + context['cert_exp'].__str__())




def analyze_ssl(host):
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen

    api_url = 'https://api.ssllabs.com/api/v3/'
    main_request = json.loads(urlopen(api_url + 'analyze?host={}'.format(host)).read().decode('utf-8'))
    endpoint_data = json.loads(urlopen(api_url + 'getEndpointData?host={}&s={}'.format(host, main_request['endpoints'][0]['ipAddress'])).read().decode('utf-8'))
    
    #print(json.dumps(endpoint_data,sort_keys=False,indent=4))

    # if the certificate is invalid
    if endpoint_data['statusMessage'] == 'Certificate not valid for domain name':
        print("Certificate not valid")
    context = {}
    if endpoint_data['ipAddress']: 
        context['IP_Address'] = endpoint_data['ipAddress']
    if endpoint_data['details']['poodle']: 
        context['SSL_Poodle_Check'] = endpoint_data['details']['poodle']
    if endpoint_data['details']['heartbleed']:
        context['Heartbleed_Vulnerable_Check'] = endpoint_data['details']['heartbleed']
    if endpoint_data['details']['heartbeat']:
        context['Heartbeat_Vulnerable_Check'] = endpoint_data['details']['heartbeat']
    if endpoint_data['details']['freak']:
        context['Freak_Vulnerable_Check'] = endpoint_data['details']['freak']
    if endpoint_data['details']['logjam']:
        context['Logjam_Vulnerable_Check'] = endpoint_data['details']['logjam']
    if endpoint_data['details']['drownVulnerable']:
        context['Drown_Vulnerable_Check'] = endpoint_data['details']['drownVulnerable']
    if endpoint_data['details']['supportsRc4']:
        context['Support_for_RC4'] = endpoint_data['details']['supportsRc4']
    if endpoint_data['details']['fallbackScsv']:
        context['TLS_fallback'] = endpoint_data['details']['fallbackScsv']
    if endpoint_data['details']['vulnBeast']:
        context['SSL_Beast_Check'] = endpoint_data['details']['vulnBeast']
    print(json.dumps(context,sort_keys=False,indent=4))

def ciphers(url,port_num):
    print(colored("\nExtracting Cipher Suites.  (Might take 60seconds to complete )", "green"))
    cmd = "nmap -Pn -p " + port_num + " --script ssl-enum-ciphers " + url
    res = os.popen(cmd)
    for line in res:
        if "TLS" in line or "open" in line:
            if "- D" in line or "- C" in line or "- B" in line or "1024" in line:
                print(colored(line.replace('|', '').replace('   ', '').strip('\n'), "red"))
            else:
                print(line.replace('|', '').replace('   ', '').strip('\n'))

    print(colored("Performing Additional SSL checks using NMap Library", "green"))
    # print(colored("\nChecking for SSL CCS Injection Vulnerability", "green"))
    cmd = "nmap -Pn -p " + port_num + " --script ssl-ccs-injection " + url
    res = os.popen(cmd)
    for line in res:
        if "VULNERALE" in line and "State" in line:
            print("\tVulnerable to SSL CCS Injection Vulnerability")

    # print(colored("Checking for Heartbleed Vulnerability", "green"))
    cmd = "nmap -Pn -p " + port_num + " --script ssl-heartbleed " + url
    res = os.popen(cmd)
    for line in res:
        if "VULNERALE" in line and "State" in line:
            print("\tVulnerable to SSL HeartBleed Vulnerability")

def runner(domain,port_num):
    try:
        cert = get_cert(domain ,int(port_num))
        cont = get_cert_info(domain, cert)
        print_status(domain, cont)
    except Exception as e:
        print("Error Connecting to host. Error: " + e.__str__())
    try:
        ciphers(domain,port_num.__str__())
    except Exception as e:
        print("Error Occured with Nmap Library. Exiting")
        sys.exit(1)
    try:
        analyze_ssl(domain)
    except Exception as e:
        print("Server Errors Received. Skipping Cipher Suites Validation " + e.__str__())
        pass


