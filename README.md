# Benchmark and Simulation Data for XQAOA

This repository contains the $D$-regular graphs and their optimal cut solutions, which were used to benchmark classical and quantum algorithms in the paper *An Expressive Ansatz for Low-Depth Quantum Optimization*. You will also find the simulation data and scripts used to produce the plots in this repository. We aim to make this repository valuable for those who wish to benchmark their quantum algorithms on the MaxCut problem.

##  Benchmark Data

In the [benchmark_data](benchmark_data) folder, you'll find $400$ $D$-regular graphs with $128$ and $256$ vertices for $3 \leq D \leq 10$. These graphs are presented in a machine-readable CSV format and are named according to the convention `G{D}#{N}_{I}.csv`, where $D$ stands for the degree of the graph, $N$ represents the number of vertices, and $I$ represents the specific instance of the graph. For each combination of $D$ and $N$, there are $25$ unique instances.

#### File Structure

The file structure of each  `G{D}#{N}_{I}.csv` files are as follows:
- The first line contains four comma separted values. They are
	- $N$ - The number of vertices in the graph.
	- $M$ - The number of edges in the graph.
	- $C_{opt}$ - The cost of the optimal cut of the graph.
	- MIPGap - The gap between the lower and upper objective bound divided by the absolute value of the incumbent objective value. A MIPGap of $0.0$ indicates that the solution is optimal.
- The second line contains the assignments that gives the optimal cut  $C_{opt}$.
- The lines $3$ till $M+2$ contain the edges that generate the $D$-regular graph. The nodes are in the range $0, \dots, N-1$.

#### Usage
The following Python code allows to reads the `G{D}#{N}_{I}.csv` and returns the graph attributes along with the list of edges. The edge list can be used to construct the $D$-regular graph using libraries such as the [NetworkX](https://networkx.org/) library.
```python
import csv

def read_graph(D, N, I):
    edges = []
    with open(f"benchmark_data/G{D}#{N}_{I}.csv") as graph_file:
        graph_reader = csv.reader(graph_file, delimiter=',')
        for i, row in enumerate(graph_reader):
            if i == 0:
                _, M, C_opt, MIPGap = row
            elif i == 1:
                solution = row
            else:
                i, j = row
                edges.append((int(i), int(j)))
    solution = [int(x) for x in solution]
    graph_attr = {"Nodes": N, "Edges": int(M), "Cost": float(C_opt),
                  "MIPGap": float(MIPGap), "Solution": solution}
    return graph_attr, edges
```

## Simulation Data

The data collected in the numerical simulations are located in the [simulation_data](simulation_data) folder. They too are present in a machine-readable CSV format, however, these CSV files are also readable by the Python Pandas library (Pandas can read these CSV files as a DataFrame object.) The CSV file names follow the same convention as those in [benchmark_data](benchmark_data) folder,  `G{D}#{N}_{I}.csv`, where $D$ stands for the degree of the graph, $N$ represents the number of vertices, and $I$ represents the specific instance of the graph.

The CSV files present in the root of the [simulation_data](simulation_data) folder contain the numerical simulation results of benchmarking the $p = 1$ ansatz for the XQAOA (X=Y Mixer), MA-QAOA, QAOA, and QAOA* against the Classical-Relaxed and the state-of-the-art Goemans-Williamson algorithm for $100$ runs for all the graphs present in the [benchmark_data](benchmark_data) folder. The CSV files present in the following folders
- [simulation_data/XQAOA_No_Gamma](simulation_data/XQAOA_No_Gamma)
- [simulation_data/XY_QAOA](simulation_data/XY_QAOA)
- [simulation_data/Y_QAOA](simulation_data/Y_QAOA)

 contain the numerical data for the $p = 1$ ansatz for the XQAOA (X=Y Mixer with $\gamma = 0$), XQAOA (XY Mixer), and the XQAOA (Y Mixer) on the first $10$ instances of the `G3#128_{I}.csv` graphs.

The CSV files present in [simulation_data/FIG5_Dataset](simulation_data/FIG5_Dataset) contain the data to generate the plot in Figure 5 of the paper. Please note that these CSV files are not readable by the Pandas as a DataFrame object.

For usage of these simulation data, please refer the python scripts present in the [plot_scripts](plot_scripts) folder.

## Usage and Citation

Please consider citing this repository and our paper *An Expressive Ansatz for Low-Depth Quantum Optimization* if you find this repository useful and use it in your research for benchmarking purposes.
