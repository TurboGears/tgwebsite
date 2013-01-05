#!/bin/bash

#TODO: Need to make a virtualenv that has the latest sphinx, along with all the needed packages for the various versions of the docs.
#TODO: Need to make a 'makebook' function
#TODO: Need to silence sphinx
#TODO: Add search box on site template. Include doc page inventories for searching

SRC=`pwd`
WORK=${HOME}/tgsiteworkspace
SITE=${HOME}/tgsite
TGDOCS=${HOME}/tgdocs
TGDOCSURL=https://github.com/TurboGears/tg2docs.git

function sitesync() {
    SRC=$1
    DEST=$2
    OPTS=$3
    rsync -a ${OPTS} ${SRC} ${DEST}
}

function checkcommands() {
    PROBLEMS=""
    for i in git make rsync ; do
	which ${i} >/dev/null 2>&1
	if [ $? -ne 0 ]; then
	    echo Missing command: ${i}
	    PROBLEMS="${PROBLEMS} ${i}"
	fi
    done
    if [ ! -z "${PROBLEMS}" ]; then
	echo Aborting
	exit 2
    fi
}

function workinit() {
    test -e ${WORK} && exit 1
    test -e ${SITE} || mkdir -p ${SITE}
    mkdir -p ${WORK}
    cd ${SRC}
    git pull
    test -e ${TGDOCS} || git clone ${TGDOCSURL} ${TGDOCS}
    cd ${TGDOCS}
    git pull
}

function makesitehtml() {
    cd ${SRC}/src
    rm -rf _build
    mkdir _build
    touch _build/.hidden
    make html
    sitesync ${SRC}/src/_build/html/ ${WORK}/
}

function maketg2docbranch() {
    BRANCH=$1
    OUTLOC=${WORK}/$2
    cd ${TGDOCS}
    git checkout ${BRANCH}
    cd docs
    test -e _build && rm -rf _build
    make html
    test -e ${OUTLOC} || mkdir -p ${OUTLOC}
    sitesync _build/html/ ${OUTLOC}/
    rm -rf _build/html
}

function finalize() {
    chmod -R 0755 ${WORK}
    sitesync ${WORK}/ ${SITE}/ --delete
    rm -rf ${WORK}
}

checkcommands
workinit
makesitehtml
maketg2docbranch a025e26483fcf5cdc800bd4d8bcac9ee290ef0a7 2.0/docs
maketg2docbranch tg2.1.5 2.1/docs
maketg2docbranch development 2.2/docs

# sync 1.0 to top of workspace
# sync 1.1 to top of workspace
# sync 1.5 to top of workspace
# sync 2.0/downloads to top of workspace
# sync 2.1/downloads to top of workspace
# sync 2.2/downloads to top of workspace
# sync remaining static files to top of workspace
# generate cogbin and sync to top of workspace
# generate planet and sync to top of workspace

finalize
