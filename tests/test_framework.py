"""Verification tests for all theorems, bounds, and worked examples."""

import math
import unittest

import numpy as np

from cognitive_graph_entropy import (
    compute_all_observables,
    conceptual_entropy,
    domain_decomposition,
    joint_edge_entropy,
    merge_nodes,
    spectral_entropy_bgs,
    spectral_entropy_heat,
    transition_entropy_rate,
)


def _complete_graph(n: int) -> np.ndarray:
    W = np.ones((n, n), dtype=np.float64)
    np.fill_diagonal(W, 0.0)
    return W


def _cycle_graph(n: int) -> np.ndarray:
    W = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        j = (i + 1) % n
        W[i, j] = W[j, i] = 1.0
    return W


def _star_graph(n_leaves: int) -> np.ndarray:
    n = n_leaves + 1
    W = np.zeros((n, n), dtype=np.float64)
    for i in range(1, n):
        W[0, i] = W[i, 0] = 1.0
    return W


def _binary_entropy(p: float) -> float:
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


class TestCognitiveGraphEntropy(unittest.TestCase):
    def test_path_merge_counterexample_0689(self) -> None:
        # Unweighted path a - b - c (indices 0, 1, 2)
        W = np.array(
            [
                [0.0, 1.0, 0.0],
                [1.0, 0.0, 1.0],
                [0.0, 1.0, 0.0],
            ]
        )
        obs_before = compute_all_observables(W)
        self.assertEqual(obs_before.m, 3)
        self.assertAlmostEqual(obs_before.D, 4.0)
        self.assertAlmostEqual(obs_before.H_c, 1.5, places=10)
        self.assertAlmostEqual(obs_before.H_q, 2.0, places=10)
        self.assertAlmostEqual(obs_before.h_rate, 0.5, places=10)

        # Merge z = b (+) c (indices 1 and 2)
        W_merged = merge_nodes(W, 1, 2)
        expected_W_merged = np.array([[0.0, 1.0], [1.0, 2.0]])
        np.testing.assert_allclose(W_merged, expected_W_merged)

        obs_after = compute_all_observables(W_merged)
        self.assertEqual(obs_after.m, 2)
        self.assertAlmostEqual(obs_after.D, 4.0)
        self.assertAlmostEqual(obs_after.H_c, 0.8112781244591328, places=10)
        self.assertAlmostEqual(obs_after.H_q, 1.5, places=10)
        self.assertAlmostEqual(obs_after.h_rate, 0.6887218755408672, places=10)
        self.assertAlmostEqual(obs_after.H_q - obs_after.H_c, obs_after.h_rate, places=12)

        # Exact granularity lemma drop: (a + b) * h2(a / (a + b))
        a, b = 0.5, 0.25
        expected_drop = (a + b) * _binary_entropy(a / (a + b))
        self.assertAlmostEqual(obs_before.H_c - obs_after.H_c, expected_drop, places=12)
        # Non-monotonicity of h_rate
        self.assertGreater(obs_after.h_rate, obs_before.h_rate)

    def test_c6_vs_k6_orthogonality(self) -> None:
        obs_c6 = compute_all_observables(_cycle_graph(6))
        obs_k6 = compute_all_observables(_complete_graph(6))
        self.assertAlmostEqual(obs_c6.H_c, math.log2(6), places=10)
        self.assertAlmostEqual(obs_k6.H_c, math.log2(6), places=10)
        self.assertAlmostEqual(obs_c6.h_rate, 1.0, places=10)
        self.assertAlmostEqual(obs_k6.h_rate, math.log2(5), places=10)

    def test_spectral_reversal_k5_vs_star_s5(self) -> None:
        K5 = _complete_graph(5)
        S5 = _star_graph(4)

        self.assertAlmostEqual(spectral_entropy_bgs(K5), 2.0, places=6)
        self.assertAlmostEqual(spectral_entropy_bgs(S5), 1.5487949406953985, places=6)
        self.assertGreater(spectral_entropy_bgs(K5), spectral_entropy_bgs(S5))

        s_heat_k5 = spectral_entropy_heat(K5, beta=1.0)
        s_heat_s5 = spectral_entropy_heat(S5, beta=1.0)
        self.assertAlmostEqual(s_heat_k5, 0.22768189116758038, places=6)
        self.assertAlmostEqual(s_heat_s5, 1.8550000468489477, places=6)
        self.assertLess(s_heat_k5, s_heat_s5)

    def test_siloed_domains_and_self_loop_invariance(self) -> None:
        # Three disconnected K2 components => k = 3 silos => log2(3) as beta -> inf
        W = np.zeros((6, 6), dtype=np.float64)
        for start in (0, 2, 4):
            W[start, start + 1] = W[start + 1, start] = 1.0

        s_large_beta = spectral_entropy_heat(W, beta=50.0)
        self.assertAlmostEqual(s_large_beta, math.log2(3), places=10)

        # Adding arbitrary self-loops leaves BGS and heat spectral entropies unchanged
        W_loops = W + np.diag([2.0, 0.5, 4.0, 0.0, 1.0, 3.0])
        self.assertAlmostEqual(spectral_entropy_bgs(W), spectral_entropy_bgs(W_loops), places=10)
        self.assertAlmostEqual(
            spectral_entropy_heat(W, beta=1.0),
            spectral_entropy_heat(W_loops, beta=1.0),
            places=10,
        )

    def test_pure_self_loop_bgs_vs_heat(self) -> None:
        W_loops_only = np.diag([1.0, 3.0, 2.0])
        with self.assertRaises(ValueError):
            spectral_entropy_bgs(W_loops_only)
        self.assertAlmostEqual(spectral_entropy_heat(W_loops_only, beta=1.0), math.log2(3), places=10)

    def test_ghost_node_and_scale_invariance(self) -> None:
        W = _star_graph(4)
        # Embed in a 10-node graph with 5 isolated ghost nodes
        W_ghosts = np.zeros((10, 10), dtype=np.float64)
        W_ghosts[:5, :5] = W

        obs_orig = compute_all_observables(W)
        obs_ghost = compute_all_observables(W_ghosts)
        self.assertEqual(obs_ghost.m, obs_orig.m)
        self.assertAlmostEqual(obs_ghost.H_c, obs_orig.H_c, places=12)
        self.assertAlmostEqual(obs_ghost.H_c_norm, obs_orig.H_c_norm, places=12)
        self.assertAlmostEqual(obs_ghost.h_rate, obs_orig.h_rate, places=12)

        # Positive rescaling w -> c * w leaves H_c, h_rate, and S_bgs invariant
        W_scaled = 0.37 * W
        obs_scaled = compute_all_observables(W_scaled)
        self.assertAlmostEqual(obs_scaled.H_c, obs_orig.H_c, places=12)
        self.assertAlmostEqual(obs_scaled.h_rate, obs_orig.h_rate, places=12)
        self.assertAlmostEqual(obs_scaled.S_bgs, obs_orig.S_bgs, places=12)

    def test_star_formula_and_loop_free_lower_bound(self) -> None:
        for n_leaves in (1, 4, 15):
            S = _star_graph(n_leaves)
            h_c, _ = conceptual_entropy(S)
            self.assertAlmostEqual(h_c, 1.0 + 0.5 * math.log2(n_leaves), places=10)
            self.assertGreaterEqual(h_c, 1.0 - 1e-12)

    def test_domain_decomposition_identity(self) -> None:
        # Two weighted clusters bridged by a weak link
        W = np.array(
            [
                [0.0, 2.0, 1.0, 0.2, 0.0],
                [2.0, 0.0, 3.0, 0.0, 0.0],
                [1.0, 3.0, 0.0, 0.0, 0.3],
                [0.2, 0.0, 0.0, 0.0, 4.0],
                [0.0, 0.0, 0.3, 4.0, 0.0],
            ]
        )
        h_c, _ = conceptual_entropy(W)
        h_between, weighted_within, _, _ = domain_decomposition(W, [[0, 1, 2], [3, 4]])
        self.assertAlmostEqual(h_c, h_between + weighted_within, places=12)


if __name__ == "__main__":
    unittest.main()
