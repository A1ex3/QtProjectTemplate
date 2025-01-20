# Build instructions for Linux

## Requirements:
- gcc (>=10)
- python (>= 3.10)
- cmake (>=3.25)
- ninja (>=1.12.1)

## Platform Plugin Dependencies [Qt6](https://doc.qt.io/qt-6/linux-requirements.html)
| Library                                 |
|-----------------------------------------|
| libatspi2.0-dev                         |
| libbluetooth-dev                        |
| libclang-dev                            |
| libcups2-dev                            |
| libdrm-dev                              |
| libegl1-mesa-dev                        |
| libfontconfig1-dev                      |
| libfreetype6-dev                        |
| libgstreamer1.0-dev                     |
| libhunspell-dev                         |
| libnss3-dev                             |
| libopengl-dev                           |
| libpulse-dev                            |
| libssl-dev                              |
| libts-dev                               |
| libx11-dev                              |
| libx11-xcb-dev                          |
| libxcb-glx0-dev                         |
| libxcb-icccm4-dev                       |
| libxcb-image0-dev                       |
| libxcb-keysyms1-dev                     |
| libxcb-randr0-dev                       |
| libxcb-render-util0-dev                 |
| libxcb-shape0-dev                       |
| libxcb-shm0-dev                         |
| libxcb-sync-dev                         |
| libxcb-util-dev                         |
| libxcb-xfixes0-dev                      |
| libxcb-xinerama0-dev                    |
| libxcb-xkb-dev                          |
| libxcb1-dev                             |
| libxcomposite-dev                       |
| libxcursor-dev                          |
| libxdamage-dev                          |
| libxext-dev                             |
| libxfixes-dev                           |
| libxi-dev                               |
| libxkbcommon-dev                        |
| libxkbcommon-x11-dev                    |
| libxkbfile-dev                          |
| libxrandr-dev                           |
| libxrender-dev                          |
| libxshmfence-dev                        |
| libxshmfence1                           |

## Clone source code.
```bash
git clone https://github.com/A1ex3/QtProjectTemplate.git
```

## Prepare dependencies. Note: for the script to work correctly, you must use the `bash` shell and run the script with root privileges.
```bash
python3 configure.py
```

## Use to update the environment variables.
```bash
source /etc/profile
```

### Build the project.
```bash
cmake -S . -B out -G Ninja
```

```bash
cmake --build out --config <Debug|Release>
```