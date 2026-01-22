from dataclasses import dataclass
import enum

class EnumThirdPartyInfoType(enum.Enum):
    GIT = 0
    HTTP_FILE = 1

@dataclass
class ThirdPartyInfo:
    struct_type: EnumThirdPartyInfoType
    name: str
    version: str
    url: str
    hash_commit: str | None = None

    def __str__(self):
        return f"ThirdPartyInfo(struct_type: {self.struct_type}, name: {self.name}, version: {self.version}, url: {self.url}, hash_commit: {self.hash_commit})"
