from dataclasses import dataclass

@dataclass
class _ThirdPartyInfo:
    name: str
    version: str
    hash_commit: str

QT_INFO = _ThirdPartyInfo("Qt", "6.8.1", "41d5d04f71871d94a76a1910ef153139a9746c32")