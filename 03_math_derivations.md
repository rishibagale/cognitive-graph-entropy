# 03 — Math Derivations

Working record of every equation in the cognitive graph entropy framework. Standard per entry: Statement · Assumptions · Full derivation (no skipped steps) · Properties · Caveats · Status · Reproduce checklist.

Status legend: `[PROVEN]` derived/theorem · `[CITED]` established in literature · `[HYP]` hypothesis with stated falsification · `[DESIGN]` open design decision.

---

## Section 1. The Graph Space and Active Support

For a finite, undirected, weighted graph $G = (V, E, W)$ with non-negative weights $w_{uv} \ge 0$ and symmetric adjacency $w_{uv} = w_{vu}$, the weighted degree of node $u$ is:

$$d(u) = \sum_{v \in V} w_{uv}$$

Under this convention, an off-diagonal edge $\{u,v\}$ ($u \ne v$) contributes $w_{uv}$ to $d(u)$ and $w_{vu}$ to $d(v)$ ($2w_{uv}$ to total network volume), while a diagonal entry $w_{uu}$ contributes $w_{uu}$ to $d(u)$ (equivalently $w_{uu} = 2 w_{\text{loop}}(u)$ under undirected stub-counting).

To prevent division by zero in transition probabilities and eliminate ghost-node dilution, walk operations are restricted to the **active support** (assuming at least one positive weight so $V^+ \ne \emptyset$ and $D > 0$):

$$V^+ = \{u \in V : d(u) > 0\}, \qquad m = |V^+| \ge 1$$

Since $w_{uv} \ge 0$, any inactive node $u \notin V^+$ has $w_{uv} = 0$ for all $v \in V$, so restricting sums to $V^+$ preserves all degrees: $d(v) = \sum_{u \in V^+} w_{uv}$. The total active volume is:

$$D = \sum_{u \in V^+} d(u) = \sum_{u,v \in V^+} w_{uv} > 0$$

---

## Section 2. The Random Walk, Detailed Balance, and Disconnected Silos

For a random walker on $V^+$, the one-step transition probability from $u$ to $v$ is:

$$P_{uv} = \frac{w_{uv}}{d(u)}$$

**Theorem (`[PROVEN]` — `C-1.2`):** The distribution $\pi(u) = \frac{d(u)}{D}$ is a reversible stationary distribution on $V^+$, satisfying detailed balance:

$$\pi(u) P_{uv} = \pi(v) P_{vu} = \frac{w_{uv}}{D} =: q_{uv}$$

It is unique if and only if the induced subgraph on $V^+$ is connected (irreducible).

**Proof:** For any $v \in V^+$, using $w_{uv} = 0$ for $u \notin V^+$ and symmetry $w_{uv} = w_{vu}$:

$$(\pi P)(v) = \sum_{u \in V^+} \pi(u) P_{uv} = \sum_{u \in V^+} \left(\frac{d(u)}{D}\right)\left(\frac{w_{uv}}{d(u)}\right) = \frac{1}{D}\sum_{u \in V^+} w_{uv} = \frac{d(v)}{D} = \pi(v)$$

Detailed balance holds identically because $\pi(u) P_{uv} = \frac{w_{uv}}{D} = \frac{w_{vu}}{D} = \pi(v) P_{vu}$. $\blacksquare$

**Note on Disconnected Graphs:** When $V^+$ consists of $k > 1$ disconnected components $C_1, \dots, C_k$ (siloed conceptual domains), $\pi(u) = d(u)/D$ remains a valid global stationary distribution weighted by component volume $D_r = \sum_{u \in C_r} d(u)$, though any convex combination of component-wise stationary distributions $\pi_r(u) = \frac{d(u)}{D_r}\mathbf{1}_{u \in C_r}$ is also stationary because a walker never crosses between silos.

---

## Section 3. Scale Invariance

