from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna
from socket import socket
import sys
from collections import namedtuple

HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')


def get_certificate(hostname, port):
    hostname_idna = idna.encode(hostname)
    sock = socket()

    sock.connect((hostname, port))
    peername = sock.getpeername()
    ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE

    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    crypto_cert = cert.to_cryptography()
    sock_ssl.close()
    sock.close()

    return HostInfo(cert=crypto_cert, peername=peername, hostname=hostname)

def print_basic_info(certificate):
    s = '''
    commonName: {commonname}
    SAN: {SAN}
    issuer: {issuer}
    notBefore: {notbefore}
    notAfter:  {notafter}
    '''.format(
            commonname=get_common_name(certificate.cert),
            SAN=get_alt_names(certificate.cert),
            issuer=get_issuer(certificate.cert),
            notbefore=certificate.cert.not_valid_before,
            notafter=certificate.cert.not_valid_after
    )
    print(s)


def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None

def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def runner(url):
    #domain = sys.argv[1]
    result = get_certificate(url, 443)
    print_basic_info(result)
