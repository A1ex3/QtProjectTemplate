@echo off
setlocal enabledelayedexpansion

set "ARG_LIB_NAME=%1"
set "PWD=%CD%"

if "%ARG_LIB_NAME%"=="configure" (
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

    !PWD!\third_party\qt\configure.bat -no-pch -skip qtwebengine -skip qtdoc -release -prefix !ARG_DRIVE_LETTER!:\Qt\!ARG_QT_VERSION!
)

if "%ARG_LIB_NAME%"=="build" (
    if "%2"=="" (
        echo Error: No drive letter specified for Qt installation.
        exit /b 1
    )

    set "ARG_DRIVE_LETTER=%2"

    cd /d "!ARG_DRIVE_LETTER!:\Qt\qt-build"

    cmake --build !ARG_DRIVE_LETTER!:\Qt\qt-build --parallel
)

if "%ARG_LIB_NAME%"=="install" (
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

if "%ARG_LIB_NAME%"=="update_env" (
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
