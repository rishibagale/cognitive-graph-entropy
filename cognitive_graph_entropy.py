"""
Reference implementation of the Cognitive Graph Entropy framework.

Implements the three orthogonal observables and coarsening operator on the
active support V+ = {u in V : d(u) > 0} of a symmetric weighted graph G = (V, E, W):
  - Axis 1: Static Degree Salience / Conceptual Entropy H_c(G) and domain decomposition
  - Axis 2: Associative Transition Entropy Rate h_rate(G) = H(q) - H_c(G)
  - Axis 3: Global Spectral Entropy S(rho) via BGS rescaled Laplacian and diffusion heat kernel
  - Degree-preserving coarsening operator z = (u (+) v) with w'_zz = w_uu + w_vv + 2 w_uv
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Optional, Sequence

import numpy as np


@dataclass(frozen=True)
class GraphObservables:
    """Summary of all three cognitive graph entropy axes on active support V+."""

    m: int
    D: float
    H_c: float
    H_c_norm: float
    H_q: float
    h_rate: float
    S_bgs: Optional[float]
    S_heat: float


def _validate_weight_matrix(W: np.ndarray) -> np.ndarray:
    """Validate that W is a square, symmetric, non-negative 2D weight matrix."""
    arr = np.asarray(W, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("W must be a square 2D matrix.")
    if np.any(arr < 0.0):
        raise ValueError("Edge weights must be non-negative.")
    if not np.allclose(arr, arr.T, atol=1e-12):
        raise ValueError("W must be symmetric (w_uv == w_vu).")
    return 0.5 * (arr + arr.T)


def active_support(W: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Restrict W to active support V+ = {u in V : d(u) > 0}.

    Returns (W_active, active_indices).
    """
    arr = _validate_weight_matrix(W)
    degrees = arr.sum(axis=1)
    idx = np.flatnonzero(degrees > 0.0)
    if idx.size == 0:
        return np.zeros((0, 0), dtype=np.float64), idx
    return arr[np.ix_(idx, idx)], idx


def _shannon_entropy(probs: np.ndarray) -> float:
    """Shannon entropy in bits for a 1D non-negative probability vector."""
    p = probs[probs > 0.0]
    if p.size == 0:
        return 0.0
    return float(-np.sum(p * np.log2(p)))


def conceptual_entropy(W: np.ndarray) -> tuple[float, float]:
    """
    Compute Axis 1: Conceptual Entropy H_c(G) and active-support normalized H_c_hat.

    Returns (H_c, H_c_norm) in bits. H_c_norm is 0.0 when m <= 1.
    """
    W_act, _ = active_support(W)
    m = W_act.shape[0]
    if m == 0:
        return 0.0, 0.0
    d = W_act.sum(axis=1)
    D = float(d.sum())
    pi = d / D
    h_c = _shannon_entropy(pi)
    h_c_norm = h_c / math.log2(m) if m >= 2 else 0.0
    return h_c, h_c_norm


def joint_edge_entropy(W: np.ndarray) -> float:
    """Compute H(q) over directed stationary transition pairs q_uv = w_uv / D."""
    W_act, _ = active_support(W)
    if W_act.shape[0] == 0:
        return 0.0
    D = float(W_act.sum())
    q = (W_act / D).ravel()
    return _shannon_entropy(q)


def transition_entropy_rate(W: np.ndarray) -> float:
    """
    Compute Axis 2: Associative Transition Entropy Rate h_rate(G) = H(X_1 | X_0) in bits.
    """
    W_act, _ = active_support(W)
    m = W_act.shape[0]
    if m == 0:
        return 0.0
    d = W_act.sum(axis=1)
    D = float(d.sum())
    pi = d / D

    h_rate = 0.0
    for i in range(m):
        p_row = W_act[i] / d[i]
        h_rate += float(pi[i]) * _shannon_entropy(p_row)
    return h_rate


def domain_decomposition(
    W: np.ndarray,
    domains: Sequence[Sequence[int]],
) -> tuple[float, float, list[float], list[float]]:
    """
    Verify and compute the Domain-Decomposition Identity on active support:
      H_c(G) = H_between(D) + sum_d p_d * H_c(G | V_d)

    Args:
        W: Symmetric non-negative weight matrix.
        domains: Disjoint partition of all active node indices in V+.

    Returns:
        (H_between, weighted_within_sum, domain_shares, within_entropies)
    """
    arr = _validate_weight_matrix(W)
    degrees = arr.sum(axis=1)
    active_set = set(np.flatnonzero(degrees > 0.0).tolist())

    seen: set[int] = set()
    for block in domains:
        for u in block:
            if u not in active_set:
                raise ValueError(f"Node {u} is not in active support V+.")
            if u in seen:
                raise ValueError(f"Node {u} appears in multiple domains.")
            seen.add(u)
    if seen != active_set:
        raise ValueError("Domains must partition all active nodes V+.")

    D = float(degrees.sum())
    if D == 0.0:
        return 0.0, 0.0, [], []

    pi = degrees / D
    domain_shares: list[float] = []
    within_entropies: list[float] = []

    for block in domains:
        if not block:
            continue
        p_d = float(np.sum(pi[list(block)]))
        if p_d <= 0.0:
            continue
        local_pi = pi[list(block)] / p_d
        domain_shares.append(p_d)
        within_entropies.append(_shannon_entropy(local_pi))

    h_between = _shannon_entropy(np.asarray(domain_shares, dtype=np.float64))
    weighted_within = sum(p_d * h_d for p_d, h_d in zip(domain_shares, within_entropies))
    return h_between, weighted_within, domain_shares, within_entropies


