FROM hysds/pge-base:latest

LABEL maintainer="hysds"

USER ops

RUN mkdir -p /home/ops/tool
COPY ./barn/Miniconda3-latest-Linux-x86_64.sh /home/ops/tool
COPY ./barn/plant.install.sh /home/ops/tool

#RUN ls ~/tool

# install miniconda and PLAnT
# to rid of some warnings from install line below
RUN mkdir -p ~/.conda && \
    # ref: https://docs.anaconda.com/anaconda/install/silent-mode/
    sh ~/tool/Miniconda3-latest-Linux-x86_64.sh -b -p ~/tool/miniconda3 && \
    rm ~/tool/Miniconda3-latest-Linux-x86_64.sh && \
    # install PLAnT
    sh ~/tool/plant.install.sh . && \
    rm ~/tool/plant.install.sh

#RUN ls ~/tool

# the tool to generate gcov product
RUN mkdir -p ~/verdi/ops/s1-gcov-plant
COPY ./covmat.py     /home/ops/verdi/ops/s1-gcov-plant
COPY ./create_nc4.py /home/ops/verdi/ops/s1-gcov-plant
COPY ./util.py       /home/ops/verdi/ops/s1-gcov-plant
COPY ./run.sh        /home/ops/verdi/ops/s1-gcov-plant

# Change to work directory
WORKDIR /home/ops

# Run shell
CMD ["/bin/bash", "--login"]

#RUN useradd -u 2000 hysds

#RUN sudo -u hysds mkdir /home/hysds/tool

## Set to root user
#USER root
#
## Install ISCE2
#RUN source /opt/conda/bin/activate root \
# && conda install -c conda-forge isce2
#
## Install directory
#ENV ISCE_HOME /opt/conda/lib/python3.7/site-packages/isce
#ARG ISCE_APPS_DIR=${ISCE_HOME}/applications
#ARG STACK_INSTALL_DIR=${ISCE_HOME}/components/contrib/stack
#ARG TOPSSTACK_INSTALL_DIR=${STACK_INSTALL_DIR}/topsStack
#ARG TOPSSTACK_COPY_DIR=/root/topsStack
#ENV PATH ${PATH}:${ISCE_APPS_DIR}:${TOPSSTACK_INSTALL_DIR}
#
## Copy stack processor code into docker image
##COPY topsStack $TOPSSTACK_COPY_DIR
#
## Copy stack processor code into install directory; Adjust group permissions
## so stack processor and associated logs can be written.
#RUN mkdir -p $STACK_INSTALL_DIR \
# && cp -r $TOPSSTACK_COPY_DIR $STACK_INSTALL_DIR \
# && rm -rf $TOPSSTACK_COPY_DIR
#
#RUN cd /etc/yum.repos.d/ && \
#    wget http://download.opensuse.org/repositories/home:/tange/CentOS_CentOS-6/home:tange.repo && \
#    yum install parallel -y && \
#    yum clean all
#
## Set to ops user
#USER ops
#
## Copy topsStack PGE into docker image
#COPY . /home/ops/verdi/ops/topsstack
#
## Change to work directory
#WORKDIR /home/ops
#
## Run shell
#CMD ["/bin/bash", "--login"]
