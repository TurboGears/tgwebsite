#!/bin/bash

REPOROOT=${HOME}/siterepo
SITEREPOROOT=${REPOROOT}/website
TGDOCS=${REPOROOT}/tg2docs

WORK=${HOME}/tgsiteworkspace
SITE=${HOME}/tgsite
VENVROOT=${HOME}/virtualenvs

TGSITEURL=https://github.com/TurboGears/tgwebsite.git
TGDOCSURL=https://github.com/TurboGears/tg2docs.git
INSTURL=http://www.turbogears.org
TG1SVN=svn://svn.code.sf.net/p/turbogears1/code

function sitesync() {
    SRC=$1
    DEST=$2
    OPTS=$3
    test -e ${DEST} || mkdir -p ${DEST}
    rsync -a ${OPTS} ${SRC} ${DEST}
}

function syncfolder() {
    FLD=$1
    sitesync ${SITEREPOROOT}/static/${FLD}/ ${WORK}/${FLD}/
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
    for i in git make rsync virtualenv sphinx-build svn; do
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
    for v in 1.1 1.5 ; do
	test -e ${REPOROOT}/docs-${v} || svn checkout ${TG1SVN}/docs/${v} ${REPOROOT}/docs-${v}
	test -e ${REPOROOT}/apidocs-${v} || svn checkout ${TG1SVN}/branches/${v} ${REPOROOT}/apidocs-${v}
    done
    
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
    make html
    sitesync ${SITEREPOROOT}/src/_build/html/ ${WORK}/
    venvoff
}

function maketg1docbranch() {
    BRANCH=$1
    OUTLOC=${WORK}/$2
    mkvenv docsbuild1
    venvon docsbuild1
    pip install --upgrade SQLObject 'SQLAlchemy<0.7a' 'Sphinx!=1.2b1'
    if [ ${BRANCH} == "1.0" ]; then
	BRANCH=1.1
    fi
    pip install --upgrade -i ${INSTURL}/${BRANCH}/downloads/current/index ${PACKAGE}
    cd ${REPOROOT}/docs-${BRANCH}
    rm -rf _build/html
    svn update .
    mkdir -p ../../branches/${BRANCH}
    svn export ${TG1SVN}/branches/${BRANCH}/CHANGELOG.txt ../../branches/${BRANCH}/CHANGELOG.txt
    make clean
    make html
    sitesync _build/html/ ${OUTLOC}/
    rm ../../branches/${BRANCH}/CHANGELOG.txt
    rmdir ../../branches/${BRANCH}
    rmdir ../../branches
    rm -rf _build/html
    venvoff
}

function maketg1apidocs() {
    BRANCH=$1
    OUTLOC=${WORK}/$2
    if [ ${BRANCH} == "1.0" ]; then
	BRANCH=1.1
    fi
    mkvenv apidocsbuild1-${BRANCH}
    venvon apidocsbuild1-${BRANCH}
    pip install --upgrade 'docutils==0.5' 'epydoc>=3.0' 'SQLObject==1.1.1' 'SQLAlchemy==0.6.8' 'WebTest==1.2.3'
    cd ${REPOROOT}/apidocs-${BRANCH}
    rm -rf doc/api
    python setup.py develop
    ./doc/build_api_docs.sh
    venvoff
    sitesync doc/api/ ${WORK}/${BRANCH}/docs/api/
    rm -rf doc/api
}

function maketg2book() {
    mkvenv bookbuild
    venvon bookbuild
    cd ${TGDOCS}
    git checkout development
    cd book
    python setup.py develop
    pip install nose dulwich==0.8.5 tw.forms simplejson zope.interface simplegeneric repoze.who-testutil repoze.who-friendlyform repoze.who.plugins.sa repoze.what-quickstart repoze.what-pylons repoze.what.plugins.sql kid decorator coverage WebTest WebOb WebHelpers WebFlash TurboGears2 Tempita SymbolType SQLAlchemy Routes PEAK-Rules MarkupSafe Genshi Extremes DecoratorTools BytecodeAssembler Babel AddOns
    test -e _build && rm -rf _build
    make html
    venvoff
    sitesync _build/html/ ${WORK}/book/
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

function syncstaticfiles() {
    rsync -a ${SITEREPOROOT}/static/google4bdb33412f144140.html ${WORK}/
}

function cleanup() {
    rm -rf ${WORK}
    exit
}

function finalize() {
    chmod -R 0755 ${WORK}
    sitesync ${WORK}/ ${SITE}/ --delete
}

trap cleanup SIGINT SIGTERM SIGHUP

checkcommands
workinit

makesitehtml
#maketg2book

maketg1docbranch 1.1 1.1/docs
maketg1apidocs 1.1 1.1/docs/api
maketg1docbranch 1.5 1.5/docs
maketg1apidocs 1.5 1.5/docs/api
maketg2docbranch a025e26483fcf5cdc800bd4d8bcac9ee290ef0a7 2.0/docs
maketg2docbranch tg2.1.5 2.1/docs

syncfolder packages

syncfolder 1.0
syncfolder 1.1/downloads
syncfolder 1.5/downloads
syncfolder 2.0/downloads
syncfolder 2.1/downloads
syncfolder 2.2/downloads
syncfolder 2.3/downloads

${SITEREPOROOT}/planet/updplanet ${WORK}/planet

syncstaticfiles
finalize
cleanup
