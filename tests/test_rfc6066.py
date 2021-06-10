#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley
# Copyright (c) 2021, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
import sys
import unittest

from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder

from pyasn1_alt_modules import pem
from pyasn1_alt_modules import rfc6066


class PkiPathTestCase(unittest.TestCase):
    pem_text = """\
MIIJHDCCAgIwggGIoAMCAQICCQDokdYGkU/O8jAKBggqhkjOPQQDAzA/MQswCQYD
VQQGEwJVUzELMAkGA1UECAwCVkExEDAOBgNVBAcMB0hlcm5kb24xETAPBgNVBAoM
CEJvZ3VzIENBMB4XDTE5MDUxNDA4NTgxMVoXDTIxMDUxMzA4NTgxMVowPzELMAkG
A1UEBhMCVVMxCzAJBgNVBAgMAlZBMRAwDgYDVQQHDAdIZXJuZG9uMREwDwYDVQQK
DAhCb2d1cyBDQTB2MBAGByqGSM49AgEGBSuBBAAiA2IABPBRdlSx6I5qpZ2sKUMI
xun1gUAzzstOYWKvKCnMoNT1x+pIKDvMEMimFcLAxxL3NVYOhK0Jty83SPDkKWMd
x9/Okdhf3U/zxJlEnXDiFrAeM6xbG8zcCRiBnmd92UvsRqNQME4wHQYDVR0OBBYE
FPI12zQE2qVV8r1pA5mwYuziFQjBMB8GA1UdIwQYMBaAFPI12zQE2qVV8r1pA5mw
YuziFQjBMAwGA1UdEwQFMAMBAf8wCgYIKoZIzj0EAwMDaAAwZQIwWlGNjb9NyqJS
zUSdsEqDSvMZb8yFkxYCIbAVqQ9UqScUUb9tpJKGsPWwbZsnLVvmAjEAt/ypozbU
hQw4dSPpWzrn5BQ0kKbDM3DQJcBABEUBoIOol1/jYQPmxajQuxcheFlkMIIDhzCC
Aw6gAwIBAgIJAKWzVCgbsG5GMAoGCCqGSM49BAMDMD8xCzAJBgNVBAYTAlVTMQsw
CQYDVQQIDAJWQTEQMA4GA1UEBwwHSGVybmRvbjERMA8GA1UECgwIQm9ndXMgQ0Ew
HhcNMTkxMTAyMTg0MjE4WhcNMjAxMTAxMTg0MjE4WjBmMQswCQYDVQQGEwJVUzEL
MAkGA1UECBMCVkExEDAOBgNVBAcTB0hlcm5kb24xEDAOBgNVBAoTB0V4YW1wbGUx
DDAKBgNVBAsTA1BDQTEYMBYGA1UEAxMPcGNhLmV4YW1wbGUuY29tMHYwEAYHKoZI
zj0CAQYFK4EEACIDYgAEPf5vbgAqbE5dn6wbiCx4sCCcn1BKSrHmCfiWC9QLSGVN
GHifQwPt9odGXjRiQ7QwpZ2wRD6Z91v+fk85XXLE3kJQCQdPIHFUY5EMpvS7T6u6
xrmwnlVpUURPTOxfc55Oo4IBrTCCAakwHQYDVR0OBBYEFCbqJQ8LMiAopNdaCo3/
Ldy9f1RlMG8GA1UdIwRoMGaAFPI12zQE2qVV8r1pA5mwYuziFQjBoUOkQTA/MQsw
CQYDVQQGEwJVUzELMAkGA1UECAwCVkExEDAOBgNVBAcMB0hlcm5kb24xETAPBgNV
BAoMCEJvZ3VzIENBggkA6JHWBpFPzvIwDwYDVR0TAQH/BAUwAwEB/zALBgNVHQ8E
BAMCAYYwQgYJYIZIAYb4QgENBDUWM1RoaXMgY2VydGlmaWNhdGUgY2Fubm90IGJl
IHRydXN0ZWQgZm9yIGFueSBwdXJwb3NlLjAVBgNVHSAEDjAMMAoGCCsGAQUFBw0C
MAoGA1UdNgQDAgECMIGRBggrBgEFBQcBFQSBhDCBgTBZBgsqhkiG9w0BCRAHAwMC
BeAxRjBEgAsqhkiG9w0BCRAHBIE1MDMMF0xBVyBERVBBUlRNRU5UIFVTRSBPTkxZ
DBhIVU1BTiBSRVNPVVJDRVMgVVNFIE9OTFkwEQYLKoZIhvcNAQkQBwIDAgTwMBEG
CyqGSIb3DQEJEAcBAwIF4DAKBggqhkjOPQQDAwNnADBkAjAZSD+BVqzc1l0fDoH3
LwixjxvtddBHbJsM5yBek4U9b2yWL2KEmwV02fTgof3AjDECMCTsksmx5f3i5DSY
fe9Q1heJlEJLd1hgZmfvUYNnCU3WrdmYzyoNdNTbg7ZFMoxsXzCCA4cwggMOoAMC
AQICCQCls1QoG7BuRjAKBggqhkjOPQQDAzA/MQswCQYDVQQGEwJVUzELMAkGA1UE
CAwCVkExEDAOBgNVBAcMB0hlcm5kb24xETAPBgNVBAoMCEJvZ3VzIENBMB4XDTE5
MTEwMjE4NDIxOFoXDTIwMTEwMTE4NDIxOFowZjELMAkGA1UEBhMCVVMxCzAJBgNV
BAgTAlZBMRAwDgYDVQQHEwdIZXJuZG9uMRAwDgYDVQQKEwdFeGFtcGxlMQwwCgYD
VQQLEwNQQ0ExGDAWBgNVBAMTD3BjYS5leGFtcGxlLmNvbTB2MBAGByqGSM49AgEG
BSuBBAAiA2IABD3+b24AKmxOXZ+sG4gseLAgnJ9QSkqx5gn4lgvUC0hlTRh4n0MD
7faHRl40YkO0MKWdsEQ+mfdb/n5POV1yxN5CUAkHTyBxVGORDKb0u0+rusa5sJ5V
aVFET0zsX3OeTqOCAa0wggGpMB0GA1UdDgQWBBQm6iUPCzIgKKTXWgqN/y3cvX9U
ZTBvBgNVHSMEaDBmgBTyNds0BNqlVfK9aQOZsGLs4hUIwaFDpEEwPzELMAkGA1UE
BhMCVVMxCzAJBgNVBAgMAlZBMRAwDgYDVQQHDAdIZXJuZG9uMREwDwYDVQQKDAhC
b2d1cyBDQYIJAOiR1gaRT87yMA8GA1UdEwEB/wQFMAMBAf8wCwYDVR0PBAQDAgGG
MEIGCWCGSAGG+EIBDQQ1FjNUaGlzIGNlcnRpZmljYXRlIGNhbm5vdCBiZSB0cnVz
dGVkIGZvciBhbnkgcHVycG9zZS4wFQYDVR0gBA4wDDAKBggrBgEFBQcNAjAKBgNV
HTYEAwIBAjCBkQYIKwYBBQUHARUEgYQwgYEwWQYLKoZIhvcNAQkQBwMDAgXgMUYw
RIALKoZIhvcNAQkQBwSBNTAzDBdMQVcgREVQQVJUTUVOVCBVU0UgT05MWQwYSFVN
QU4gUkVTT1VSQ0VTIFVTRSBPTkxZMBEGCyqGSIb3DQEJEAcCAwIE8DARBgsqhkiG
9w0BCRAHAQMCBeAwCgYIKoZIzj0EAwMDZwAwZAIwGUg/gVas3NZdHw6B9y8IsY8b
7XXQR2ybDOcgXpOFPW9sli9ihJsFdNn04KH9wIwxAjAk7JLJseX94uQ0mH3vUNYX
iZRCS3dYYGZn71GDZwlN1q3ZmM8qDXTU24O2RTKMbF8=
"""

    def setUp(self):
        self.asn1Spec = rfc6066.PkiPath()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))
        self.assertEqual(3, len(asn1Object))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
