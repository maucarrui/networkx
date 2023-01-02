import random
import time

from collections import Counter

import networkx as nx
from networkx.algorithms.isomorphism.tree_isomorphism import (
    assign_structure,
    categorize_entries,
    categorize_lists,
    get_centers_of_tree,
    get_initial_values,
    get_levels,
    get_multisets_list_of_level,
    rooted_tree_isomorphism,
    rooted_tree_isomorphism_n,
    sort_lists_of_naturals,
    sort_natural_multisets,
    tree_isomorphism,
    tree_isomorphism_n,
    update_values,
)
from networkx.classes.function import is_directed

# Tests the function categorize_entries. The returned function should behave
# like a function NONEMPTY : N -> P(N) such that NONEMPTY(i) are the numbers in
# the i-th position of some list in S; this numbers are sorted
def test_categorize_entries():
    # An arbitrary list of lists of natural numbers.
    S = [
        [0, 0, 1, 2, 3],
        [1, 2, 3],
        [0, 1, 1, 4],
        [3, 3, 4],
        [4],
        [4, 4, 5],
    ]

    # Expected NONEMPTY function.
    expected_NONEMPTY = {
        0: [0, 1, 3, 4],
        1: [0, 1, 2, 3, 4],
        2: [1, 3, 4, 5],
        3: [2, 4],
        4: [3],
    }

    # Obtained NONEMPTY function.
    obtained_NONEMPTY = categorize_entries(S)

    assert expected_NONEMPTY == obtained_NONEMPTY


# Tests the function categorize_lists. The returned function should behave like
# a function LENGTH such that LENGTH(i) are the lists of S with length i.
def test_categorize_lists():
    # An arbitrary list of lists of natural numbers.
    S = [
        [0, 0, 1, 2, 3],
        [1, 2, 3],
        [0, 1, 1, 4],
        [3, 3, 4],
        [4],
        [4, 4, 5],
    ]

    # Expected LENGTH function.
    expected_LENGTH = {
        1: [[4]],
        3: [[1, 2, 3], [3, 3, 4], [4, 4, 5]],
        4: [[0, 1, 1, 4]],
        5: [[0, 0, 1, 2, 3]],
    }

    # Obtained LENGTH function.
    obtained_LENGTH = categorize_lists(S)

    assert expected_LENGTH == obtained_LENGTH


# Tests the function sort_lists_of_naturals. The expected sorted list should
# have a lexicographical ordering.
def test_sort_list_of_naturals():
    # An arbitrary list of lists of natural numbers.
    S = [
        [0, 0, 1, 2, 3],
        [1, 2, 3],
        [0, 1, 1, 4],
        [3, 3, 4],
        [4],
        [4, 4, 5],
    ]

    expected_ordering = [
        [0, 0, 1, 2, 3],
        [0, 1, 1, 4],
        [1, 2, 3],
        [3, 3, 4],
        [4],
        [4, 4, 5],
    ]

    obtained_ordering = sort_lists_of_naturals(S)

    assert expected_ordering == obtained_ordering

    # Test for another list of lists of natural numbers.
    S = [
        [1, 2, 3, 7, 8],
        [2, 2, 3, 4],
        [2, 2, 4, 3],
        [0, 1],
        [0, 0],
        [1, 3, 4],
        [2, 3, 4],
        [7],
        [8, 8],
    ]

    expected_ordering = [
        [0, 0],
        [0, 1],
        [1, 2, 3, 7, 8],
        [1, 3, 4],
        [2, 2, 3, 4],
        [2, 2, 4, 3],
        [2, 3, 4],
        [7],
        [8, 8],
    ]

    obtained_ordering = sort_lists_of_naturals(S)

    assert expected_ordering == obtained_ordering


