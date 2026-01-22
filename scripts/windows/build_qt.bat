@echo off
setlocal enabledelayedexpansion

set "ARG_STAGE=%1"
set "PWD=%CD%"
set "PYTHON_LOGGER=!PWD!\scripts\logger.py"
set "LOG_FILE=!PWD!\scripts\logs\build_data.log"
set "PATH_TO_THIS_FILE=!PWD!\scripts\windows\build_qt.bat"

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
    -qt-pcre ^
    -qt-zlib ^
    -qt-harfbuzz ^
    -qt-libpng ^
    -qt-libjpeg ^
    -skip qt3d ^
    -skip qt5compat ^
    -skip qtactiveqt ^
    -skip qtcanvas3d ^
    -skip qtcharts ^
    -skip qtcoap ^
    -skip qtconnectivity ^
    -skip qtdatavis3d ^
    -skip qtdoc ^
    -skip qtfeedback ^
    -skip qtgamepad ^
    -skip qtgraphs ^
    -skip qtgrpc ^
    -skip qthttpserver ^
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
    -skip qtspeech ^
    -skip qtsystems ^
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

    for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "TMP_PATH=%%B"
    for /f "tokens=2*" %%A in ('reg query "HKEY_CURRENT_USER\Environment" /v Path') do set "TMP_USER_PATH=%%B"

    echo !TMP_PATH! | find /i "!ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!\bin" >nul
    if not errorlevel 1 (
        echo Info: Path to "!ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!\bin" is already in PATH.
    ) else (
        python !PYTHON_LOGGER! ^
        --log_file_path !LOG_FILE! ^
        --executable_file_path !PATH_TO_THIS_FILE! ^
        --log_msg_level info ^
        --log_msg "Snapshot of the system environment variable 'Path', before data update. Data: !TMP_PATH!"

        python !PYTHON_LOGGER! ^
        --log_file_path !LOG_FILE! ^
        --executable_file_path !PATH_TO_THIS_FILE! ^
        --log_msg_level info ^
        --log_msg "Snapshot of the user environment variable 'Path', before data update. Data: !TMP_USER_PATH!"

        setx /M Path "!ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!\bin;!TMP_PATH!"
    )

    if not defined QT_PATH (
        setx /M QT_PATH "!ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!"
    ) else (
        if "%QT_PATH%" neq "!ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!" (
            setx /M QT_PATH "!ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!"
        )
    )
)

cd "%PWD%"
endlocal