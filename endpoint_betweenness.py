"""
Endpoint Betweenness Centrality (EPBC)
--------------------------------------

Manual implementation, NetworkX validation, and evaluation
on selected real-world network datasets.

Authors: Prince Verma & Ayush Mann
Course: Network Science
University: University of Delhi
"""

import itertools
from pathlib import Path

import networkx as nx


# ============================================================
# 1. MANUAL EPBC IMPLEMENTATION
# ============================================================

def endpoint_betweenness_centrality(
    G,
    node,
    normalized=True,
    weight=None
):
    """
    Calculate Endpoint Betweenness Centrality (EPBC)
    for one node.

    For every reachable source-target pair:
    - source and target receive a contribution of 1
    - an intermediate node receives its fraction of
      shortest paths containing that node

    Undirected graphs use unordered node pairs.
    Directed graphs use ordered node pairs.
    """

    score = 0.0

    # Generate source-target pairs
    if G.is_directed():
        node_pairs = itertools.permutations(G.nodes(), 2)
    else:
        node_pairs = itertools.combinations(G.nodes(), 2)

    for source, target in node_pairs:

        # Ignore unreachable pairs
        if not nx.has_path(G, source, target):
            continue

        # Find all shortest paths
        shortest_paths = list(
            nx.all_shortest_paths(
                G,
                source,
                target,
                weight=weight
            )
        )

        # Endpoint contribution
        if node == source or node == target:
            score += 1.0

        # Intermediate-node contribution
        else:
            paths_containing_node = sum(
                node in path
                for path in shortest_paths
            )

            score += (
                paths_containing_node /
                len(shortest_paths)
            )

    # Normalize the score
    if normalized:
        n = len(G)

        if G.is_directed():
            score /= n * (n - 1)
        else:
            score /= n * (n - 1) / 2

    return score


# ============================================================
# 2. NETWORKX IMPLEMENTATION
# ============================================================

def endpoint_betweenness_centrality_builtin(
    G,
    weight=None
):
    """
    Calculate endpoint-aware betweenness centrality
    using NetworkX.

    endpoints=True includes source and target nodes
    in the betweenness calculation.
    """

    return nx.betweenness_centrality(
        G,
        normalized=True,
        endpoints=True,
        weight=weight
    )


# ============================================================
# 3. MANUAL IMPLEMENTATION VALIDATION
# ============================================================

def validate_implementation(
    G,
    weight=None,
    tolerance=1e-9
):
    """
    Compare the manual EPBC implementation with
    NetworkX for every node.

    Returns True if all scores agree within tolerance.
    """

    builtin_scores = endpoint_betweenness_centrality_builtin(
        G,
        weight=weight
    )

    all_match = True

    print("\nValidation Results")
    print("-" * 75)

    for node in G.nodes():

        manual_score = endpoint_betweenness_centrality(
            G,
            node,
            normalized=True,
            weight=weight
        )

        builtin_score = builtin_scores[node]

        difference = abs(
            manual_score - builtin_score
        )

        matches = difference <= tolerance

        if not matches:
            all_match = False

        print(
            f"Node {node}: "
            f"Manual = {manual_score:.6f}, "
            f"NetworkX = {builtin_score:.6f}, "
            f"Difference = {difference:.2e}, "
            f"{'MATCH' if matches else 'MISMATCH'}"
        )

    print("-" * 75)

    if all_match:
        print(
            "Validation successful: "
            "all manual and NetworkX scores match."
        )
    else:
        print(
            "Validation failed: "
            "at least one score differs."
        )

    return all_match


# ============================================================
# 4. TOP-N RESULTS
# ============================================================

def top_nodes(scores, k=5):
    """Return the top-k nodes according to EPBC score."""

    return sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:k]


def print_top_nodes(G, weight=None, k=5):
    """Calculate and display the top-k EPBC nodes."""

    scores = endpoint_betweenness_centrality_builtin(
        G,
        weight=weight
    )

    print(f"\nTop {k} EPBC Nodes")
    print("-" * 35)

    for rank, (node, score) in enumerate(
        top_nodes(scores, k),
        start=1
    ):
        print(
            f"{rank}. Node {node}: {score:.6f}"
        )

    return scores


# ============================================================
# 5. GRAPH INFORMATION
# ============================================================

def print_graph_information(name, G):
    """Display basic information about a network."""

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print(f"Nodes : {G.number_of_nodes()}")
    print(f"Edges : {G.number_of_edges()}")

    graph_type = (
        "Directed"
        if G.is_directed()
        else "Undirected"
    )

    weight_type = (
        "Weighted"
        if nx.is_weighted(G)
        else "Unweighted"
    )

    print(f"Type  : {graph_type} / {weight_type}")


# ============================================================
# 6. DEMONSTRATION GRAPH
# ============================================================