# Test the get_levels function. The returned function should behave like a
# function M: N -> P(V) such that, for each i in {0,...,h}, M(i) is the set of
# vertices that are found in the i-th level of T.
def test_isomorphism_trees_get_levels():
    # Test for an arbitrary graph.
    edges_t1 = [
        ("v0", "v1"),
        ("v0", "v2"),
        ("v0", "v3"),
        ("v1", "v4"),
        ("v1", "v5"),
        ("v3", "v6"),
    ]
    T1 = nx.Graph(edges_t1)

    # Expected level function.
    expected_levels = {
        2: {"v0"},
        1: {"v1", "v2", "v3"},
        0: {"v4", "v5", "v6"},
    }

    # Obtained level function.
    obtained_levels = get_levels(T1, "v0", 2)

    assert expected_levels == obtained_levels

    # Test for another arbitrary graph.
    edges_t2 = [
        ("u3", "u4"),
        ("u3", "u2"),
        ("u4", "u5"),
        ("u4", "u6"),
        ("u4", "u7"),
        ("u2", "u1"),
        ("u7", "u8"),
        ("u1", "u0"),
    ]
    T2 = nx.Graph(edges_t2)

    # Expected level function.
    expected_levels = {
        3: {"u3"},
        2: {"u2", "u4"},
        1: {"u5", "u6", "u7", "u1"},
        0: {"u8", "u0"},
    }

    obtained_levels = get_levels(T2, "u3", 3)

    assert expected_levels == obtained_levels


# Test the get_initial_values function. The returned function should behave like
# a function M: N -> P(V) such that, such that, for every vertex v in the tree
# T, if v is a leave then v's initial value is 0, otherwise its defined as -1.
def test_isomorphism_trees_set_initial_values():
    # Test for an arbitrary graph.
    edges_t1 = [
        ("v0", "v1"),
        ("v0", "v2"),
        ("v0", "v3"),
        ("v1", "v4"),
        ("v1", "v5"),
        ("v3", "v6"),
    ]
    T1 = nx.Graph(edges_t1)

    # Expected level function.
    expected_values = {
        "v0": -1,
        "v1": -1,
        "v2": 0,
        "v3": -1,
        "v4": 0,
        "v5": 0,
        "v6": 0,
    }

    # Obtained level function.
    obtained_values = get_initial_values(T1, "v0")

    assert expected_values == obtained_values

    # Test for another arbitrary graph.
    edges_t2 = [
        ("u3", "u4"),
        ("u3", "u2"),
        ("u4", "u5"),
        ("u4", "u6"),
        ("u4", "u7"),
        ("u2", "u1"),
        ("u7", "u8"),
        ("u1", "u0"),
    ]
    T2 = nx.Graph(edges_t2)

    # Expected level function.
    expected_levels = {
        "u3": -1,
        "u4": -1,
        "u2": -1,
        "u5": 0,
        "u6": 0,
        "u7": -1,
        "u1": -1,
        "u8": 0,
        "u0": 0,
    }

    obtained_levels = get_initial_values(T2, "u3")

    assert expected_values == obtained_values


# Tests the function assign_values. The returned function should assign to all
# the vertices found on the i-th level a structure.
def test_assign_values():
    # Test for an specific scenario.
    levels = {
        2: {"v0"},
        1: {"v1", "v2", "v3"},
        0: {"v4", "v5", "v6"},
    }

    values = {
        "v0": 1,
        "v1": 2,
        "v2": 0,
        "v3": 1,
        "v4": 0,
        "v5": 0,
        "v6": 0,
    }

    parenthood = {
        "v1": "v0",
        "v2": "v0",
        "v3": "v0",
        "v4": "v1",
        "v5": "v1",
        "v6": "v3",
    }

    expected_structure_lvl_2 = {
        "v0": Counter([0, 1, 2]),
    }

    expected_structure_lvl_1 = {
        "v1": Counter([0, 0]),
        "v3": Counter([0]),
    }

    obtained_structure_lvl_1, leaves_lvl_1 = assign_structure(
        parenthood, levels, values, 1
    )

    obtained_structure_lvl_2, leaves_lvl_2 = assign_structure(
        parenthood, levels, values, 2
    )

    assert leaves_lvl_1 == {"v2"}
    assert leaves_lvl_2 == set()

    assert obtained_structure_lvl_1 == expected_structure_lvl_1
    assert obtained_structure_lvl_2 == expected_structure_lvl_2


