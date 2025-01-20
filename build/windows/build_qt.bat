@echo off
setlocal enabledelayedexpansion

set "ARG_STAGE=%1"
set "PWD=%CD%"

if "%ARG_STAGE%"=="configure" (
    if "%2"=="" (
        echo Error: No drive letter specified for Qt installation.
        exit /b 1
    )
    if "%3"=="" (
        echo Error: No Qt version specified.
        exit /b 1
    )

    set "ARG_DRIVE_LETTER=%2"
    set "ARG_QT_VERSION=%3"

    cd /d "!ARG_DRIVE_LETTER!:\"
    cd \

    if not exist "Qt" (
        md "Qt"
    )

    cd "Qt"

    if not exist "!ARG_QT_VERSION!" (
        md "!ARG_QT_VERSION!"
    )

    if not exist "qt-build" (
        md "qt-build"
    )
    cd "qt-build"

    !PWD!\third_party\qt\configure.bat ^
    -no-pch ^
    -shared ^
    -opensource ^
    -confirm-license ^
    -nomake tests ^
    -nomake examples ^
    -skip qt3d ^
    -skip qt5compat ^
    -skip qtactiveqt ^
    -skip qtcanvas3d ^
    -skip qtcharts ^
    -skip qtcoap ^
    -skip qtconnectivity ^
    -skip qtdatavis3d ^
    -skip qtdeclarative ^
    -skip qtdoc ^
    -skip qtfeedback ^
    -skip qtgamepad ^
    -skip qtgraphs ^
    -skip qtgrpc ^
    -skip qthttpserver ^
    -skip qtimageformats ^
    -skip qtlanguageserver ^
    -skip qtlocation ^
    -skip qtlottie ^
    -skip qtmqtt ^
    -skip qtmultimedia ^
    -skip qtnetworkauth ^
    -skip qtopcua ^
    -skip qtpim ^
    -skip qtpositioning ^
    -skip qtqa ^
    -skip qtquick3d ^
    -skip qtquick3dphysics ^
    -skip qtquickeffectmaker ^
    -skip qtquicktimeline ^
    -skip qtremoteobjects ^
    -skip qtrepotools ^
    -skip qtscxml ^
    -skip qtsensors ^
    -skip qtserialbus ^
    -skip qtserialport ^
    -skip qtshadertools ^
    -skip qtspeech ^
    -skip qtsvg ^
    -skip qtsystems ^
    -skip qttools ^
    -skip qttranslations ^
    -skip qtvirtualkeyboard ^
    -skip qtwayland ^
    -skip qtwebchannel ^
    -skip qtwebengine ^
    -skip qtwebglplugin ^
    -skip qtwebsockets ^
    -skip qtwebview ^
    -skip qtxmlpatterns ^
    -release ^
    -prefix !ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!
)

if "%ARG_STAGE%"=="build" (
    if "%2"=="" (
        echo Error: No drive letter specified for Qt installation.
        exit /b 1
    )

    set "ARG_DRIVE_LETTER=%2"

    cd /d "!ARG_DRIVE_LETTER!:\Qt\qt-build"

    cmake --build !ARG_DRIVE_LETTER!:\Qt\qt-build --parallel
)

if "%ARG_STAGE%"=="install" (
    if "%2"=="" (
        echo Error: No drive letter specified for Qt installation.
        exit /b 1
    )
    if "%3"=="" (
        echo Error: No Qt version specified.
        exit /b 1
    )

    set "ARG_DRIVE_LETTER=%2"
    set "ARG_QT_VERSION=%3"

    cd /d "!ARG_DRIVE_LETTER!:\Qt\qt-build"

    cmake --install !ARG_DRIVE_LETTER!:\Qt\qt-build
)

if "%ARG_STAGE%"=="update_env" (
    if "%2"=="" (
        echo Error: No drive letter specified for Qt installation.
        exit /b 1
    )
    if "%3"=="" (
        echo Error: No Qt version specified.
        exit /b 1
    )

    set "ARG_DRIVE_LETTER=%2"
    set "ARG_QT_VERSION=%3"

    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "!ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!\bin;%PATH%" /f
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v QT_FULL_DIRECTORY /t REG_EXPAND_SZ /d "!ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!" /f

    setx Path "%Path%"
)

cd "%PWD%"
endlocal
