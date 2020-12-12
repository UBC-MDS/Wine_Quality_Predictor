############################################################
# Dockerfile to build wine_quality_prediction images
# Based on Ubuntu
############################################################

#Set base image to Ubuntu
FROM jupyter/scipy-notebook


################## BEGIN INSTALLATION ######################
#Install python basics

# Create Timezon Variable
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Beijing

USER root  
RUN wget -N http://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /app

# needed for installing Chrome
RUN apt-get update && apt-get install -y gnupg2
RUN apt-get install -y xvfb

# pip install required libraries
RUN pip install psutil>=5.7.2\
    git+git://github.com/mgelbart/plot-classifier.git\
    chromedriver-binary-auto

 # install Chrome to use with altair save
RUN \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*   

#Install other dependancies
RUN pip3 install matplotlib>=3.2.2
RUN pip3 install scikit-learn>=0.23.2
RUN pip3 install scipy==1.5.3
RUN pip3 install numpy>=1.19.4
RUN pip3 install pandas>=1.1.3
RUN pip3 install matplotlib>=3.3.3
RUN pip3 install requests>=2.24.0
RUN pip3 install graphviz
RUN pip3 install altair>=4.1.0
RUN pip3 install jinja2
RUN pip3 install pip>=20
RUN pip3 install pandas-profiling>=1.4.3
RUN pip3 install psutil>=5.7.2
RUN pip3 install xgboost>=1.*
RUN pip3 install lightgbm>=3.*
RUN pip3 install git+git://github.com/mgelbart/plot-classifier.git
RUN pip3 install altair-saver==0.5.0
RUN pip3 install docopt==0.6.2
RUN pip3 install selenium==3.141.0
RUN pip3 install webdriver-manager==3.2.2

RUN conda install -y -c anaconda python-chromedriver-binary


CMD ["echo Finish Creating Docker Image!"]
