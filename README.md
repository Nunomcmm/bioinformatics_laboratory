# Bioinformatics Laboratory

## "Analyzing the differences between the most used programs for phylogenetic trees creation"

In this project we compare the existing differences between the results of each the phylogenetic tree program, RAxML, MEGA and IQ-TREE.  
For this we will compare the accuracy between each bootstrap values and the time each program takes to create the trees.  
It was used replicate bootstrap value of 100 in trees creation.  
Only compares Maximum-Likelihood Trees.  
At the end we can be checked which program was more accurate.  

## Methodology

1. Use a correct fasta file as input
2. Validate the file
3. Create table of contents
4. Standardize the name
5. Tree creation:
   * RAxML
   * IQ-TREE 
   * MEGA
6. Concatenate all trees
7. Compare using Shimodaira-Hasegawa method

## Requirements

* Docker installation
  
## Getting started

Pull docker image:  
`docker pull nunomcmm/docker_lb:latest`

Run docker image with volumes:  
`docker run -v $HOME/Desktop/Snakerun/inputs/:/project/inputs -v $HOME/Desktop/Snakerun/outputs/:/project/outputs -i -t nunomcmm/docker_lb:latest`

**Note**: In this docker run, `$HOME/Desktop/Snakerun/inputs` is the path to the directory or file that you want to use.  
`/project/inputs` is the path where the directory or file is mounted in the container.  
In this case, the generated outputs will be placed in `/Snakerun/outputs` directory.  

Execute Snakemake using all cores, where "OUTPUTS" is the outputs directory name and "INPUT" is FASTA input file:  
`OUTPUTDIR="OUTPUTS" INPUT="INPUT" snakemake --cores all`

Example:  
`OUTPUTDIR="outputs" INPUT="inputs/RAG_small.fasta" snakemake --cores all`

In case you don't want to get inside the docker, you can use the following command:  
`docker run -v $HOME/Desktop/Snakerun/inputs/:/project/inputs -v $HOME/Desktop/Snakerun/outputs/:/project/outputs -e OUTPUTDIR="outputs" -e INPUT="inputs/RAG_small_t.fasta" -i -t nunomcmm/docker_lb:latest snakemake --cores all`
