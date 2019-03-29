# SOFWERX RF Classifier
A tool for intercepting, classifying, and exploiting RF signals

  The goal of this project is to create a functional hardware prototype that could actively detect local radio signals and classify them - either by checking them against a database or using machine learning to determine metadata about the signal. This has been successful with the machine learning run on networked devices - however, the further specification is to accomplish all tasks locally, on a portable device. More specifically, we have been attempting to accomplish the above mentioned tasks on a NVIDIA Jetson TX2.

  Thus far, we have successfully designed and automated a TX2 environment that can auto-detect incoming radio signals and also created a base framework for a database that can be queried for recognized signals. After generating the classification model from Deepsig, we can begin to test real-time classification on the TX2. Looking forward, the next step would be linking and automating the separate functions we have created, from detection, to classification (and transfer learning), to database storage.

### Dataset
Generated dataset can be found at [Deepsig](https://www.deepsig.io/datasets)

### Dependencies
The RF scanning environment and scripts rely on:
*GNURadio
*[RTLSDR Scanner](https://eartoearoak.com/software/rtlsdr-scanner)

The SDR we used for testing was an RTL-SDR

### Scanning
With repo and dependencies installed, run 
```./scanner.sh [start] [end]```

where start and end indicate the ends of the range you would like to scan on, in MHz

### DB/DB Scraping
The initial foundations for a database have been sourced from [SigID Wiki](https://www.sigidwiki.com/wiki/Signal_Identification_Guide)

The python script for scraping the database, as well as the database itself can be found in db/

### Classification
The classifier source files can be found in classifier/

To build the Docker container, run the build_dockerfile script with the desired architecture. This will copy the Dockerfile from the relevent directory into classifier/, and build the container:

```./build_dockerfile amd```

Note: The ARM Dockerfile is currently broken, and will not build successfully
