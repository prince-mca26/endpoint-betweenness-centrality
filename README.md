# Endpoint Betweenness Centrality

Implementation and evaluation of Endpoint Betweenness Centrality (EPBC) using Python and NetworkX.

## Authors

- Prince Verma
- Ayush Mann

## Project Overview

This project implements Endpoint Betweenness Centrality (EPBC) and evaluates it on selected network datasets.

The project includes:

- A manual implementation of Endpoint Betweenness Centrality
- Validation of the manual implementation against NetworkX
- Evaluation of EPBC on real-world network datasets
- Support for weighted and unweighted networks
- Support for directed and undirected networks

## Networks Evaluated

- **Karate Club** — undirected, unweighted
- **Dolphins** — undirected, unweighted
- **Football** — directed, weighted
- **PolBooks** — undirected, unweighted

The Network Repository datasets are stored in the `data/` directory in Matrix Market (`.mtx`) format.

## Project Structure

endpoint-betweenness-centrality/
│
├── README.md
├── endpoint_betweenness.py
├── requirements.txt
│
├── data/
│   ├── dolphins.mtx
│   ├── football.mtx
│   └── polbooks.mtx
│
└── .github/
    └── workflows/
        └── test.yml

## Implementation

The project contains two implementations:

### Manual EPBC

The manual implementation:

1. Generates source-target node pairs
2. Finds all shortest paths
3. Gives endpoint nodes a contribution of 1
4. Calculates intermediate-node contribution from the fraction of shortest paths containing the node
5. Normalizes the final score

### NetworkX

NetworkX is used for validation and efficient evaluation through:

    nx.betweenness_centrality(
        G,
        normalized=True,
        endpoints=True,
        weight=weight
    )

The manual implementation is compared against the NetworkX results to verify correctness.

## Requirements

- Python 3.12 or compatible Python 3 version
- NetworkX

Install the required dependency using:

    pip install -r requirements.txt

## Running the Project

From the repository root:

    python endpoint_betweenness.py

The program:

1. Tests the demonstration graph
2. Evaluates the Karate Club network
3. Loads and evaluates the Dolphins dataset
4. Loads and evaluates the Football dataset using edge weights
5. Loads and evaluates the PolBooks dataset

The program displays the network information and the top 5 nodes according to EPBC.

## Automated Testing

GitHub Actions is configured to automatically run the project whenever changes are pushed to the repository.

The workflow:

- Sets up Python
- Installs the required dependencies
- Runs `endpoint_betweenness.py`

A successful workflow run confirms that the project executes correctly in the GitHub environment.

## Technologies

- Python
- NetworkX
- GitHub Actions

## References

- NetworkX Betweenness Centrality documentation
- Network Repository datasets
- Course presentation on Endpoint Betweenness Centrality
