#!/bin/bash

#TODO: Need to make a 'makebook' function
#TODO: Need to silence sphinx
#TODO: Add search box on site template. Include doc page inventories for searching

REPOROOT=${HOME}/siterepo
SITEREPOROOT=${REPOROOT}/website
TGDOCS=${REPOROOT}/tg2docs

WORK=${HOME}/tgsiteworkspace
SITE=${HOME}/tgsite
VENVROOT=${HOME}/virtualenvs

TGSITEURL=https://github.com/TurboGears/tgwebsite.git
TGDOCSURL=https://github.com/TurboGears/tg2docs.git

function sitesync() {
    SRC=$1
    DEST=$2
    OPTS=$3
    rsync -a ${OPTS} ${SRC} ${DEST}
}

function mkvenv() {
    NAME=$1
    test -e ${VENVROOT}/${NAME} || virtualenv --no-site-packages ${VENVROOT}/${NAME}
}

function venvon() {
    VENV=$1
    source ${VENVROOT}/${VENV}/bin/activate
}

function venvoff() {
    deactivate
}

function invenv() {
    VENV=shift
    CMD=shift

    venvon ${VENV}
    ${CMD} $*
    venvoff
}

function checkcommands() {
    PROBLEMS=""
    for i in git make rsync virtualenv sphinx-build; do
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
    test -e ${REPOROOT} || mkdir -p ${REPOROOT}
    test -e ${SITE} || mkdir -p ${SITE}
    test -e ${SITEREPOROOT} || git clone ${TGSITEURL} ${SITEREPOROOT}
    test -e ${TGDOCS} || git clone ${TGDOCSURL} ${TGDOCS}
    
    mkdir -p ${WORK}
    
    cd ${SITEREPOROOT}
    git pull
    cd ${TGDOCS}
    git pull
}

function makesitehtml() {
    mkvenv sitebuild
    venvon sitebuild
    pip install --upgrade sphinx
    cd ${SITEREPOROOT}/src
    test -e _build && rm -rf _build
    ${SITEREPOROOT}/bin/cogbin.py
    make html
    git checkout cogbin.rst
    sitesync ${SITEREPOROOT}/src/_build/html/ ${WORK}/
    venvoff
}

function maketg2docbranch() {
    BRANCH=$1
    OUTLOC=${WORK}/$2
    mkvenv docsbuild
    venvon docsbuild
    pip install --upgrade sqlalchemy python_memcached tgext.geo mapfish sphinx
    cd ${TGDOCS}
    git checkout ${BRANCH}
    cd docs
    test -e _build && rm -rf _build
    make html
    test -e ${OUTLOC} || mkdir -p ${OUTLOC}
    sitesync _build/html/ ${OUTLOC}/
    rm -rf _build/html
    venvoff
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

# sync 1.0/docs to top of workspace
# sync 1.0/downloads to top of workspace
# sync 1.1/docs to top of workspace
# sync 1.1/downloads to top of workspace
# sync 1.5/docs to top of workspace
# sync 1.5/downloads to top of workspace
# sync 2.0/downloads to top of workspace
# sync 2.1/downloads to top of workspace
# sync 2.2/downloads to top of workspace
# sync remaining static files to top of workspace
# generate planet and sync to top of workspace

finalize