def combinatorial_laplacian(W: np.ndarray) -> np.ndarray:
    """
    Construct the combinatorial graph Laplacian L = Deg_simple - W_simple on V+.
    Diagonal self-loops cancel out identically: L_uu = sum_{v != u} w_uv.
    """
    W_act, _ = active_support(W)
    if W_act.shape[0] == 0:
        return np.zeros((0, 0), dtype=np.float64)
    W_simple = W_act.copy()
    np.fill_diagonal(W_simple, 0.0)
    deg_simple = np.diag(W_simple.sum(axis=1))
    return deg_simple - W_simple


def spectral_entropy_bgs(W: np.ndarray) -> float:
    """
    Compute Axis 3 (BGS 2006): S(rho_BGS) in bits, where rho_BGS = L / Tr(L).
    Raises ValueError if Tr(L) == 0 (no off-diagonal edges).
    """
    L = combinatorial_laplacian(W)
    if L.shape[0] == 0:
        raise ValueError("Active support V+ is empty.")
    tr = float(np.trace(L))
    if tr <= 0.0:
        raise ValueError("Tr(L) == 0: BGS density matrix requires at least one off-diagonal edge.")
    evals = np.linalg.eigvalsh(L)
    evals = np.maximum(evals, 0.0)
    mu = evals / tr
    return _shannon_entropy(mu)


def spectral_entropy_heat(W: np.ndarray, beta: float = 1.0) -> float:
    """
    Compute Axis 3 (De Domenico & Biamonte 2016): S(rho_beta) in bits,
    where rho_beta = exp(-beta * L) / Tr(exp(-beta * L)).
    """
    if beta <= 0.0:
        raise ValueError("Diffusion scale beta must be positive.")
    L = combinatorial_laplacian(W)
    if L.shape[0] == 0:
        return 0.0
    evals = np.linalg.eigvalsh(L)
    evals = np.maximum(evals, 0.0)
    shifted = -beta * (evals - np.min(evals))
    weights = np.exp(shifted)
    mu = weights / float(np.sum(weights))
    return _shannon_entropy(mu)


def merge_nodes(W: np.ndarray, u: int, v: int) -> np.ndarray:
    """
    Degree-preserving coarsening operator z = (u (+) v) on distinct nodes u != v.

    Replaces nodes u and v with a single merged node placed at index min(u, v):
      - External edges: w'_zx = w'_xz = w_ux + w_vx
      - Self-loop accumulation: w'_zz = w_uu + w_vv + 2 * w_uv
    """
    arr = _validate_weight_matrix(W)
    n = arr.shape[0]
    if u == v or not (0 <= u < n) or not (0 <= v < n):
        raise ValueError("u and v must be distinct valid node indices.")

    keep, drop = (u, v) if u < v else (v, u)
    W_new = arr.copy()

    w_uu = arr[keep, keep]
    w_vv = arr[drop, drop]
    w_uv = arr[keep, drop]

    # Sum external weights into row/col `keep`
    ext_weights = arr[keep, :] + arr[drop, :]
    W_new[keep, :] = ext_weights
    W_new[:, keep] = ext_weights
    W_new[keep, keep] = w_uu + w_vv + 2.0 * w_uv

    # Remove `drop`
    mask = np.ones(n, dtype=bool)
    mask[drop] = False
    return W_new[np.ix_(mask, mask)]


def compute_all_observables(W: np.ndarray, beta: float = 1.0) -> GraphObservables:
    """Compute all three cognitive graph entropy axes for weight matrix W."""
    W_act, _ = active_support(W)
    m = W_act.shape[0]
    D = float(W_act.sum())
    if m == 0 or D == 0.0:
        return GraphObservables(
            m=0, D=0.0, H_c=0.0, H_c_norm=0.0, H_q=0.0, h_rate=0.0, S_bgs=None, S_heat=0.0
        )

    h_c, h_c_norm = conceptual_entropy(W_act)
    h_q = joint_edge_entropy(W_act)
    h_rate = transition_entropy_rate(W_act)
    s_heat = spectral_entropy_heat(W_act, beta=beta)
    try:
        s_bgs: Optional[float] = spectral_entropy_bgs(W_act)
    except ValueError:
        s_bgs = None

    return GraphObservables(
        m=m,
        D=D,
        H_c=h_c,
        H_c_norm=h_c_norm,
        H_q=h_q,
        h_rate=h_rate,
        S_bgs=s_bgs,
        S_heat=s_heat,
    )