def create_demo_graph():
    """
    Create the small graph used to demonstrate
    and validate EPBC.

        A ----- B
        |       |
        D ----- C
        |
        E
    """

    G = nx.Graph()

    G.add_edges_from([
        ("A", "B"),
        ("B", "C"),
        ("A", "D"),
        ("C", "D"),
        ("D", "E")
    ])

    return G


# ============================================================
# 7. MATRIX MARKET DATASET LOADER
# ============================================================

def load_mtx_graph(file_path):
    """
    Load a Network Repository Matrix Market (.mtx) graph.

    Matrix Market header determines:

    - symmetric -> undirected graph
    - general   -> directed graph
    - pattern   -> unweighted graph
    - integer/real -> weighted graph

    Network Repository datasets use 1-based node IDs,
    which are preserved here.
    """

    with open(file_path, "r") as file:

        # Read Matrix Market header
        header = file.readline().strip()

        if not header.startswith("%%MatrixMarket"):
            raise ValueError(
                f"{file_path} is not a valid "
                "Matrix Market file."
            )

        header_parts = header.split()

        value_type = header_parts[3].lower()
        symmetry = header_parts[4].lower()

        # Skip comment lines
        line = file.readline()

        while line.startswith("%"):
            line = file.readline()

        # Matrix dimensions:
        # rows, columns, number of entries
        rows, columns, entries = map(
            int,
            line.split()[:3]
        )

        # Symmetric matrix = undirected graph
        if symmetry == "symmetric":
            G = nx.Graph()
        else:
            G = nx.DiGraph()

        # Matrix Market uses 1-based node numbering
        G.add_nodes_from(
            range(1, rows + 1)
        )

        # Pattern matrices are unweighted
        weighted = value_type != "pattern"

        for _ in range(entries):

            line = file.readline().strip()

            if not line:
                continue

            parts = line.split()

            source = int(parts[0])
            target = int(parts[1])

            if weighted:

                value = float(parts[2])

                G.add_edge(
                    source,
                    target,
                    weight=value
                )

            else:

                G.add_edge(
                    source,
                    target
                )

        return G


# ============================================================
# 8. NETWORK EVALUATION
# ============================================================

def evaluate_network(
    name,
    G,
    weight=None,
    validate=False
):
    """
    Evaluate a network using NetworkX EPBC.

    If validate=True, the manual implementation is
    independently compared with NetworkX.
    """

    print_graph_information(
        name,
        G
    )

    if validate:

        validate_implementation(
            G,
            weight=weight
        )

    return print_top_nodes(
        G,
        weight=weight,
        k=5
    )


# ============================================================
# 9. MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("ENDPOINT BETWEENNESS CENTRALITY")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Demonstration graph
    # --------------------------------------------------------

    print("\n[1] Demonstration Graph")

    demo_graph = create_demo_graph()

    evaluate_network(
        "Demonstration Graph",
        demo_graph,
        weight=None,
        validate=True
    )

    # --------------------------------------------------------
    # 2. Karate Club
    # --------------------------------------------------------

    print("\n[2] Karate Club Network")

    karate = nx.karate_club_graph()

    evaluate_network(
        "Karate Club",
        karate,
        weight=None,
        validate=True
    )

    # --------------------------------------------------------
    # 3. Network Repository datasets
    #
    # Required files:
    #
    # data/dolphins.mtx
    # data/football.mtx
    # data/polbooks.mtx
    # --------------------------------------------------------

    data_dir = Path("data")

    # --------------------------------------------------------
    # Dolphins
    # --------------------------------------------------------

    print("\n[3] Dolphins Network")

    dolphins_file = (
        data_dir / "dolphins.mtx"
    )

    if dolphins_file.exists():

        dolphins = load_mtx_graph(
            dolphins_file
        )

        evaluate_network(
            "Dolphins",
            dolphins,
            weight=None,
            validate=False
        )

    else:

        print(
            "\nDolphins dataset not found. "
            "Place dolphins.mtx inside data/."
        )

    # --------------------------------------------------------
    # Football
    # --------------------------------------------------------

    print("\n[4] Football Network")

    football_file = (
        data_dir / "football.mtx"
    )

    if football_file.exists():

        football = load_mtx_graph(
            football_file
        )

        evaluate_network(
            "Football",
            football,
            weight="weight",
            validate=False
        )

    else:

        print(
            "\nFootball dataset not found. "
            "Place football.mtx inside data/."
        )

    # --------------------------------------------------------
    # PolBooks
    # --------------------------------------------------------

    print("\n[5] PolBooks Network")

    polbooks_file = (
        data_dir / "polbooks.mtx"
    )

    if polbooks_file.exists():

        polbooks = load_mtx_graph(
            polbooks_file
        )

        evaluate_network(
            "PolBooks",
            polbooks,
            weight=None,
            validate=False
        )

    else:

        print(
            "\nPolBooks dataset not found. "
            "Place polbooks.mtx inside data/."
        )


if __name__ == "__main__":
    main()
