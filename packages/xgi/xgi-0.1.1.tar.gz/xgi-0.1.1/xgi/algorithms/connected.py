import networkx as nx
import xgi
import scipy.sparse as sparse
import random

__all__ = [
    "is_connected",
    "connected_components",
    "number_connected_components",
    "node_connected_component",
    "is_connected_bfs",
]


def is_connected(H, s=1):
    """
    A function to determine whether a hypergraph is s-connected.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, default: 1
        Specifies the s-connected level

    Returns
    -------
    bool
        Specifies whether the hypergraph is s-connected.

    See Also
    --------
    connected_components
    number_connected_components

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print(xgi.is_connected(H))
    """
    data = sparse.find(xgi.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.is_connected(nx.Graph(zip(rows, cols)))


def connected_components(H, s=1):
    """
    A function to find the s-connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, default: 1
        Specifies the s-connected level

    Returns
    -------
    iterable of lists
        A list where each entry is an s-component of the hypergraph.

    See Also
    --------
    is_connected
    number_connected_components

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print([len(component) for component in xgi.connected_components(H)])
    """
    data = sparse.find(xgi.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.connected_components(nx.Graph(zip(rows, cols)))


def number_connected_components(H, s=1):
    """
    A function to find the number of s-connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, default: 1
        Specifies the s-connected level

    Returns
    -------
    int
        Returns the number of s-connected components of a hypergraph.

    See Also
    --------
    is_connected
    connected_components

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print(xgi.number_connected_components(H))
    """
    return len(connected_components(H, s=s))


def node_connected_component(H, n, s=1):
    """
    A function to find the s-connected component of which a node in the
    hypergraph is a part.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    n: hashable
        Node label
    s: int, default: 1
        Specifies the s-connected level

    See Also
    --------
    connected_components

    Returns
    -------
    list
        Returns the s-connected component of which the specified node in the
        hypergraph is a part.

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print(xgi.node_connected_component(H, 0))
    """
    data = sparse.find(xgi.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.node_connected_component(nx.Graph(zip(rows, cols)), n)


def is_connected_bfs(H):
    """
    A function to determine whether a hypergraph is connected.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

    Returns
    -------
    bool
        Specifies whether the hypergraph is s-connected.

    Notes
    -----
    This currently does not check for s-connectedness.

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print(xgi.is_connected(H))
    """
    return len(_plain_bfs(H, random.choice(list(H.nodes)))) == len(H)


def _plain_bfs(H, source):
    """A fast BFS node generator"""
    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                nextlevel.update(H.neighbors(v))
    return seen
