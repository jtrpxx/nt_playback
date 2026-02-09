from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import ipaddress
import datetime

def generate_self_signed_cert():
    # 1. สร้าง Private Key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 2. กำหนดรายละเอียด Certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"TH"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Nichetel Project"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    
    # 3. สร้าง Certificate
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(u"localhost"), 
            x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
            x509.DNSName(u"nichetel-niceplayer"),
            x509.IPAddress(ipaddress.ip_address("192.168.1.90")),
            x509.DNSName(u"nichetel-player-connect")
        ]),
        critical=False,
    ).sign(key, hashes.SHA256())

    # 4. บันทึกไฟล์ key.pem
    with open("key.pem", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # 5. บันทึกไฟล์ cert.pem
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print("สร้างไฟล์ cert.pem และ key.pem เรียบร้อยแล้ว")

if __name__ == "__main__":
    generate_self_signed_cert()
