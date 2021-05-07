#!/bin/sh
SCRIPTDIR=$(dirname "$0")
mkdir -p /usr/local/share/rm-sec-toolkit
ln -s "$(pwd)/$SCRIPTDIR/modules" /usr/local/share/rm-sec-toolkit/modules