**Proposition (`[PROVEN]` — `C-1.7`):** Conceptual Entropy $H_c(G)$ and transition entropy rate $h_{\text{rate}}(G)$ are invariant to positive linear scaling of edge weights ($w'_{uv} = c \cdot w_{uv}$ for $c > 0$).

**Proof:** Scaling every entry by $c > 0$ yields $d'(u) = c \cdot d(u)$ and $D' = c \cdot D$, so:

$$\pi'(u) = \frac{c \cdot d(u)}{c \cdot D} = \pi(u), \qquad P'_{uv} = \frac{c \cdot w_{uv}}{c \cdot d(u)} = P_{uv}$$

Hence $H_c(G') = H_c(G)$ and $h_{\text{rate}}(G') = h_{\text{rate}}(G)$. Consequently, uniform exponential weight decay across all edges leaves $H_c$ and $h_{\text{rate}}$ unchanged; both measure relative weight proportions rather than absolute magnitude. $\blacksquare$

*(Caveat for Axis 3: $\rho_{\text{BGS}} = L/\operatorname{Tr}(L)$ is also scale-invariant, whereas $\rho_\beta = e^{-\beta L}/\operatorname{Tr}(e^{-\beta L})$ maps $w \mapsto c w$ to an effective diffusion scale $\beta \mapsto c\beta$.)*

---

## Section 4. Bounds, Normalization, and Domain Decomposition

The **Conceptual Entropy** of $G$ is the Shannon entropy of its stationary degree distribution $\pi$:

$$H_c(G) = -\sum_{u \in V^+} \pi(u)\log_2 \pi(u)$$

### General & Loop-Free Bounds

Across all active graphs with $m = |V^+| \ge 1$ (allowing self-loops):

$$0 \le H_c(G) \le \log_2 m$$

- $H_c(G) = 0$ iff $m = 1$ (a single active node with a self-loop).
- $H_c(G) = \log_2 m$ iff $G$ is weighted-degree-regular on $V^+$ ($\pi_u = 1/m$).

If $G$ has **no self-loops** ($w_{uu} = 0$ for all $u \in V^+$), then $m \ge 2$ and every edge incident to $u$ contributes equal weight to another node $v \ne u$:

$$d(u) = \sum_{v \ne u} w_{uv} = \sum_{v \ne u} w_{vu} \le \sum_{v \ne u} d(v) = D - d(u) \implies d(u) \le \frac{D}{2}$$

Thus $\pi_{\max} = \max_{u \in V^+} \pi(u) \le \frac{1}{2}$, and by the min-entropy bound:

$$1 \le -\log_2 \pi_{\max} \le H_c(G) \le \log_2 m \qquad (\text{loop-free } G,\; m \ge 2)$$

with $H_c(G) = 1$ iff $m = 2$ (a single undirected edge).

### Ghost-Node Invariance & Normalization

Adding isolated "ghost" nodes ($d(u) = 0$) leaves $H_c(G)$ unchanged ($0 \log_2 0 = 0$), but artificially deflates naive normalization by $\log_2 |V|$. To compare graphs of different sizes without ghost-node dilution, normalize strictly by the active support size $m = |V^+|$ (for $m \ge 2$):

$$\hat{H}_c(G) = \frac{H_c(G)}{\log_2 m} \in \begin{cases} \left[\frac{1}{\log_2 m}, 1\right] & \text{loop-free } G \\ [0, 1] & \text{allowing self-loops} \end{cases}$$

### Domain-Decomposition Identity

Because $H_c(G)$ measures weighted-degree evenness (for instance, a centralized star graph with $n$ leaves has $\pi_{\text{hub}} = \frac{1}{2}$ and $\pi_{\text{leaf}} = \frac{1}{2n}$, yielding $H_c = \frac{1}{2} + n \cdot \frac{1}{2n}(1 + \log_2 n) = 1 + \frac{1}{2}\log_2 n$), separating cross-domain breadth from within-domain spread requires partitioning $V^+$ into disjoint conceptual domains $\mathcal{D} = \{V_1, \dots, V_K\}$.

Letting $p_d = \sum_{u \in V_d} \pi(u) = \frac{D_d}{D} > 0$ denote the domain weight share and $\pi_d(u) = \frac{\pi(u)}{p_d}$ denote the local distribution within domain $V_d$, Shannon's grouping axiom (A3) yields the exact decomposition:

$$H_c(G) = \underbrace{H(p_1, \dots, p_K)}_{H_{\text{between}}(\mathcal{D})\text{ (Domain Breadth)}} + \sum_{d=1}^K p_d \underbrace{H_c(G \mid V_d)}_{\text{Within-Domain Spread}}$$

---

## Section 5. Merging and Graph Coarsening

Coarsening two distinct active nodes $u \ne v \in V^+$ into a merged concept node $z = (u \oplus v)$ strictly decreases Axis 1 ($H_c$), but does **not** monotonically decrease Axis 2 ($h_{\text{rate}}$).

### Part A: The Probability Lemma (Mass Coarsening)

Merging two positive probability masses $a = \pi(u) > 0$ and $b = \pi(v) > 0$ into $a + b$ reduces Shannon entropy by:

$$H_c(G) - H_c(G') = -a\log_2 a - b\log_2 b + (a+b)\log_2(a+b) = (a+b)h_2\left(\frac{a}{a+b}\right) > 0$$

where $h_2(x) = -x\log_2 x - (1-x)\log_2(1-x)$ is the binary entropy function, strictly positive because $0 < \frac{a}{a+b} < 1$.

### Part B: The Degree-Preserving Adjacency Operator

Under the degree definition $d(x) = \sum_y w_{xy}$ of Section 1, preserving all remaining node degrees and total volume $D$ when replacing $u, v$ with $z = (u \oplus v)$ requires:

- **External edges ($x \notin \{u,v\}$):** $w'_{zx} = w'_{xz} = w_{ux} + w_{vx}$.
- **Internal self-loop:** Both prior self-loops and both directed orientations of the collapsed edge $\{u,v\}$ accumulate into the diagonal entry of $z$:

$$w'_{zz} = w_{uu} + w_{vv} + 2w_{uv}$$

*(In undirected NetworkX / stub-weight notation where $w_{xx} = 2w_{\text{loop}}(x)$, this is $w'_{\text{loop}}(z) = w_{\text{loop}}(u) + w_{\text{loop}}(v) + w_{uv}$.)*

**Verification:** Summing row $z$ gives:

$$d'(z) = \sum_{x \notin \{u,v\}} (w_{ux} + w_{vx}) + w_{uu} + w_{vv} + 2w_{uv} = d(u) + d(v)$$

For $x \notin \{u,v\}$, $d'(x) = \sum_{y \notin \{u,v\}} w_{xy} + w_{xu} + w_{xv} = d(x)$. Thus $D' = D$ and $\pi'(z) = \pi(u) + \pi(v)$, ensuring $H_c(G') < H_c(G)$.

### Counterexample: Non-Monotonicity of $h_{\text{rate}}$ Under $\oplus$

Consider the unweighted path graph $a - b - c$ ($w_{ab} = w_{bc} = 1$, no initial self-loops):

- **Before merge ($V^+ = \{a, b, c\}$):**
  - Degrees: $d(a) = 1$, $d(b) = 2$, $d(c) = 1$, $D = 4$, $\pi = (\frac{1}{4}, \frac{1}{2}, \frac{1}{4})$.
  - $H_c = 1.500\text{ bits}$.
  - Directed edge weights $q_{uv} = w_{uv}/D$: four edges $(a,b), (b,a), (b,c), (c,b)$ each with $q_{uv} = \frac{1}{4}$, so $H(q) = \log_2 4 = 2.000\text{ bits}$.
  - $h_{\text{rate}} = H(q) - H_c = 2.000 - 1.500 = 0.500\text{ bits}$.
- **After merging $z = b \oplus c$ ($V^+ = \{a, z\}$):**
  - Rewired weights: $w'_{az} = w'_{za} = 1$, $w'_{zz} = 0 + 0 + 2(1) = 2$.
  - Degrees: $d'(a) = 1$, $d'(z) = 3$, $D' = 4$, $\pi' = (\frac{1}{4}, \frac{3}{4})$.
  - $H_c' = -\frac{1}{4}\log_2\frac{1}{4} - \frac{3}{4}\log_2\frac{3}{4} = 2 - \frac{3}{4}\log_2 3 \approx 0.8113\text{ bits}$.
  - Nonzero cells of $q'$: $q'_{az} = \frac{1}{4}$, $q'_{za} = \frac{1}{4}$, $q'_{zz} = \frac{2}{4} = \frac{1}{2}$, giving $H(q') = 0.5 + 0.5 + 0.5 = 1.500\text{ bits}$.
  - $h_{\text{rate}}' = H(q') - H_c' = 1.500 - 0.8113 = \frac{3}{4}\log_2 3 - \frac{1}{2} \approx 0.6887\text{ bits} > 0.500\text{ bits}$.

*(Check via direct transitions: $P'_{az} = 1$ contributes $0$; $z$ transitions with $P'_{za} = \frac{1}{3}, P'_{zz} = \frac{2}{3}$, giving $h_{\text{rate}}' = \pi'_z h_2(\frac{1}{3}) = \frac{3}{4}\log_2 3 - \frac{1}{2} \approx 0.6887\text{ bits}$.)*

---

## Section 6. Rigorous Shannon Uniqueness

We establish $H(p_1, \dots, p_n) = -\sum_{i=1}^n p_i \log_2 p_i$ from three standard axioms on probability distributions $P = (p_1, \dots, p_n) \in \Delta_n$ and their uniform restriction $h(n) = H\left(\frac{1}{n}, \dots, \frac{1}{n}\right)$:

- **Axiom A1 (Continuity):** $H(p_1, \dots, p_n)$ is continuous on the probability simplex $\Delta_n$.
- **Axiom A2 (Monotonicity on Uniform Choices & Bit Normalization):** For positive integers $a \le b$, $h(a) \le h(b)$, with $h(2) = 1$.
- **Axiom A3 (Grouping / Recursivity):** If outcomes are partitioned into $m$ groups $G_1, \dots, G_m$ with group sums $q_k = \sum_{j \in G_k} p_j > 0$, then:

$$H(p_1, \dots, p_n) = H(q_1, \dots, q_m) + \sum_{k=1}^m q_k H\left(\frac{p_j}{q_k} : j \in G_k\right)$$

### Stage 1 — Deriving Additivity from A3

Partition $mn$ equally likely outcomes (each of probability $\frac{1}{mn}$) into $m$ contiguous groups of size $n$. Each group has $q_k = \frac{n}{mn} = \frac{1}{m}$, and each conditional distribution is uniform over $n$ elements ($\frac{1/mn}{1/m} = \frac{1}{n}$). Applying A3 yields:

$$h(mn) = h(m) + \sum_{k=1}^m \frac{1}{m} h(n) = h(m) + h(n)$$

Setting $m = n = 1$ gives $h(1) = 2h(1) \implies h(1) = 0$. By induction, $h(n^m) = m \cdot h(n)$ and $h(2^k) = k \cdot h(2) = k$ for all integers $k \ge 0$.

### Stage 2 — Integer Squeeze via A2

For any integer $n \ge 1$ and $m \ge 1$, let $k_m = \lfloor m \log_2 n \rfloor$, so $k_m \le m \log_2 n < k_m + 1$ and $2^{k_m} \le n^m \le 2^{k_m+1}$. By non-strict monotonicity (A2):

$$h(2^{k_m}) \le h(n^m) \le h(2^{k_m+1}) \implies k_m \le m \cdot h(n) \le k_m + 1 \implies \frac{k_m}{m} \le h(n) \le \frac{k_m + 1}{m}$$

Since $\left|\frac{k_m}{m} - \log_2 n\right| < \frac{1}{m}$, taking $m \to \infty$ yields $h(n) = \log_2 n$ by the Squeeze Theorem.

### Stage 3 — Extension to Positive Rationals via A3

Let $p_i = \frac{r_i}{M}$ with positive integers $r_i \ge 1$ summing to $\sum_{i=1}^n r_i = M$. Partition $M$ uniform atomic outcomes (entropy $h(M) = \log_2 M$) into $n$ contiguous blocks of sizes $r_1, \dots, r_n$. Within block $i$, the conditional distribution is uniform over $r_i$ atoms, so A3 gives:

$$\log_2 M = h(M) = H(p_1, \dots, p_n) + \sum_{i=1}^n p_i h(r_i) = H(p_1, \dots, p_n) + \sum_{i=1}^n p_i \log_2 r_i$$

Rearranging and using $\sum_{i=1}^n p_i \log_2 M = \log_2 M$ yields:

$$H(p_1, \dots, p_n) = \sum_{i=1}^n p_i \log_2 M - \sum_{i=1}^n p_i \log_2 r_i = -\sum_{i=1}^n p_i \log_2\left(\frac{r_i}{M}\right) = -\sum_{i=1}^n p_i \log_2 p_i$$

### Stage 4 — Extension to Reals & Boundary via A1

Because $\mathbb{Q}^n_{>0} \cap \Delta_n$ is dense in $\Delta_n$, Continuity (A1) uniquely extends $H(p_1, \dots, p_n) = -\sum_{i=1}^n p_i \log_2 p_i$ to all real probability distributions on $\Delta_n$, including boundary faces where $p_i = 0$ (with $\lim_{p \to 0^+} (-p\log_2 p) = 0$). $\blacksquare$

---

## Section 7. Three Observables of the Cognitive Graph

The framework characterizes a cognitive graph across three distinct axes:

### Axis 1: Static Degree Salience ($H_c$)

$$H_c(G) = -\sum_{u \in V^+} \pi_u \log_2 \pi_u, \qquad \pi_u = \frac{d(u)}{D}$$

Measures static evenness of weighted degree across $V^+$ (and decomposes into domain breadth $H_{\text{between}}(\mathcal{D})$ plus within-domain spread via Section 4).

### Axis 2: Associative Transition Entropy Rate ($h_{\text{rate}}$)

Deriving from detailed balance ($q_{uv} = \pi_u P_{uv} = w_{uv}/D$ and $P_{uv} = q_{uv}/\pi_u$):

$$\begin{aligned}
h_{\text{rate}}(G) &= -\sum_{u,v \in V^+} \pi_u P_{uv} \log_2 P_{uv} \\
&= -\sum_{u,v \in V^+} q_{uv} \log_2\left(\frac{q_{uv}}{\pi_u}\right) \\
&= -\sum_{u,v \in V^+} q_{uv} \log_2 q_{uv} + \sum_{u \in V^+} \left(\sum_{v \in V^+} q_{uv}\right)\log_2 \pi_u \\
&= H(q) - H_c(G)
\end{aligned}$$

In information-theoretic terms, $H(X_0, X_1) = H(q)$ is the joint two-step entropy, $H(X_0) = H_c(G)$ is the marginal node entropy, and $h_{\text{rate}}(G) = H(X_1 \mid X_0)$ measures step-to-step transition unpredictability.

- **Orthogonality to $H_c$:** On 6 nodes, the cycle $C_6$ and complete graph $K_6$ are both regular with $H_c = \log_2 6 \approx 2.585\text{ bits}$, yet $h_{\text{rate}}(C_6) = \log_2 2 = 1.000\text{ bit}$ while $h_{\text{rate}}(K_6) = \log_2 5 \approx 2.322\text{ bits}$.
- **Symmetry caveat:** Because $w_{uv} = w_{vu}$ enforces time-reversibility ($q_{uv} = q_{vu}$), capturing asymmetric logical implication ($A \implies B$) requires extending $P$ to a directed graph where $\pi \ne d/D$.

### Axis 3: Global Spectral Entropy ($S$)

Let $L = \operatorname{Deg}_{\text{simple}} - W_{\text{simple}}$ be the combinatorial graph Laplacian on $V^+$, where $L_{uu} = \sum_{v \ne u} w_{uv}$ and $L_{uv} = -w_{uv}$ ($u \ne v$), with eigenvalues $0 = \lambda_1 \le \lambda_2 \le \dots \le \lambda_m$. Because $L$ cancels diagonal entries $w_{uu}$, Axis 3 measures inter-node wiring topology and is **invariant to self-loops**. Defining a trace-normalized positive semidefinite operator $\rho$ yields the classical spectral entropy:

$$S(\rho) = -\operatorname{Tr}(\rho \log_2 \rho) = -\sum_{i=1}^m \mu_i \log_2 \mu_i$$

where $\{\mu_i\}$ are the eigenvalues of $\rho$ (with $0\log_2 0 = 0$). Two standard operators exist in network theory:

1. **Rescaled Laplacian** ([Braunstein, Ghosh, & Severini, 2006](https://arxiv.org/abs/quant-ph/0406165)):
   $\rho_{\text{BGS}} = \frac{L}{\operatorname{Tr}(L)}$ with $\mu_i = \frac{\lambda_i}{\sum_j \lambda_j}$ (defined when $G$ has at least one off-diagonal edge so $\operatorname{Tr}(L) > 0$). Emphasizes high-degree, high-eigenvalue modes, ranking $K_5$ ($2.000\text{ bits}$, eigenvalues $0,5,5,5,5$) above star $S_5$ ($1.549\text{ bits}$, eigenvalues $0,1,1,1,5$).
2. **Diffusion Heat Kernel** ([De Domenico & Biamonte, 2016](https://link.aps.org/doi/10.1103/PhysRevX.6.041062)):
   $\rho_\beta = \frac{e^{-\beta L}}{\operatorname{Tr}(e^{-\beta L})}$ with $\mu_i(\beta) = \frac{e^{-\beta \lambda_i}}{\sum_j e^{-\beta \lambda_j}}$ at diffusion scale $\beta > 0$ (well-defined even when all edges are self-loops, where $L = 0 \implies \rho_\beta = I_m/m$).
   - At $\beta = 1$, ranking flips relative to BGS: $S(K_5) \approx 0.228\text{ bits}$ ($97.4\%$ weight on $\lambda_1 = 0$) vs $S(S_5) \approx 1.855\text{ bits}$ (all 5 modes $\{0,1,1,1,5\}$, with $99.7\%$ thermal weight spread across $\{0,1,1,1\}$).
   - As $\beta \to \infty$, $\lim_{\beta \to \infty} S(\rho_\beta) = \log_2 k$ directly counts the number of disconnected conceptual silos $k$ (the multiplicity of $\lambda = 0$).

*(Note: In `yentellect/backend/graph.py`, Axis 3 is paired operationally with the normalized Laplacian spectral gap $\lambda_2(L_{\text{sym}})$ to identify low-mixing bottlenecks and Fiedler bridge candidates.)*