# Tests the function get_multisets_list_of_level. The returned list should
# correspond to the structures of the vertices found on the i-th level, and the
# map should correspond to a mapping of structures to the vertices that have
# said structure.
def test_get_multisets_list_of_level():
    # Test for an specific scenario.
    levels = {
        2: {"v0"},
        1: {"v1", "v2", "v3", "v7"},
        0: {"v4", "v5", "v6", "v8"},
    }

    values = {
        "v0": 1,
        "v1": 2,
        "v2": 0,
        "v3": 1,
        "v7": 1,
        "v4": 0,
        "v5": 0,
        "v6": 0,
        "v8": 0,
    }

    parenthood = {
        "v1": "v0",
        "v2": "v0",
        "v3": "v0",
        "v7": "v0",
        "v4": "v1",
        "v5": "v1",
        "v6": "v3",
        "v8": "v7",
    }

    structures_lvl_2 = {
        "v0": Counter([0, 1, 2]),
    }

    structures_lvl_1 = {
        "v1": Counter([0, 0]),
        "v3": Counter([0]),
        "v7": Counter([0]),
    }

    expected_list_lvl_2 = [(0, 1, 2)]
    expected_list_lvl_1 = [(0, 0), (0,), (0,)]

    expected_mapping_lvl_2 = {
        (0, 1, 2): {"v0"},
    }

    expected_mapping_lvl_1 = {
        (0, 0): {"v1"},
        (0,): {"v3", "v7"},
    }

    obt_list_lvl_1, obt_mapping_lvl_1 = get_multisets_list_of_level(
        levels, values, structures_lvl_1, 1
    )
    obt_list_lvl_2, obt_mapping_lvl_2 = get_multisets_list_of_level(
        levels, values, structures_lvl_2, 2
    )

    assert len(structures_lvl_1) == len(obt_list_lvl_1)
    for struct in expected_list_lvl_1:
        assert struct in obt_list_lvl_1

    assert len(structures_lvl_2) == len(obt_list_lvl_2)
    for struct in expected_list_lvl_2:
        assert struct in obt_list_lvl_2

    assert obt_mapping_lvl_1 == expected_mapping_lvl_1
    assert obt_mapping_lvl_2 == expected_mapping_lvl_2


def test_update_values():
    # Test for an specific scenario.
    # Starting values.
    values = {
        "v0": -1,
        "v1": -1,
        "v2": 0,
        "v3": -1,
        "v7": -1,
        "v4": 0,
        "v5": 0,
        "v6": 0,
        "v8": 0,
    }

    mapping_lvl_1 = {
        (0, 0): {"v1"},
        (0,): {"v3", "v7"},
    }

    structures_list_lvl_1 = ((0,), (0,), (0, 0))

    expected_values_after_lvl_1 = {
        "v0": -1,
        "v1": 2,
        "v2": 0,
        "v3": 1,
        "v7": 1,
        "v4": 0,
        "v5": 0,
        "v6": 0,
        "v8": 0,
    }

    # Dummy functions.
    parenthood = {}
    children = {}
    leaves = set()

    update_values(
        structures_list_lvl_1, mapping_lvl_1, values, children, parenthood, leaves
    )

    assert expected_values_after_lvl_1 == values

    structures_list_lvl_2 = [
        (0, 1, 2),
    ]

    mapping_lvl_2 = {
        (0, 1, 2): {"v0"},
    }

    expected_values_after_lvl_2 = {
        "v0": 1,
        "v1": 2,
        "v2": 0,
        "v3": 1,
        "v7": 1,
        "v4": 0,
        "v5": 0,
        "v6": 0,
        "v8": 0,
    }

    update_values(
        structures_list_lvl_2, mapping_lvl_2, values, children, parenthood, leaves
    )

    assert expected_values_after_lvl_2 == values


# Auxiliary function to determine if an isomorphism is valid.  Let f be an
# isomorphism, then u and v are adjacent if and only if f(u) and f(v) are
# adjacent.
def is_valid_isomorphism(T1, T2, isomorphism):
    # Test that for all (u, v) in E_T1 then (f(u), f(v)) in E_T2.
    for (u, v) in T1.edges():
        if not T2.has_edge(isomorphism[u], isomorphism[v]):
            return False

    # Define the inverse mapping of the isomorphism.
    inverse_iso = {}

    for v in isomorphism:
        inverse_iso[isomorphism[v]] = v

    # Test that for all (u, v) in E_T2 then (f^-1(u), f^-1(v)) in E_T1.
    for (u, v) in T2.edges():
        if not T1.has_edge(inverse_iso[u], inverse_iso[v]):
            return False

    # If both conditions are satisfied, return true.
    return True


