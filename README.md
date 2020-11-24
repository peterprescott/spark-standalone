# Big Data Analysis using Spark

This is my project file for Assignment 1 of [COMP529](https://intranet.csc.liv.ac.uk/teaching/modules/module.php?code=COMP529), which  requires the configuration of a Spark standalone cluster, and then the implementation of some specified data analysis on a table of coronavirus data (see [task description](./files/A1.pdf)).

The cluster configuration is done using Docker, so setting it up on your own machine should be as simple as this:
```
git clone https://github.com/pi-prescott/spark-standalone
cd spark-standalone
docker-compose up
```

![](./files/figures/configuration.png)
