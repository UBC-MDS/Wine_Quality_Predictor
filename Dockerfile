############################################################
# Dockerfile to build wine_quality_prediction images
# Based on Ubuntu
############################################################

#Set base image to Ubuntu
FROM selenium/standalone-chrome

#Update repositor source list
RUN sudo apt-get update

################## BEGIN INSTALLATION ######################
#Install python basics
RUN sudo apt-get -y install \
	build-essential \
	python-dev \
	python-setuptools

# Create Timezon Variable
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Beijing
# Install tzdata
RUN sudo apt-get install -y tzdata

# Install python pip
RUN sudo apt-get -y install python3-pip

RUN sudo apt-get -y install git-all

#Install other dependancies
RUN sudo pip3 install matplotlib>=3.2.2
RUN sudo pip3 install scikit-learn>=0.23.2
RUN sudo pip3 install scipy==1.5.3
RUN sudo pip3 install numpy>=1.19.4
RUN sudo pip3 install pandas>=1.1.3
RUN sudo pip3 install matplotlib>=3.3.3
RUN sudo pip3 install requests>=2.24.0
RUN sudo pip3 install graphviz
RUN sudo pip3 install altair>=4.1.0
RUN sudo pip3 install jinja2
RUN sudo pip3 install pip>=20
RUN sudo pip3 install pandas-profiling>=1.4.3
RUN sudo pip3 install psutil>=5.7.2
RUN sudo pip3 install xgboost>=1.*
RUN sudo pip3 install lightgbm>=3.*
RUN sudo pip3 install git+git://github.com/mgelbart/plot-classifier.git
RUN sudo pip3 install altair-saver==0.5.0
RUN sudo pip3 install docopt==0.6.2
RUN sudo pip3 install selenium==3.141.0
RUN sudo pip3 install webdriver-manager==3.2.2



CMD ["echo Finish Creating Docker Image!"]