# Tests the function rooted_tree_isomorphism_n.
def test_rooted_tree_isomorphism_n_hardcoded():
    # The following trees are isomorph.
    edges_t1 = [
        ("v0", "v1"),
        ("v0", "v2"),
        ("v0", "v3"),
        ("v1", "v4"),
        ("v1", "v5"),
        ("v3", "v6"),
        ("v4", "v7"),
        ("v4", "v8"),
        ("v4", "v9"),
        ("v6", "v10"),
        ("v6", "v11"),
        ("v9", "v12"),
    ]
    T1 = nx.Graph(edges_t1)

    edged_t2 = [
        ("w0", "w1"),
        ("w0", "w2"),
        ("w0", "w3"),
        ("w2", "w4"),
        ("w4", "w5"),
        ("w4", "w6"),
        ("w3", "w7"),
        ("w3", "w8"),
        ("w8", "w9"),
        ("w8", "w10"),
        ("w8", "w11"),
        ("w10", "w12"),
    ]

    T2 = nx.Graph(edged_t2)

    are_iso, iso = rooted_tree_isomorphism_n(T1, "v0", T2, "w0")

    assert are_iso
    assert is_valid_isomorphism(T1, T2, iso)


# Tests the function get_centers_of_tree.
def test_get_centers_of_tree():
    # Hardcoded trees.
    edges_t1 = [
        ("v0", "v1"),
        ("v1", "v3"),
        ("v3", "v2"),
        ("v3", "v4"),
        ("v3", "v5"),
        ("v5", "v6"),
        ("v6", "v7"),
        ("v7", "v8"),
    ]
    T1 = nx.Graph(edges_t1)

    centers_t1 = get_centers_of_tree(T1)
    assert centers_t1 == {"v5"}

    edges_t2 = [
        ("u0", "u1"),
        ("u1", "u2"),
        ("u2", "u3"),
        ("u3", "u4"),
        ("u4", "u5"),
        ("u4", "u6"),
        ("u4", "u7"),
        ("u7", "u8"),
    ]
    T2 = nx.Graph(edges_t2)

    centers_t2 = get_centers_of_tree(T2)
    assert centers_t2 == {"u3"}

    edges_t3 = [("w0", "w1"), ("w1", "w2"), ("w2", "w3"), ("w3", "w4"), ("w4", "w5")]
    T3 = nx.Graph(edges_t3)

    centers_t3 = get_centers_of_tree(T3)
    assert centers_t3 == {"w2", "w3"}


# Tests the function tree_isomorphism_n.
def test_tree_isomorphism_n_hardcoded():
    # Hardcoded trees.
    edges_t1 = [
        ("v0", "v1"),
        ("v1", "v3"),
        ("v3", "v2"),
        ("v3", "v4"),
        ("v3", "v5"),
        ("v5", "v6"),
        ("v6", "v7"),
        ("v7", "v8"),
    ]
    T1 = nx.Graph(edges_t1)

    edges_t2 = [
        ("u0", "u1"),
        ("u1", "u2"),
        ("u2", "u3"),
        ("u3", "u4"),
        ("u4", "u5"),
        ("u4", "u6"),
        ("u4", "u7"),
        ("u7", "u8"),
    ]
    T2 = nx.Graph(edges_t2)

    is_iso, isomorphism = tree_isomorphism_n(T1, T2)
    assert is_iso
    assert is_valid_isomorphism(T1, T2, isomorphism)

    # Previous hardcoded test
    edges_1 = [
        ("a", "b"),
        ("a", "c"),
        ("a", "d"),
        ("b", "e"),
        ("b", "f"),
        ("e", "j"),
        ("e", "k"),
        ("c", "g"),
        ("c", "h"),
        ("g", "m"),
        ("d", "i"),
        ("f", "l"),
    ]
    T1 = nx.Graph(edges_1)

    edges_2 = [
        ("v", "y"),
        ("v", "z"),
        ("u", "x"),
        ("q", "u"),
        ("q", "v"),
        ("p", "t"),
        ("n", "p"),
        ("n", "q"),
        ("n", "o"),
        ("o", "r"),
        ("o", "s"),
        ("s", "w"),
    ]
    T2 = nx.Graph(edges_2)

    # Possible isomorphisms.
    isomorphism1 = {
        "a": "n",
        "b": "q",
        "c": "o",
        "d": "p",
        "e": "v",
        "f": "u",
        "g": "s",
        "h": "r",
        "i": "t",
        "j": "y",
        "k": "z",
        "l": "x",
        "m": "w",
    }

    # could swap y and z
    isomorphism2 = {
        "a": "n",
        "b": "q",
        "c": "o",
        "d": "p",
        "e": "v",
        "f": "u",
        "g": "s",
        "h": "r",
        "i": "t",
        "j": "z",
        "k": "y",
        "l": "x",
        "m": "w",
    }

    is_iso, isomorphism = tree_isomorphism_n(T1, T2)

    assert is_iso
    assert (isomorphism == isomorphism1) or (isomorphism == isomorphism2)
    assert is_valid_isomorphism(T1, T2, isomorphism)


