import platform, ctypes
from dataclasses import dataclass

@dataclass
class _EnumPlatformSystemKV:
    NUMBER: int
    NAME: str

    def __eq__(self, value):
        return self.NUMBER == value.NUMBER
    
    def __ne__(self, value):
        return not self.__eq__(value)

class EnumPlatformSystem:
    LINUX = _EnumPlatformSystemKV(0, "Linux")
    WINDOWS = _EnumPlatformSystemKV(1, "Windows")

def current_os():
    if platform.system() == EnumPlatformSystem.WINDOWS.NAME:
        return EnumPlatformSystem.WINDOWS
    elif platform.system() == EnumPlatformSystem.LINUX.NAME:
        return EnumPlatformSystem.LINUX
    else:
        raise RuntimeError(f"Error: unsupported OS: {platform.system()}")
    
def get_mount_partitions():
    if current_os() == EnumPlatformSystem.WINDOWS:
        GetLogicalDrives = ctypes.windll.kernel32.GetLogicalDrives
        driveflags = GetLogicalDrives()

        if driveflags == 0:
            return []

        drives = []
        for i in range(26):
            if driveflags & (1 << i):
                drives.append(f"{chr(65 + i)}")

        return drives
    else:
        return []