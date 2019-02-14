FROM continuumio/miniconda3
MAINTAINER Lorenzo Riches "lo.riches@gmail.com"

ADD . /app
WORKDIR /app

RUN conda env create -n eee -f /app/environment.yml
# Pull the environment name out of the environment.yml
RUN echo "source activate eee" > ~/.bashrc
ENV PATH /opt/conda/envs/eee/bin:$PATH

VOLUME /data

ENTRYPOINT ["python","./app.py"]