# Tests the function tree_isomorphism_n with some trivial graphs.
def test_tree_isomorphism_n_trivials():
    # Test the trivial case of empty trees, i.e. no nodes.
    T1 = nx.Graph()
    T2 = nx.Graph()

    is_iso, isomorphism = tree_isomorphism_n(T1, T2)
    assert is_iso
    assert isomorphism == {}

    # Test the trivial case of a single node in each tree.
    T1 = nx.Graph()
    T1.add_node("a")

    T2 = nx.Graph()
    T2.add_node("n")

    is_iso, isomorphism = tree_isomorphism_n(T1, T2)

    assert is_iso
    assert isomorphism == {"a": "n"}
    assert is_valid_isomorphism(T1, T2, isomorphism)

    # Test another trivial case where the two graphs have different numbers of
    # nodes.

    edges_1 = [("a", "b"), ("a", "c")]

    edges_2 = [("v", "y")]

    T1 = nx.Graph(edges_1)
    T2 = nx.Graph(edges_2)

    is_iso, isomorphism = tree_isomorphism_n(T1, T2)

    assert not is_iso
    assert isomorphism == {}

    # Test another trivial case where the two graphs have the same different
    # numbers of nodes but differ in structure.
    edges_1 = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e")]
    edges_2 = [("a", "b"), ("b", "c"), ("b", "d"), ("c", "e")]

    T1 = nx.Graph(edges_1)
    T2 = nx.Graph(edges_2)

    is_iso, isomorphism = tree_isomorphism_n(T1, T2)

    assert not is_iso
    assert isomorphism == {}


# Given a tree T1, create a new tree T2 that is isomorphic to T1.
def generate_isomorphism(T1):

    assert nx.is_tree(T1)

    # Get a random permutation of the nodes of T1.
    nodes1 = list(T1)
    nodes2 = nodes1.copy()
    random.shuffle(nodes2)

    # this is one isomorphism, however they may be multiple
    # so we don't necessarily get this one back
    someisomorphism = [(u, v) for (u, v) in zip(nodes1, nodes2)]

    # map from old to new
    map1to2 = {u: v for (u, v) in someisomorphism}

    # get the edges with the transformed names
    edges2 = [random_swap((map1to2[u], map1to2[v])) for (u, v) in T1.edges()]
    # randomly permute, to ensure we're not relying on edge order somehow
    random.shuffle(edges2)

    # so t2 is isomorphic to t1
    T2 = nx.Graph(edges2)

    return T2


# The function nonisomorphic_trees generates all the non-isomorphic trees of a
# given order. Take each tree, make a "copy" of it, and its copy should be
# isomorphic to the original; verify that the function tree_isomorphism_n
# returns True and a proper isomorphism. For k=4 the test takes around 2.83
# seconds, and for k=15 it takes around 7.57 seconds.
def test_tree_isomorphism_n_positive(maxk=13):
    print("\nPositive test with new function\n")

    for k in range(2, maxk + 1):
        start_time = time.time()
        trial = 0
        for T1 in nx.nonisomorphic_trees(k):
            T2 = generate_isomorphism(T1)

            is_iso, isomorphism = tree_isomorphism_n(T1, T2)

            assert is_iso
            assert is_valid_isomorphism(T1, T2, isomorphism)

            trial += 1

        print(k, trial, time.time() - start_time)


