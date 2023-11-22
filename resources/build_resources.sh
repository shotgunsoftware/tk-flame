#!/usr/bin/env bash
#
# Copyright (c) 2021 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

# The path to output all built .py files to:
UI_PYTHON_PATH=../python/tk_flame/ui


# Helper functions to build UI files
function build_qt {
    echo " > Building " $2

    # compile ui to python
    echo "$1 $2 > $UI_PYTHON_PATH/$3.py"
    $1 $2 > $UI_PYTHON_PATH/$3.py

    # replace PySide imports with sgtk.platform.qt and remove line containing Created by date
    sed -i"" -E "s/^(from PySide.\.QtWidgets)(.*)$//g" $UI_PYTHON_PATH/$3.py
    sed -i"" -E "s/^(from PySide.\.)(\w*)(.*)$/from sgtk.platform.qt import \2\nfor name, cls in \2.__dict__.items():\n    if isinstance(cls, type): globals()[name] = cls\n/g" $UI_PYTHON_PATH/$3.py
    sed -i"" -E "s/^(from PySide. import)(.*)$/from sgtk.platform.qt import\2/g" $UI_PYTHON_PATH/$3.py

    sed -i"" -E 's/u\"/\"/g' $UI_PYTHON_PATH/$3.py
}

function build_ui {
    ver=$($1 --version | cut -d' ' -f2 | cut -d. -f1)
    gt6=$(echo "$ver >= 6" | /usr/bin/bc)
    if [ "1" -eq "$gt6" ] ; then
        # running > Qt6
        build_qt "$1 -g python --from-imports --star-imports" "$2.ui" "$2"
    else
        # running < Qt6
        build_qt "$1 -g python --from-imports" "$2.ui" "$2"
    fi
}

function build_res {
    build_qt "$1 -g python" "$2.qrc" "$2_rc"
}


while getopts u:r: flag
do
    case "${flag}" in
        u) uic=${OPTARG};;
        r) rcc=${OPTARG};;
    esac
done

if [ -z "$uic" ]; then
    echo "the PySide uic compiler must be specified with the -u parameter"
    exit 1
fi

if [ -z "$rcc" ]; then
    echo "the PySide rcc compiler must be specified with the -r parameter"
    exit 1
fi

uicversion=$(${uic} --version)
rccversion=$(${rcc} --version)


if [ -z "$uicversion" ]; then
    echo "the PySide uic compiler version cannot be determined"
    exit 1
fi

if [ -z "$rccversion" ]; then
    echo "the PySide rcc compiler version cannot be determined"
    exit 1
fi

echo "Using PySide uic compiler version: ${uicversion}"
echo "Using PySide rcc compiler version: ${rccversion}"

# build UI's:
echo "building user interfaces..."
build_ui $uic project_create_dialog

# build resources
echo "building resources..."
build_res $rcc resources
