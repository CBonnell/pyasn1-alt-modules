#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to add a map for use with opentypes.
# Updated by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# CMS Compressed Data Content Type
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc3274.txt
#

from pyasn1.type import namedtype
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import rfc5652
from pyasn1_alt_modules import opentypemap

cmsContentTypesMap = opentypemap.get('cmsContentTypesMap')


class CompressionAlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    pass


# The CMS Compressed Data Content Type

id_ct_compressedData = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.9')

class CompressedData(univ.Sequence):
    pass

CompressedData.componentType = namedtype.NamedTypes(
    namedtype.NamedType('version', rfc5652.CMSVersion()), # Always set to 0
    namedtype.NamedType('compressionAlgorithm', CompressionAlgorithmIdentifier()),
    namedtype.NamedType('encapContentInfo', rfc5652.EncapsulatedContentInfo())
)


# Algorithm identifier for the zLib Compression Algorithm
# This includes cpa_zlibCompress as defined in RFC 6268,
# from https://www.rfc-editor.org/rfc/rfc6268.txt

id_alg_zlibCompress = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.8')

cpa_zlibCompress = rfc5280.AlgorithmIdentifier()
cpa_zlibCompress['algorithm'] = id_alg_zlibCompress
# cpa_zlibCompress['parameters'] are absent


# Update the CMS Content Types Map

_cmsContentTypesMapUpdate = {
    id_ct_compressedData: CompressedData(),
}

cmsContentTypesMap.update(_cmsContentTypesMapUpdate)