# The function nonisomorphic_trees generates all the non-isomorphic trees of a
# given order. Take each pair of trees verify that the function
# tree_isomorphism_n returns False and an empty isomorphism.
def test_tree_isomorphism_n_negative(maxk=11):
    print("\nNegative test with new function\n")

    for k in range(4, maxk + 1):
        test_trees = list(nx.nonisomorphic_trees(k))
        start_time = time.time()
        trial = 0
        for i in range(len(test_trees) - 1):
            T1 = test_trees[i]
            for j in range(i + 1, len(test_trees)):
                trial += 1

                T2 = test_trees[j]
                is_iso, isomorphism = tree_isomorphism_n(T1, T2)

                assert not is_iso

        print(k, trial, time.time() - start_time)


# have this work for graph
# given two trees (either the directed or undirected)
# transform t2 according to the isomorphism
# and confirm it is identical to t1
# randomize the order of the edges when constructing
def check_isomorphism(t1, t2, isomorphism):

    # get the name of t1, given the name in t2
    mapping = {v2: v1 for (v1, v2) in isomorphism}

    # these should be the same
    d1 = is_directed(t1)
    d2 = is_directed(t2)
    assert d1 == d2

    edges_1 = []
    for (u, v) in t1.edges():
        if d1:
            edges_1.append((u, v))
        else:
            # if not directed, then need to
            # put the edge in a consistent direction
            if u < v:
                edges_1.append((u, v))
            else:
                edges_1.append((v, u))

    edges_2 = []
    for (u, v) in t2.edges():
        # translate to names for t1
        u = mapping[u]
        v = mapping[v]
        if d2:
            edges_2.append((u, v))
        else:
            if u < v:
                edges_2.append((u, v))
            else:
                edges_2.append((v, u))

    return sorted(edges_1) == sorted(edges_2)


def test_hardcoded():

    print("hardcoded test")

    # define a test problem
    edges_1 = [
        ("a", "b"),
        ("a", "c"),
        ("a", "d"),
        ("b", "e"),
        ("b", "f"),
        ("e", "j"),
        ("e", "k"),
        ("c", "g"),
        ("c", "h"),
        ("g", "m"),
        ("d", "i"),
        ("f", "l"),
    ]

    edges_2 = [
        ("v", "y"),
        ("v", "z"),
        ("u", "x"),
        ("q", "u"),
        ("q", "v"),
        ("p", "t"),
        ("n", "p"),
        ("n", "q"),
        ("n", "o"),
        ("o", "r"),
        ("o", "s"),
        ("s", "w"),
    ]

    # there are two possible correct isomorphisms
    # it currently returns isomorphism1
    # but the second is also correct
    isomorphism1 = [
        ("a", "n"),
        ("b", "q"),
        ("c", "o"),
        ("d", "p"),
        ("e", "v"),
        ("f", "u"),
        ("g", "s"),
        ("h", "r"),
        ("i", "t"),
        ("j", "y"),
        ("k", "z"),
        ("l", "x"),
        ("m", "w"),
    ]

    # could swap y and z
    isomorphism2 = [
        ("a", "n"),
        ("b", "q"),
        ("c", "o"),
        ("d", "p"),
        ("e", "v"),
        ("f", "u"),
        ("g", "s"),
        ("h", "r"),
        ("i", "t"),
        ("j", "z"),
        ("k", "y"),
        ("l", "x"),
        ("m", "w"),
    ]

    t1 = nx.Graph()
    t1.add_edges_from(edges_1)
    root1 = "a"

    t2 = nx.Graph()
    t2.add_edges_from(edges_2)
    root2 = "n"

    isomorphism = sorted(rooted_tree_isomorphism(t1, root1, t2, root2))

    # is correct by hand
    assert (isomorphism == isomorphism1) or (isomorphism == isomorphism2)

    # check algorithmically
    assert check_isomorphism(t1, t2, isomorphism)

    # try again as digraph
    t1 = nx.DiGraph()
    t1.add_edges_from(edges_1)
    root1 = "a"

    t2 = nx.DiGraph()
    t2.add_edges_from(edges_2)
    root2 = "n"

    isomorphism = sorted(rooted_tree_isomorphism(t1, root1, t2, root2))

    # is correct by hand
    assert (isomorphism == isomorphism1) or (isomorphism == isomorphism2)

    # check algorithmically
    assert check_isomorphism(t1, t2, isomorphism)


