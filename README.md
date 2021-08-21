# Network Strengthening
Program in Python which will reinforce a train network, based on a study of graph algorithm.

## Context
This project was to be carried out for the subject **Algorithmique des Graphes** within the framework of my studies in order to validate my Computer Science License. 

## How to Use
```
$python3 ameliorations.py [-h] [--metro [METRO ...]] [--rer [RER ...]]
                        [--liste-stations] [--articulations] [--ponts]
                        [--ameliorer-articulations] [--ameliorer-ponts]
```
optional arguments:
```
  -h, --help            show this help message and exit
  --metro [METRO ...]   load line of metro
  --rer [RER ...]       load line of rer
  --liste-stations      displays the list of network stations with their
                        identifier sorted in order alphabetical
  -articulations        displays the articulation points of the network that
                        has been loaded
  --ponts               displays the bridges of the network that has been
                        loaded
  --ameliorer-articulations
                        displays the articulation points of the network that
                        has been loaded,as well as the edges to be added so
                        that these stations are no longer points of
                        articulation
  --ameliorer-ponts     displays the bridges of the network that has been
                        loaded, as well as the edges to addso that these edges
                        are no longer bridges.
```         
                        

