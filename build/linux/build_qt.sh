#! /bin/bash

CURRENT_DIR="$(pwd)"

trap 'cd "$CURRENT_DIR"' EXIT

function configure () {
    qt_version="$1"

    if [ -z "$qt_version" ]; then
        echo Error: No Qt version specified.
        exit 1
    fi

    mkdir -p /tmp/Qt/qt-build
    mkdir -p /usr/lib/Qt/$qt_version && true || exit 1

    cd /tmp/Qt/qt-build

    $CURRENT_DIR/third_party/qt/configure \
    -no-pch \
    -shared \
    -opensource \
    -confirm-license \
    -nomake tools \
    -nomake tests \
    -nomake examples \
    -skip qt3d -skip qt5compat -skip qtactiveqt -skip qtcanvas3d -skip qtcharts \
    -skip qtcoap -skip qtconnectivity -skip qtdatavis3d -skip qtdeclarative \
    -skip qtdoc -skip qtfeedback -skip qtgamepad -skip qtgraphs -skip qtgrpc \
    -skip qthttpserver -skip qtimageformats -skip qtlanguageserver -skip qtlocation \
    -skip qtlottie -skip qtmqtt -skip qtmultimedia -skip qtnetworkauth -skip qtopcua \
    -skip qtpim -skip qtpositioning -skip qtqa -skip qtquick3d -skip qtquick3dphysics \
    -skip qtquickeffectmaker -skip qtquicktimeline -skip qtremoteobjects -skip qtrepotools \
    -skip qtscxml -skip qtsensors -skip qtserialbus -skip qtserialport -skip qtshadertools \
    -skip qtspeech -skip qtsvg -skip qtsystems -skip qttools -skip qttranslations \
    -skip qtvirtualkeyboard -skip qtwayland -skip qtwebchannel -skip qtwebengine \
    -skip qtwebglplugin -skip qtwebsockets -skip qtwebview -skip qtxmlpatterns \
    -release \
    -prefix /usr/lib/Qt/$qt_version
}

function build () {
    cmake --build /tmp/Qt/qt-build --parallel
}

function install () {
    qt_version="$1"

    if [ -z "$qt_version" ]; then
        echo Error: No Qt version specified.
        exit 1
    fi

    cmake --install /tmp/Qt/qt-build
}

function update_env () {
    qt_version="$1"
    qt_full_directory="/usr/lib/Qt/$qt_version"

    if [ -z "$qt_version" ]; then
        echo "Error: No Qt version specified."
        exit 1
    fi

    if [ ! -f /etc/profile ]; then
        echo "Error: /etc/profile file does not exist."
        exit 1
    fi

    if [ ! -d /etc/profile.d ]; then
        echo "Error: /etc/profile.d directory does not exist."
        exit 1
    fi

    echo "export PATH=\"\$PATH:$qt_full_directory/bin\"" | tee /etc/profile.d/qt_init.sh > /dev/null
    echo "export QT_FULL_DIRECTORY=\"$qt_full_directory\"" | tee -a /etc/profile.d/qt_init.sh > /dev/null

    chmod +x /etc/profile.d/qt_init.sh

    echo "Warning: use the command 'source /etc/profile' to update the environment variables!"
}

STAGE="$1"
if [ "$STAGE" = "configure" ]; then
    qt_version="$2"

    configure "$qt_version"

elif [ "$STAGE" = "build" ]; then
    build

elif [ "$STAGE" = "install" ]; then
    qt_version="$2"

    install "$qt_version"

elif [ "$STAGE" = "update_env" ]; then
    qt_version="$2"

    update_env "$qt_version"
else
    echo "Command not found!"
    exit 1
fi