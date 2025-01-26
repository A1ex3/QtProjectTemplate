import platform, ctypes

def current_os():
    if platform.system() == "Windows":
        return "windows"
    elif platform.system() == "Linux":
        return "linux"
    else:
        assert 1==0, f"Error: unsupported OS: {platform.system()}"
    
def get_mount_partitions():
    if current_os() == "windows":
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