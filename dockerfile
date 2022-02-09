# Pull base image.
FROM snakemake/snakemake

LABEL MAINTAINER = nunoporsche@hotmail.com

WORKDIR /project/
COPY scripts/ /project/scripts/
COPY files/ /project/files/
COPY requirements.txt /project/
COPY tests/ /project/tests/
COPY Snakefile /project/

RUN apt-get update && \
    apt-get install raxml -y && \
    apt-get install -y apt-utils && \
    apt-get install libgconf-2-4 -y && \
    apt-get install libgtk2.0.0 -y

RUN dpkg -i files/mega_11.0.9-1_amd64.deb 

RUN conda install -c bioconda iqtree 

RUN pip3 install requests==2.25.1 && \
    pip3 install -r requirements.txt 
