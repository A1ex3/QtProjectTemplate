from dataclasses import dataclass

@dataclass
class _ThirdPartyInfo:
    name: str
    version: str
    hash_commit: str
    repository: str | None = None

QT_INFO = _ThirdPartyInfo("Qt", "6.10.0", "077347cc6d198053fb61cc0841c5c0c60a7deeb1", "https://code.qt.io/qt/qt5.git")