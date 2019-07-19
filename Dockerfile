FROM debian:buster-slim as pybase
RUN apt update && \
    apt install -y git make python python-pip subversion && \
    apt clean

FROM pybase as sphinx2
RUN pip install sphinx==1.2.3

#--------------------
# Make site wide html
FROM sphinx2 as sitehtml
COPY ./src/ /tmp/src/
WORKDIR /tmp/src
RUN pip install http://effbot.org/media/downloads/xmlrpclib-1.0.1.zip unicodecsv && \
    make html && \
    chmod -R 0755 /tmp/src/_build/html


#-------------------------------
# TG 1.1 Doc Branch and API Docs
FROM sphinx2 as tg11docs
ARG BRANCH=1.1
ARG INSTURL=http://www.turbogears.org
ARG TG1SVN=svn://svn.code.sf.net/p/turbogears1/code

RUN pip install --upgrade 'SQLAlchemy<0.7a'
RUN svn co svn://svn.code.sf.net/p/turbogears1/code/docs/${BRANCH} /tmp/tg1
WORKDIR /tmp/tg1
RUN pip install http://www.turbogears.org/1.1/downloads/current/PEAK-Rules-0.5a1.dev-r2686.tar.gz && \
    pip install --trusted-host www.turbogears.org --upgrade --extra-index-url ${INSTURL}/${BRANCH}/downloads/current/index/ TurboGears
RUN make html && chmod -R 0755 /tmp/tg1/_build/html
RUN svn export ${TG1SVN}/branches/${BRANCH}/CHANGELOG.txt _build/html/
RUN pip install  'docutils==0.5' 'epydoc>=3.0' 'WebTest==1.2.3' #'SQLObject==1.1.1' 
RUN svn co svn://svn.code.sf.net/p/turbogears1/code/branches/${BRANCH} /tmp/tg1api
WORKDIR /tmp/tg1api
RUN python setup.py develop
RUN ./doc/build_api_docs.sh && chmod -R 0755 /tmp/tg1api/doc/api


#-------------------------------
# TG 1.5 Doc Branch and API Docs
FROM sphinx2 as tg15docs
ARG BRANCH=1.5
ARG INSTURL=http://www.turbogears.org
ARG TG1SVN=svn://svn.code.sf.net/p/turbogears1/code

RUN pip install --upgrade 'SQLAlchemy<0.7a'
RUN svn co svn://svn.code.sf.net/p/turbogears1/code/docs/${BRANCH} /tmp/tg1
WORKDIR /tmp/tg1
RUN pip install http://www.turbogears.org/1.5/downloads/current/PEAK-Rules-0.5a1.dev-r2707.tar.gz && \
    pip install --trusted-host www.turbogears.org --upgrade --extra-index-url ${INSTURL}/${BRANCH}/downloads/current/index/ TurboGears
RUN make html && chmod -R 0755 /tmp/tg1/_build/html
RUN svn export ${TG1SVN}/branches/${BRANCH}/CHANGELOG.txt _build/html/
RUN pip install  'docutils==0.5' 'epydoc>=3.0' 'WebTest==1.2.3' #'SQLObject==1.1.1' 
RUN svn co svn://svn.code.sf.net/p/turbogears1/code/branches/${BRANCH} /tmp/tg1api
WORKDIR /tmp/tg1api
RUN python setup.py develop
RUN ./doc/build_api_docs.sh && chmod -R 0755 /tmp/tg1api/doc/api

#------------------------------
# TG 2.0 Doc Branch common base
FROM sphinx2 as tg2docbase
RUN pip install --upgrade sqlalchemy python_memcached tgext.geo mapfish sphinx
RUN mkdir /tmp/tg2
RUN git clone https://github.com/TurboGears/tg2docs.git /tmp/tg2docs
WORKDIR /tmp/tg2docs

#------------
# TG 2.0 Docs
FROM tg2docbase as tg20docs
ARG BRANCH=a025e26483fcf5cdc800bd4d8bcac9ee290ef0a7
ARG VERSION=2.0
RUN git checkout ${BRANCH}
WORKDIR /tmp/tg2docs/docs
RUN /bin/echo -e "\nrelease ='${VERSION}'" >> conf.py
RUN make html && chmod -R 0755 /tmp/tg2docs/docs/_build/html


#------------
# TG 2.1 Docs
FROM tg2docbase as tg21docs
ARG BRANCH=tg2.1.5
ARG VERSION=2.1
RUN git checkout ${BRANCH}
WORKDIR /tmp/tg2docs/docs
RUN /bin/echo -e "\nrelease ='${VERSION}'" >> conf.py
RUN make html && chmod -R 0755 /tmp/tg2docs/docs/_build/html


#---------------------------
# Prepare final static image
FROM nginx:latest
RUN rm -rf /usr/share/nginx/html

COPY --chown=nobody:nogroup --from=sitehtml /tmp/src/_build/html /usr/share/nginx/html/
COPY --chown=nobody:nogroup                 ./static/1.0         /usr/share/nginx/html/1.0
COPY --chown=nobody:nogroup --from=tg11docs /tmp/tg1/_build/html /usr/share/nginx/html/1.1/docs
COPY --chown=nobody:nogroup --from=tg11docs /tmp/tg1api/doc/api  /usr/share/nginx/html/1.1/docs/api
COPY --chown=nobody:nogroup --from=tg15docs /tmp/tg1/_build/html /usr/share/nginx/html/1.5/docs
COPY --chown=nobody:nogroup --from=tg15docs /tmp/tg1api/doc/api  /usr/share/nginx/html/1.5/docs/api
COPY --chown=nobody:nogroup --from=tg20docs /tmp/tg2docs/docs/_build/html /usr/share/nginx/html/2.0/docs
COPY --chown=nobody:nogroup --from=tg21docs /tmp/tg2docs/docs/_build/html /usr/share/nginx/html/2.1/docs
COPY --chown=nobody:nogroup                 ./static/google4bdb33412f144140.html /usr/share/nginx/html
COPY --chown=nobody:nogroup                 ./static/EP2012      /usr/share/nginx/html
COPY --chown=nobody:nogroup                 ./static/packages    /usr/share/nginx/html/packages
COPY --chown=nobody:nogroup                 ./static/1.1/downloads /usr/share/nginx/html/1.1/downloads
COPY --chown=nobody:nogroup                 ./static/1.5/downloads /usr/share/nginx/html/1.5/downloads
COPY --chown=nobody:nogroup                 ./static/2.0/downloads /usr/share/nginx/html/2.0/downloads
COPY --chown=nobody:nogroup                 ./static/2.1/downloads /usr/share/nginx/html/2.1/downloads
COPY --chown=nobody:nogroup                 ./static/2.2/downloads /usr/share/nginx/html/2.2/downloads
COPY --chown=nobody:nogroup                 ./static/2.3/downloads /usr/share/nginx/html/2.3/downloads
