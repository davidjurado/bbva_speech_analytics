# Pull tensorflow image with Python3
FROM tensorflow/tensorflow:2.3.0
#FROM continuumio/anaconda3:latest

# Set the working directory to /app
WORKDIR /app

# Transfer content from current dir to /app in container
ADD . /app

# Install audio libraries
RUN apt-get update

# Install python packages
# pip install -r requirements.txt
#RUN conda env create -f environment.yml
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN conda env create -f environment.yml
#SHELL ["conda", "run", "-n", "tensorflow", "/bin/bash", "-c"]

#RUN conda install -c anaconda flask -y && conda install -c conda-forge/label/cf201901 uwsgi
#RUN conda install -c anaconda flask -y && pip install uwsgi
#RUN conda env update --file environment.yml
#RUN conda install python=3.6
#RUN conda install -c conda-forge uwsgi -y && pip install tensorflow==2.3.0 && conda install -c anaconda nltk -y && conda install -c anaconda flask -y


#RUN conda init bash
#RUN conda activate tensorflow

# Start uWSGI using config file
#CMD ["conda", "run", "-n", "tensorflow", "uwsgi", "app.ini"]
CMD ["uwsgi", "app.ini"]