# randomly swap a tuple (a,b)
def random_swap(t):
    (a, b) = t
    if random.randint(0, 1) == 1:
        return (a, b)
    else:
        return (b, a)


# given a tree t1, create a new tree t2
# that is isomorphic to t1, with a known isomorphism
# and test that our algorithm found the right one
def positive_single_tree(t1):

    assert nx.is_tree(t1)

    nodes1 = [n for n in t1.nodes()]
    # get a random permutation of this
    nodes2 = nodes1.copy()
    random.shuffle(nodes2)

    # this is one isomorphism, however they may be multiple
    # so we don't necessarily get this one back
    someisomorphism = [(u, v) for (u, v) in zip(nodes1, nodes2)]

    # map from old to new
    map1to2 = {u: v for (u, v) in someisomorphism}

    # get the edges with the transformed names
    edges2 = [random_swap((map1to2[u], map1to2[v])) for (u, v) in t1.edges()]
    # randomly permute, to ensure we're not relying on edge order somehow
    random.shuffle(edges2)

    # so t2 is isomorphic to t1
    t2 = nx.Graph()
    t2.add_edges_from(edges2)

    # lets call our code to see if t1 and t2 are isomorphic
    isomorphism = tree_isomorphism(t1, t2)

    # make sure we got a correct solution
    # although not necessarily someisomorphism
    assert len(isomorphism) > 0
    assert check_isomorphism(t1, t2, isomorphism)


# run positive_single_tree over all the
# non-isomorphic trees for k from 4 to maxk
# k = 4 is the first level that has more than 1 non-isomorphic tree
# k = 13 takes about 2.86 seconds to run on my laptop
# larger values run slow down significantly
# as the number of trees grows rapidly
def test_positive(maxk=13):

    print("positive test")

    for k in range(2, maxk + 1):
        start_time = time.time()
        trial = 0
        for t in nx.nonisomorphic_trees(k):
            positive_single_tree(t)
            trial += 1
        print(k, trial, time.time() - start_time)


# test the trivial case of a single node in each tree
# note that nonisomorphic_trees doesn't work for k = 1
def test_trivial():

    print("trivial test")

    # back to an undirected graph
    t1 = nx.Graph()
    t1.add_node("a")
    root1 = "a"

    t2 = nx.Graph()
    t2.add_node("n")
    root2 = "n"

    isomorphism = rooted_tree_isomorphism(t1, root1, t2, root2)

    assert isomorphism == [("a", "n")]

    assert check_isomorphism(t1, t2, isomorphism)


# test another trivial case where the two graphs have
# different numbers of nodes
def test_trivial_2():

    print("trivial test 2")

    edges_1 = [("a", "b"), ("a", "c")]

    edges_2 = [("v", "y")]

    t1 = nx.Graph()
    t1.add_edges_from(edges_1)

    t2 = nx.Graph()
    t2.add_edges_from(edges_2)

    isomorphism = tree_isomorphism(t1, t2)

    # they cannot be isomorphic,
    # since they have different numbers of nodes
    assert isomorphism == []


# the function nonisomorphic_trees generates all the non-isomorphic
# trees of a given size.  Take each pair of these and verify that
# they are not isomorphic
# k = 4 is the first level that has more than 1 non-isomorphic tree
# k = 11 takes about 4.76 seconds to run on my laptop
# larger values run slow down significantly
# as the number of trees grows rapidly
def test_negative(maxk=11):

    print("negative test")

    for k in range(4, maxk + 1):
        test_trees = list(nx.nonisomorphic_trees(k))
        start_time = time.time()
        trial = 0
        for i in range(len(test_trees) - 1):
            for j in range(i + 1, len(test_trees)):
                trial += 1
                assert tree_isomorphism(test_trees[i], test_trees[j]) == []
        print(k, trial, time.time() - start_time)
