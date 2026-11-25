# 00 — Claims Registry

Every claim in the paper/framework carries exactly one status. No claim enters prose without a row here.

- `[PROVEN]` — derived/theorem; must be reproducible from memory in < 1 week (see [03_math_derivations.md](03_math_derivations.md))
- `[CITED]` — established in literature, with citation
- `[HYP]` — hypothesis; falsification condition stated
- `[DESIGN]` — open design decision; must be resolved per claim before submission
- `[OVERCLAIM]` — currently stated beyond evidence; reword before submission

---

## Set 1 — Cognitive Graph Entropy & Three-Axis Observables

| ID | Claim | Status | Falsification / notes |
|----|-------|--------|-----------------------|
| C-1.1 | Shannon entropy $H(p) = -\sum_i p_i \log_2 p_i$ is the unique uncertainty measure satisfying continuity (A1), monotonicity on uniform choices with $h(2)=1$ (A2), and grouping/recursivity (A3). | `[PROVEN]` | [03 §6](03_math_derivations.md#section-6-rigorous-shannon-uniqueness) (integer squeeze on $2^{k_m} \le n^m \le 2^{k_m+1}$, rational grouping, density of $\mathbb{Q}^n_{>0} \cap \Delta_n$ in $\Delta_n$) |
| C-1.2 | For symmetric association weights $w_{uv} = w_{vu} \ge 0$, $\pi(u) = d(u)/D$ is a reversible stationary distribution on active support $V^+ = \{u \in V : d(u) > 0\}$ ($D > 0$), unique iff the induced subgraph on $V^+$ is connected (irreducible). | `[PROVEN]` | [03 §1–2](03_math_derivations.md#section-2-the-random-walk-detailed-balance-and-disconnected-silos); if $V^+$ has $k > 1$ disconnected silos, any convex combination of component-wise stationary distributions is stationary |
| C-1.3 | Under the degree-preserving coarsening operator $z = (u \oplus v)$ on distinct $u, v \in V^+$ ($w'_{zx} = w_{ux} + w_{vx}$, $w'_{zz} = w_{uu} + w_{vv} + 2w_{uv}$), Axis 1 ($H_c$) strictly decreases by $(a+b)h_2\left(\frac{a}{a+b}\right) > 0$, whereas Axis 2 ($h_{\text{rate}}$) is **non-monotonic** (e.g., $a-b-c$ raises $h_{\text{rate}}$ from $0.500$ to $0.689\text{ bits}$). | `[PROVEN]` | [03 §5](03_math_derivations.md#section-5-merging-and-graph-coarsening); consequence: cross-ontology comparisons of $H_c$ are invalid without controlling $m = |V^+|$ and ontology version |
| C-1.4 | Conceptual entropy $H_c$ (together with domain decomposition $H_{\text{between}} + \sum_d p_d H_c(G \mid V_d)$ and structural companions $h_{\text{rate}}, S(\rho)$) tracks breadth/diversity of a user's knowledge graph. | `[HYP]` | Fixed ontology; cohort with external breadth probes; ordering of observables must track probe ordering in the stated direction |
| C-1.5 | The entropy construction is novel mathematics. | `[OVERCLAIM]` | $H_c(G)$ is a member of the studied graph-entropy family (Körner 1973; Dehmer & Mowshowitz 2011), and $S(\rho)$ uses BGS (2006) and De Domenico & Biamonte (2016). Reword: novelty = cognitive operationalization (associative walk from language/session graphs + multi-axis regime separation) + empirical claim, not the entropy formulas |
| C-1.6 | Three-axis observable assignment: Axis 1 ($H_c$) measures static degree salience & domain breadth; Axis 2 ($h_{\text{rate}} = H(q) - H_c$) measures step-to-step transition unpredictability; Axis 3 ($S(\rho)$ via $\rho_{\text{BGS}}$ or $\rho_\beta$) measures global Laplacian topology & disconnected silos ($\lim_{\beta\to\infty} S(\rho_\beta) = \log_2 k$). | `[PROVEN]` / `[CITED]` | [03 §7](03_math_derivations.md#section-7-three-observables-of-the-cognitive-graph); resolves Session 1 open design decision. Note: `yentellect/backend/graph.py` also tracks normalized Fiedler gap $\lambda_2(L_{\text{sym}})$ for bridge recommendation; directed graphs require dropping symmetry ($\pi \ne d/D$) |
| C-1.7 | $H_c(G)$, $h_{\text{rate}}(G)$, and $\rho_{\text{BGS}}$ are invariant under positive linear rescaling of all edge weights ($w'_{uv} = c \cdot w_{uv}$, $c > 0$). | `[PROVEN]` | [03 §3](03_math_derivations.md#section-3-scale-invariance); note: heat kernel $\rho_\beta = e^{-\beta L}/\operatorname{Tr}(e^{-\beta L})$ rescales diffusion time $\beta \mapsto c\beta$ under $w \mapsto c w$ |

### Open Questions

1. **Operational edge-weight definition:** Co-occurrence / embedding similarity / interaction frequency must be fixed for all sessions before any empirical cohort data is collected.
2. **Directed associative extensions:** Capturing asymmetric implication ($A \implies B$) requires extending the walk to directed weights where detailed balance fails and $\pi$ is solved via Perron–Frobenius rather than $\pi_u = d(u)/D$.
