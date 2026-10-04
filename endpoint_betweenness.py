"""
Endpoint Betweenness Centrality (EPBC)
--------------------------------------

Manual implementation, NetworkX validation, and evaluation
on selected real-world network datasets.

Authors: Ayush Mann & Prince Verma
Course: Network Science
University: University of Delhi
"""

import itertools
from pathlib import Path

import networkx as nx


def endpoint_betweenness_centrality(
    G,
    node,
    normalized=True,
    weight=None
):
    """
    Calculate Endpoint Betweenness Centrality (EPBC) for one node.

    For every reachable source-target pair:
    - source and target receive a contribution of 1
    - an intermediate node receives its fraction of shortest paths

    Undirected graphs use unordered pairs.
    Directed graphs use ordered pairs.

    Parameters
    ----------
    G : networkx.Graph
        Input graph.
    node : node
        Node whose EPBC is calculated.
    normalized : bool
        Whether to normalize the result.
    weight : str or None
        Edge attribute used as shortest-path weight.

    Returns
    -------
    float
        EPBC score of the node.
    """

    score = 0.0

    if G.is_directed():
        node_pairs = itertools.permutations(G.nodes(), 2)
    else:
        node_pairs = itertools.combinations(G.nodes(), 2)

    for source, target in node_pairs:

        if not nx.has_path(G, source, target):
            continue

        shortest_paths = list(
            nx.all_shortest_paths(
                G,
                source,
                target,
                weight=weight
            )
        )

        if node == source or node == target:
            score += 1.0
        else:
            paths_containing_node = sum(
                node in path
                for path in shortest_paths
            )

            score += (
                paths_containing_node /
                len(shortest_paths)
            )

    if normalized:
        n = len(G)

        if G.is_directed():
            score /= n * (n - 1)
        else:
            score /= n * (n - 1) / 2

    return score


def endpoint_betweenness_centrality_builtin(G, weight=None):
    """
    Calculate endpoint-aware betweenness centrality using NetworkX.

    NetworkX enables endpoint inclusion with endpoints=True.
    """

    return nx.betweenness_centrality(
        G,
        normalized=True,
        endpoints=True,
        weight=weight
    )


def validate_implementation(G, weight=None, tolerance=1e-9):
    """
    Compare the manual EPBC implementation with NetworkX.

    Returns True when all node scores agree within tolerance.
    """

    builtin_scores = endpoint_betweenness_centrality_builtin(
        G,
        weight=weight
    )

    all_match = True

    print("\nValidation Results")
    print("-" * 70)

    for node in G.nodes():

        manual_score = endpoint_betweenness_centrality(
            G,
            node,
            normalized=True,
            weight=weight
        )

        builtin_score = builtin_scores[node]

        difference = abs(manual_score - builtin_score)
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

    print("-" * 70)

    if all_match:
        print("Validation successful: all scores match.")
    else:
        print("Validation failed: at least one score differs.")

    return all_match


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
        print(f"{rank}. Node {node}: {score:.6f}")

    return scores


def print_graph_information(name, G):
    """Display basic information about a network."""

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print(f"Nodes : {G.number_of_nodes()}")
    print(f"Edges : {G.number_of_edges()}")

    graph_type = "Directed" if G.is_directed() else "Undirected"
    weight_type = "Weighted" if nx.is_weighted(G) else "Unweighted"

    print(f"Type  : {graph_type} / {weight_type}")


def create_demo_graph():
    """
    Create the small graph used to demonstrate and validate EPBC.

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


def load_gml_graph(file_path):
    """Load a graph stored in GML format."""

    return nx.read_gml(file_path)


def load_pajek_graph(file_path):
    """
    Load a graph stored in Pajek format and convert it to
    a simple Graph or DiGraph.
    """

    G = nx.read_pajek(file_path)

    if G.is_directed():
        return nx.DiGraph(G)

    return nx.Graph(G)


def evaluate_network(name, G, weight=None, validate=False):
    """
    Evaluate a network using NetworkX EPBC.

    Set validate=True when an independent comparison with
    the manual implementation is required.
    """

    print_graph_information(name, G)

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
        validate=False
    )

    # --------------------------------------------------------
    # 3. Network Repository datasets
    #
    # Place the following files inside data/:
    #
    # data/dolphins.gml
    # data/football.net
    # data/polbooks.gml
    # --------------------------------------------------------

    data_dir = Path("data")

    # Dolphins
    dolphins_file = data_dir / "dolphins.gml"

    if dolphins_file.exists():
        dolphins = load_gml_graph(dolphins_file)

        evaluate_network(
            "Dolphins",
            dolphins,
            weight=None,
            validate=False
        )
    else:
        print(
            "\nDolphins dataset not found. "
            "Place dolphins.gml inside data/."
        )

    # Football
    football_file = data_dir / "football.net"

    if football_file.exists():
        football = load_pajek_graph(football_file)

        evaluate_network(
            "Football",
            football,
            weight="weight",
            validate=False
        )
    else:
        print(
            "\nFootball dataset not found. "
            "Place football.net inside data/."
        )

    # PolBooks
    polbooks_file = data_dir / "polbooks.gml"

    if polbooks_file.exists():
        polbooks = load_gml_graph(polbooks_file)

        evaluate_network(
            "PolBooks",
            polbooks,
            weight=None,
            validate=False
        )
    else:
        print(
            "\nPolBooks dataset not found. "
            "Place polbooks.gml inside data/."
        )


if __name__ == "__main__":
    main()
