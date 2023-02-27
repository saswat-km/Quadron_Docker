# Quadron

Quadron [1] is a Gradient Boosting Machines (GBM) model, trained on G4-seq data, to predict G4 formation propensity of 
a sequence. Quadron is written in R programming language. The source code is available at https://github.com/aleksahak/Quadron. 

Running Quadron requires installation of a specific version of R, specific versions of several R packages as depenecies, downloading
Quadron source code from the Github repository, installing xgboost library, and bit compiling the Quadron package -- These steps 
take a lot of time. In this project, we Dockerize Quadron to avoid repeating all these configuration steps everytime a user wants 
to run Quadron. A text file called Dockerfile is used to specify all the configuration steps. A Docker engine creates a Docker 
image from the Dockerfile. Docker engine runs containers created off of the docker image. Container technologies such as Docker 
also offer other benefits such as portability, performance, agility, isolation, and scalability [2].

In order to run the Dockerized version of Quadron, you need to have the Docker engine installed on your box. Please refer to 
instructions at https://docs.docker.com/engine/install/. You also need the Quadron Docker image. You can either get the Quadron 
Docker image from Docker Hub, or you can build the image locally. If you are getting the image from the Docker Hub (preferred), 
you can skip the instructions for building/pushing the image, and go to the instructions for running Quadron Docker container.

# Getting the Quadron Docker Image

To pull the Quadron Docker image from the Docker Hub repository:
> docker pull kxk302/quadron:1.0.0

To view the pulled image:
> docker images -f "reference=kxk302/quadron:1.0.0"

# Building/Pushing the Quadron Docker Image

All the commands are run in the same directory, say, /Users/kxk302/workspace/

Clone Quadron_Docker repository (This creates a folder called Quadron_Docker):
> git clone https://github.com/kxk302/Quadron_Docker.git

Change your directory to Quadron_Docker folder:
> cd ./Quadron_Docker

To create a Docker image:
> docker build --progress=plain -t kxk302/quadron:1.0.0 .

To view the created image:
> docker images -f "reference=kxk302/quadron:1.0.0"

To push the created image to your Docker Hub repository (You need to be regsitered at https://hub.docker.com/):
> docker login\
> docker push kxk302/quadron:1.0.0

# Running the Quadron Docker Container

Suppose you want to run Quadron on a .fasta file located at '/Users/kxk302/workspace/Quadron_Docker/input/test.fasta' folder.
The input file name is 'test.fasta', the input file folder is '/Users/kxk302/workspace/Quadron_Docker/input/', and absolute path
to input file name is '/Users/kxk302/workspace/Quadron_Docker/input/test.fasta'.  

Suppose you want Quadron to save the output file at '/Users/kxk302/workspace/Quadron_Docker/output/test_out.txt'. The output file 
name is 'test_out.txt', the output file folder is '/Users/kxk302/workspace/Quadron_Docker/output/', and absolute path
to output file name is '/Users/kxk302/workspace/Quadron_Docker/output/test_out.txt'.

Suppose you want Quadron to use 8 CPUs. 

On Unix/Mac OS, to run the containerized version of Quadron, run the following command:
> ./scripts/run_quadron.sh <InputFileAbsolutePath> <OutputFileAbsolutePath> <NumberOfCPUs>

For example:

> ./scripts/run_quadron.sh  /Users/kxk302/workspace/Quadron_Docker/input/test.fasta /Users/kxk302/workspace/Quadron_Docker/output/test_out.txt 8

On Windows, to run the containerized version of Quadron, run the following command:

> docker run -v InputFileAbsolutePath:/InputFileName -v OutputFileFolder:/output kxk302/quadron:1.0.0 /InputFileName /output/OutputFileName NumberOfCPUs

Below is an actual invocation of Dockerzed Quadron:
> docker run -v /Users/kxk302/workspace/Quadron_Docker/input/test.fasta:/test.fasta -v /Users/kxk302/workspace/Quadron_Docker/output:/output kxk302/quadron:1.0.0 /test.fasta /output/test_out.txt 8

The -v flag simply mounts a folder on your host machine to the container, to make your local files accessible to the container.

# References

1. Sahakyan, A.B., Chambers, V.S., Marsico, G. et al. Machine learning model for sequence-driven DNA G-quadruplex formation. Sci Rep 7, 14535 (2017). https://doi.org/10.1038/s41598-017-14017-4

2. https://www.microfocus.com/documentation/visual-cobol/vc60/EclUNIX/GUID-F5BDACC7-6F0E-4EBB-9F62-E0046D8CCF1B.html
