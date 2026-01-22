#! /bin/bash

echo "Updating and installing tools..."
apt update && apt upgrade -y
apt install meson pkg-config autoconf automake libtool bison m4 libgl1-mesa-dev patchelf zsync libcurl4-openssl-dev squashfs-tools desktop-file-utils \
    x11proto-core-dev x11proto-dev libexpat1-dev libwayland-dev xutils-dev gperf libgcrypt-dev libarchive-dev libgpgme-dev libgpg-error-dev \
    libicu-dev libharfbuzz-dev \
    gcc g++ git curl wget make cmake ninja-build python3 -y

echo "Qt for X11 Requirements..."
apt install \
    libfontconfig1-dev \
    libfreetype-dev \
    libgtk-3-dev \
    libx11-dev \
    libx11-xcb-dev \
    libxcb-cursor-dev \
    libxcb-cursor0 \
    libxcb-glx0-dev \
    libxcb-icccm4-dev \
    libxcb-image0-dev \
    libxcb-keysyms1-dev \
    libxcb-randr0-dev \
    libxcb-render-util0-dev \
    libxcb-render0-dev \
    libxcb-shape0-dev \
    libxcb-shm0-dev \
    libxcb-sync-dev \
    libxcb-util-dev \
    libxcb-xfixes0-dev \
    libxcb-xkb-dev \
    libxcb1-dev \
    libxext-dev \
    libxfixes-dev \
    libxi-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    libxrender-dev \
    -y