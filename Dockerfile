FROM debian:10

# Install R per instructions below
# https://linuxize.com/post/how-to-install-r-on-debian-10/

# Install the packages necessary to add a new repository over HTTPS
RUN apt -y update && \
    apt -y install dirmngr --install-recommends && \
    apt -y install apt-transport-https &&  \
    apt -y install ca-certificates && \
    apt -y install software-properties-common && \
    apt -y install gnupg2

# Run the following commands to enable the CRAN repository and add the CRAN GPG key to your system
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8F25A8A73EACF41 && \
    add-apt-repository "deb https://cloud.r-project.org/bin/linux/debian buster-cran40/"

# Update the packages list and install the R package
RUN apt -y update && \
    apt -y upgrade && \
    apt -y install r-base

# Install Git, then clone Quadron repo
RUN apt -y update && \
    apt -y install git && \
    git clone https://github.com/aleksahak/Quadron

# Start R in Quadron/lib folder, install package 'caret', then run 'source("bitcompile.R")'
RUN cd Quadron/lib && Rscript -e "install.packages('caret')" && Rscript -e "source('bitcompile.R')" && cd - 

# Copy scripts folder, then run quadrun_setup.R
ADD scripts /scripts
RUN cd /scripts && Rscript quadron_setup.R && cd -

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

