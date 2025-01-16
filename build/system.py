import platform, os

def current_os():
    if platform.system() == "Windows":
        return "windows"
    elif platform.system() == "Linux":
        return "linux"
    else:
        assert 1==0, f"Error: unsupported OS: {platform.system()}"
    
def get_mount_partitions():
    if current_os() == "windows":
        return [drive.strip().replace(":", "") for drive in os.popen('wmic logicaldisk get name').read().splitlines() if drive.strip() and not drive.startswith('Name')]
    else:
        return []