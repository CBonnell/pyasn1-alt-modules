#
# This file is part of pyasn1-alt-modules software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# Copyright (c) 2021-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
import sys
import unittest

from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder

from pyasn1_alt_modules import pem
from pyasn1_alt_modules import rfc2315


class Pkcs7TestCase(unittest.TestCase):
    pem_text_unordered = """\
MIIKdQYJKoZIhvcNAQcCoIIKZjCCCmICAQExADALBgkqhkiG9w0BBwGgggpIMIIC
XjCCAcegAwIBAgIBADANBgkqhkiG9w0BAQQFADB1MQswCQYDVQQGEwJSVTEPMA0G
A1UEBxMGTW9zY293MRcwFQYDVQQKEw5Tb3ZhbSBUZWxlcG9ydDEMMAoGA1UECxMD
TklTMQ8wDQYDVQQDEwZBQlMgQ0ExHTAbBgkqhkiG9w0BCQEWDmNlcnRAb25saW5l
LnJ1MB4XDTk5MDgxNTE5MDI1OFoXDTAwMDExMjE5MDI1OFowdTELMAkGA1UEBhMC
UlUxDzANBgNVBAcTBk1vc2NvdzEXMBUGA1UEChMOU292YW0gVGVsZXBvcnQxDDAK
BgNVBAsTA05JUzEPMA0GA1UEAxMGQUJTIENBMR0wGwYJKoZIhvcNAQkBFg5jZXJ0
QG9ubGluZS5ydTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAw0g1P0yQAZIi
ml2XOCOxnCcuhHmAgj4Ei9M2ebrrGwUMONPzr1a8W7JcpnR3FeOjxEIxrzkHr6UA
oj4l/oC7Rv28uIig+Okf+82ekhH6VgAQNr5LAzfN8J6dZLx2OXAmmLleAqHuisT7
I40vEFRoRmC5hiMlILE2rIlIKJn6cUkCAwEAATANBgkqhkiG9w0BAQQFAAOBgQBZ
7ELDfGUNb+fbpHl5W3d9JMXsdOgd96+HG+X1SPgeiRAMjkla8WFCSaQPIR4vCy0m
tm5a2bWSji6+vP5FGbjOz5iMlHMrCtu0He7Eim2zpaGI06ZIY75Cn1h2r3+KS0/R
h01TJUbmsfV1tZm6Wk3bayJ+/K8A4mBHv8P6rhYacDCCAowwggH1oAMCAQICAQAw
DQYJKoZIhvcNAQEEBQAwgYsxCzAJBgNVBAYTAlJVMQ8wDQYDVQQHEwZNb3Njb3cx
FzAVBgNVBAoTDkdvbGRlbiBUZWxlY29tMQwwCgYDVQQLEwNST0wxHjAcBgNVBAMT
FUdvbGRlbiBUZWxlY29tIEFCUyBDQTEkMCIGCSqGSIb3DQEJARYVY2VydEBnb2xk
ZW50ZWxlY29tLnJ1MB4XDTAwMDEwNTE1MDY1MVoXDTEwMDExNTE1MDY1MVowgYsx
CzAJBgNVBAYTAlJVMQ8wDQYDVQQHEwZNb3Njb3cxFzAVBgNVBAoTDkdvbGRlbiBU
ZWxlY29tMQwwCgYDVQQLEwNST0wxHjAcBgNVBAMTFUdvbGRlbiBUZWxlY29tIEFC
UyBDQTEkMCIGCSqGSIb3DQEJARYVY2VydEBnb2xkZW50ZWxlY29tLnJ1MIGfMA0G
CSqGSIb3DQEBAQUAA4GNADCBiQKBgQDPFel/Svli6ogoUEb6eLtEvNSjyalETSMP
MIZXdmWIkWijvEUhDnNJVAE3knAt6dVYqxWq0vc6CbAGFZNqEyioGU48IECLzV0G
toiYejF/c9PuyIKDejeV9/YZnNFaZAUOXhOjREdZURLISKhX4tAbQyvK0Qka9AAR
MEy9DoqV8QIDAQABMA0GCSqGSIb3DQEBBAUAA4GBAHQzgqFkoSMQr077UCr5C0l1
rxLA17TrocCmUC1/PLmN0LmUHD0d7TjjTQKJaJBHxcKIg6+FOY6LSSY4nAN79eXi
nBz+jEUG7+NTU/jcEArI35yP7fi4Mwb96EYDmUkUGtcLNq3JBe/d1Zhmy9HnNBL1
Dn9thM2Q8RPYAJIU3JnGMIICqTCCAhICAQAwDQYJKoZIhvcNAQEEBQAwgZwxCzAJ
BgNVBAYTAlJVMQ8wDQYDVQQIEwZNb3Njb3cxDzANBgNVBAcTBk1vc2NvdzEXMBUG
A1UEChMOR29sZGVuIFRlbGVjb20xDDAKBgNVBAsTA1JPTDEeMBwGA1UEAxMVR29s
ZGVuIFRlbGVjb20gQUJTIENBMSQwIgYJKoZIhvcNAQkBFhVjZXJ0QGdvbGRlbnRl
bGVjb20ucnUwHhcNMTAwMTE1MTU0MDI2WhcNMjAwMjIyMTU0MDI2WjCBnDELMAkG
A1UEBhMCUlUxDzANBgNVBAgTBk1vc2NvdzEPMA0GA1UEBxMGTW9zY293MRcwFQYD
VQQKEw5Hb2xkZW4gVGVsZWNvbTEMMAoGA1UECxMDUk9MMR4wHAYDVQQDExVHb2xk
ZW4gVGVsZWNvbSBBQlMgQ0ExJDAiBgkqhkiG9w0BCQEWFWNlcnRAZ29sZGVudGVs
ZWNvbS5ydTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAzxXpf0r5YuqIKFBG
+ni7RLzUo8mpRE0jDzCGV3ZliJFoo7xFIQ5zSVQBN5JwLenVWKsVqtL3OgmwBhWT
ahMoqBlOPCBAi81dBraImHoxf3PT7siCg3o3lff2GZzRWmQFDl4To0RHWVESyEio
V+LQG0MrytEJGvQAETBMvQ6KlfECAwEAATANBgkqhkiG9w0BAQQFAAOBgQCMrS4T
LIzxcpu8nwOq/xMcxW4Ctz/wjIoePWkmSLe+Tkb4zo7aTsvzn+ETaWb7qztUpyl0
QvlXn4vC2iCJloPpofPqSzF1UV3g5Zb93ReZu7E6kEyW0ag8R5XZKv0xuR3b3Le+
ZqolT8wQELd5Mmw5JPofZ+O2cGNvet8tYwOKFjCCAqUwggIOoAMCAQICAgboMA0G
CSqGSIb3DQEBBAUAMIGcMQswCQYDVQQGEwJSVTEPMA0GA1UECBMGTW9zY293MQ8w
DQYDVQQHEwZNb3Njb3cxFzAVBgNVBAoTDkdvbGRlbiBUZWxlY29tMQwwCgYDVQQL
EwNST0wxHjAcBgNVBAMTFUdvbGRlbiBUZWxlY29tIEFCUyBDQTEkMCIGCSqGSIb3
DQEJARYVY2VydEBnb2xkZW50ZWxlY29tLnJ1MB4XDTExMDEyODEyMTcwOVoXDTEy
MDIwMTAwMDAwMFowdjELMAkGA1UEBhMCUlUxDDAKBgNVBAgTA04vQTEXMBUGA1UE
ChMOR29sZGVuIFRlbGVjb20xDDAKBgNVBAsTA0lTUDEWMBQGA1UEAxMNY3JheS5n
bGFzLm5ldDEaMBgGCSqGSIb3DQEJARYLZWxpZUByb2wucnUwgZ8wDQYJKoZIhvcN
AQEBBQADgY0AMIGJAoGBAPJAm8KG3ZCoJSvoGmLMPlGaMIpadu/EGSEYu+M/ybLp
Cs8XmwB3876JVKKCbtGI6eqxOqvjedYXb+nKcyhz4Ztmm8RgAD7Z1WUItIpatejT
79EYOUWrDN713SLZsImMyP4B4EySl4LZfHFRU2iOwLB6WozGCYuULLqYS9MDPrnT
AgMBAAGjGzAZMBcGCWCGSAGG+EIBDQQKFghDPS07Uz0tOzANBgkqhkiG9w0BAQQF
AAOBgQDEttS70qYCA+MGBA3hOR88XiBcTmuBarJDwn/rj31vRjYZUgp9bbFwscRI
Ic4lDnlyvunwNitl+341bDg7u6Ebu9hCMbciyu4EtrsDh77DlLzbmNcXbnhlvbFL
K9GiPz3dNyvQMfmaA0twd62zJDOVJ1SmO04lLmu/pAx8GhBZkqEAMQA=
"""

    # canonically ordered SET components
    pem_text_reordered = """\
MIIKcwYJKoZIhvcNAQcCoIIKZDCCCmACAQExADALBgkqhkiG9w0BBwGgggpIMIIC
XjCCAcegAwIBAgIBADANBgkqhkiG9w0BAQQFADB1MQswCQYDVQQGEwJSVTEPMA0G
A1UEBxMGTW9zY293MRcwFQYDVQQKEw5Tb3ZhbSBUZWxlcG9ydDEMMAoGA1UECxMD
TklTMQ8wDQYDVQQDEwZBQlMgQ0ExHTAbBgkqhkiG9w0BCQEWDmNlcnRAb25saW5l
LnJ1MB4XDTk5MDgxNTE5MDI1OFoXDTAwMDExMjE5MDI1OFowdTELMAkGA1UEBhMC
UlUxDzANBgNVBAcTBk1vc2NvdzEXMBUGA1UEChMOU292YW0gVGVsZXBvcnQxDDAK
BgNVBAsTA05JUzEPMA0GA1UEAxMGQUJTIENBMR0wGwYJKoZIhvcNAQkBFg5jZXJ0
QG9ubGluZS5ydTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAw0g1P0yQAZIi
ml2XOCOxnCcuhHmAgj4Ei9M2ebrrGwUMONPzr1a8W7JcpnR3FeOjxEIxrzkHr6UA
oj4l/oC7Rv28uIig+Okf+82ekhH6VgAQNr5LAzfN8J6dZLx2OXAmmLleAqHuisT7
I40vEFRoRmC5hiMlILE2rIlIKJn6cUkCAwEAATANBgkqhkiG9w0BAQQFAAOBgQBZ
7ELDfGUNb+fbpHl5W3d9JMXsdOgd96+HG+X1SPgeiRAMjkla8WFCSaQPIR4vCy0m
tm5a2bWSji6+vP5FGbjOz5iMlHMrCtu0He7Eim2zpaGI06ZIY75Cn1h2r3+KS0/R
h01TJUbmsfV1tZm6Wk3bayJ+/K8A4mBHv8P6rhYacDCCAowwggH1oAMCAQICAQAw
DQYJKoZIhvcNAQEEBQAwgYsxCzAJBgNVBAYTAlJVMQ8wDQYDVQQHEwZNb3Njb3cx
FzAVBgNVBAoTDkdvbGRlbiBUZWxlY29tMQwwCgYDVQQLEwNST0wxHjAcBgNVBAMT
FUdvbGRlbiBUZWxlY29tIEFCUyBDQTEkMCIGCSqGSIb3DQEJARYVY2VydEBnb2xk
ZW50ZWxlY29tLnJ1MB4XDTAwMDEwNTE1MDY1MVoXDTEwMDExNTE1MDY1MVowgYsx
CzAJBgNVBAYTAlJVMQ8wDQYDVQQHEwZNb3Njb3cxFzAVBgNVBAoTDkdvbGRlbiBU
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
"""

    def setUp(self):
        self.asn1Spec = rfc2315.ContentInfo()

    def testDerCodec(self):

        substrate = pem.readBase64fromText(self.pem_text_unordered)

        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

    def testDerCodecDecodeOpenTypes(self):

        substrate = pem.readBase64fromText(self.pem_text_reordered)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec, decodeOpenTypes=True)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(
            substrate, der_encoder(asn1Object, omitEmptyOptionals=False))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
