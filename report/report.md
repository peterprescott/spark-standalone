---
title: "Assignment 1: Big Data Analytics with Spark"
author: "Peter Prescott (201442927)"
---

# Introduction

Recent years have witnessed a *data revolution* characterised by unprecedented volume, variety and velocity [@RKitchin2014]. The challenge of handling such quantities of data has led to the development of a series of new technologies: the *MapReduce* paradigm for distributed data processing [@JDeanGhemawat2008], the *Hadoop* Distributed File System for storing and streaming such data [@KShvachkoEtAl2010], the *Spark* Resilient Distributed Dataset for in-memory cluster computing [@MZahariaEtAl2012], and the Spark SQL extension's optimized relational *Dataframe* API [@MArmbrustEtAl2015].

For this assignment [@BAmen2020], I am required to describe the middleware configuration of a Spark standalone cluster, to perform some simple analysis on a Spark Dataframe created from a CSV containing coronavirus data, and to present the results in a report of two A4 pages of 12-point text.

# Middleware Configuration

Configuring a Spark cluster requires setting up Spark master and worker nodes running the same versions of Spark and Hadoop, and a PySpark driver running the same version of Python as that which is used to call it. To simplify matters, and to make it easy to reproduce the configuration across different machines, I used Docker, which is rapidly becoming accepted as the standard solution for reproducible research and collaborative software development [@CBoettiger2015].

![](../files/figures/docker-hierarchy.png){#fig:docker}

Docker allows the different components of an application (in this case, our Spark cluster) to be run in isolated virtual *containers* launched from reproducible *images* defined explicitly by a 'Dockerfile' script. Based on the suggestion of @APerez2020, my configuration starts with a base image for the cluster, which adds a new installation of Python 3 to the pre-built publicly-available `openjdk:8-jre-slim` image, which offers a Java environment running on a Debian Linux kernel. On top of this, I defined a base Spark image for the master and worker images for the nodes of the Spark cluster; and separately an image for the PySpark driver, for which I set up the popular Jupyter notebook interface [@FPerezGranger2015]. The relationship of the images to each other is shown in Figure 1. For full details, see the Dockerfiles on the project's git repository: [github.com/pi-prescott/spark-standalone/tree/master/docker](https://github.com/pi-prescott/spark-standalone/tree/master/docker).

Once the images have been defined and built, the containers need to be run simultaneously with their network ports correctly mapped so that the different components of the configuration can interact successfully (Figure 2). These details are saved in a YAML configuration file, and then the cluster can be launched with a single command: `docker-compose up`. Finally, we need to connect to the Spark cluster by initiating a `SparkSession` from our Jupyter notebook. We can then confirm everything is configured correctly by checking the Spark Master UI at [localhost:8080]().

![](../files/figures/configuration.png){#fig:configuration}

# Data Analytic Design

The assignment specifies a series of simple analytic tasks to perform: the data flow is visualized in Figure 3. First we read a CSV containing coronavirus data into a Spark dataframe; then we check it has the correct schema. We can ask Spark to automatically infer the schema, and it succeeds in distinguishing integers from strings, but not (in this case) in recognizing that `Date` is a distinct type; so instead I specified the schema explicitly. We then use the `filter` function to remove null values, before using some other specific functions to find the highest `total_deaths` count in each country and the countries with highest and lowest `total_cases` counts.

![](../files/figures/data-flow.png)

# Results and Discussion

It was found that the United States has the highest number of `total_cases` with 8,779,653, while Montserrat has the lowest, with 13. Confusingly, the assignment suggests that the highest `total_deaths` for Sweden should be 986, but this is the answer one will obtain if the schema is not correctly specified -- the actual answer is 5,918. For the requested lists of twenty countries see the Jupyter notebook code and output in Appendix.

# Conclusions and Recommendations

This analysis was performed on a small CSV file of only 2.2 megabytes, which certainly does not qualify as *big data*. If we were to analyze a dataset of several terabytes then the single-machine standalone cluster we have configured would not be adequate. Instead we would need to actually leverage the capacity for utilizing a large cluster of distributed computing power that Spark is intended for -- say by renting cloud computing power on AWS. Because our configuration is precisely defined by Dockerfiles it should be straightforwardly transferable to such a scenario.

Our analysis has grouped the data by `location` to compare coronavirus numbers between countries, but without taking into account the differing sizes of these countries such comparisons are not very meaningful. It would also be interesting to consider the geospatial distribution of cases. Just as traditional database management systems have been extended with spatial database operations, similarly [Sedona](http://sedona.apache.org/) is a project currently incubating which extends Spark with *spatial* RDDs [@JYuEtAl2019].

# References
