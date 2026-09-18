# ARIS4C010 · Formal core v0.1

This file records baseline propositions that the empirical benchmark must respect. They are mostly elementary or reductions to known problems; they are **not presented as novelty by themselves**.

## Definitions

Let:

- (C) be the set of candidate targets;
- (Q) be the set of admissible queries;
- (R) be the finite answer alphabet;
- (A(c,q)in R) be the oracle response for target (c) and query (q), after all required context has been frozen;
- a policy (pi) select queries adaptively from the history of query/answer pairs.

For (Q'\subseteq Q), define the response signature

[
\sigma_{Q'}(c)=(A(c,q))_{q\in Q'}.
]

Two candidates are **query-equivalent** under (Q') iff their signatures are identical.

---

## Proposition 1 · finite-channel capacity

Any deterministic decision tree with maximum depth (b) and at most (r=|R|) outgoing answer branches per query has at most (r^b) leaves.

Therefore exact identification of (N) possible targets in worst case requires

[
b\ge \lceil\log_r N\rceil.
]

### Proof sketch
A rooted tree with branching factor at most (r) and depth at most (b) has no more than (r^b) depth-(b) response strings, hence no more than (r^b) uniquely addressable leaves.

### Consequences
- 20 binary responses: at most (2^{20}=1,048,576) leaves.
- 21 binary responses: at most (2^{21}=2,097,152) leaves.
- This is a channel bound, not a semantic ontology result.

---

## Proposition 2 · no universal finite worst-case budget for an infinite target universe

If (C) is infinite and (R) is finite, no fixed finite (b) can guarantee exact identification of every (c\in C).

### Proof
By Proposition 1, a depth-(b) protocol can distinguish at most (r^b) targets, which is finite.

### Important nuance
This does **not** imply every target requires infinitely many questions.

For a countably infinite target set, a prefix code can assign every individual target a finite but unbounded code length. Under a sufficiently concentrated prior with finite entropy, expected code length can also be finite.

Thus distinguish:
- finite worst-case bound;
- finite per-target identification;
- finite expected identification cost.

---

## Proposition 3 · separability criterion for finite closed worlds

For finite (C), exact deterministic identification using queries from (Q) is possible iff

[
\forall c_i\neq c_j,\exists q\in Q:
A(c_i,q)\neq A(c_j,q).
]

### Necessity
If two targets give the same answer to every admissible query, no adaptive history can separate them.

### Sufficiency
Because (C) is finite, there are finitely many target pairs. Choose one separating query for every pair. The resulting finite subfamily has an injective joint response signature, so asking that finite set non-adaptively already identifies every target. An adaptive tree can then be constructed as well.

### Interpretation
The prerequisite is not a complete metaphysical taxonomy. It is a **separating query family relative to the chosen target universe**.

---

## Proposition 4 · static minimum basis reduces to Test Cover in the deterministic binary case

Suppose (R=\{0,1\}). For each query (q), define

[
T_q=\{c\in C:A(c,q)=1\}.
]

A subset (Q'\subseteq Q) gives every candidate a unique binary signature iff for every pair (c_i,c_j), at least one selected (T_q) contains exactly one of them.

That is precisely a Test Cover.

### Consequence
Finding a minimum static binary semantic basis is NP-hard in general by the known complexity of Test Cover.

The mapping is useful for 010 but not a novel combinatorial problem.

---

## Proposition 5 · admissible-query monotonicity

If (Q_1\subseteq Q_2), then the optimal identification cost using (Q_2) cannot be worse than the optimal cost using (Q_1), under the same candidate set, response model and cost function.

[
L^*(Q_2)\le L^*(Q_1).
]

### Consequence
Restricting unrestricted partitions to semantically admissible natural-language questions induces a non-negative overhead:

[
\Delta_{sem}=L^*(Q_{sem})-L^*(Q_{all})\ge 0.
]

This inequality is definitional. The empirical contribution is measuring its magnitude and predictors.

---

## Proposition 6 · response coarsening cannot increase information

Let a rich response (Y\in R_{rich}) be deterministically mapped to a coarser response (Z=f(Y)), such as forcing BORDERLINE, UNKNOWN, UNDEFINED and BOTH into binary YES/NO.

Then by the data-processing inequality,

[
I(C;Z)\le I(C;Y).
]

### Consequence
A richer response protocol weakly dominates a deterministic coarsening in information content **per observed response**.

This does not prove that a rich protocol is always better in practice:
- it may impose greater human cognitive cost;
- labels may be less reliable;
- response time may increase;
- comparison by number of questions can differ from comparison by transmitted bits or total interaction cost.

These must be measured separately.

---

## Proposition 7 · context is part of the oracle definition

If there exist (x_1,x_2) such that

[
A(c,q,x_1)\neq A(c,q,x_2),
]

then (A(c,q)) is not a well-defined deterministic benchmark response without fixing, inferring or querying the relevant context variable.

### Consequence
Indexicals, comparison-class predicates and institutional/contextual concepts cannot simply be assigned one universal YES/NO matrix.

---

## Proposition 8 · open-world non-detectability under signature aliasing

Let (C_{in}) be the active closed-world candidate set and (c_{out}\notin C_{in}) an out-of-support target.

If there exists (c_{in}\in C_{in}) such that

[
A(c_{out},q)=A(c_{in},q)\quad\forall q\in Q,
]

then no policy restricted to (Q) can distinguish (c_{out}) from (c_{in}).

### Consequence
An OUT-OF-SUPPORT option is not sufficient by itself. Detectability requires:
- separating queries not exhausted by the in-support ontology;
- model mismatch/residual evidence;
- generative ontology expansion;
- or an explicit external validation channel.

This gives a principled benchmark for open-world failure rather than treating OOS as a free abstention token.

---

## Proposition 9 · strong ineffability lies outside ordinary query-game semantics

Ordinary concept identification assumes an oracle can:
1. maintain a stable representation of the target;
2. understand the query;
3. judge the query relative to that target.

If a putative content is strongly ineffable in the sense that the relevant cognitive system cannot form or maintain the content at all, the oracle function (A(c,q)) is not defined in the ordinary way.

### Consequence
"Strongly ineffable content" should be a **boundary of the task model**, not just another row in the response matrix.

Weak linguistic ineffability is different: a target can be represented/recognized even if the current language lacks a compact lexical expression.

---

# Empirical quantities built on the formal core

For a candidate distribution (p(c)):

### Shannon lower bound
[
H(C)=-\sum_c p(c)\log_2 p(c).
]

### Semantic Query Overhead
[
\Delta_{sem}=E[L^*_{sem}]-E[L^*_{all}].
]

### Normalized binary semantic efficiency
[
\eta_{sem}=\frac{H(C)}{E[L_{sem}]}.
]

### Pairwise separation coverage
[
Sep(Q)=
\frac{
|\{(i,j):\exists q\in Q, A(c_i,q)\neq A(c_j,q)\}|
}{
\binom{|C|}{2}
}.
]

### Collision profile
The multiset of query-equivalence-class sizes under the chosen (Q).

---

# Formal work still worth doing

1. noisy/stochastic oracle extension;
2. query-specific answer alphabet and costs;
3. abstention/unknown channel with reliability;
4. sufficient conditions for greedy semantic information gain to approximate the optimal policy;
5. open-world Bayesian formulation with a nonparametric/OOS mass;
6. lower bounds when admissible queries are constrained by ontology syntax;
7. relationship between adaptive semantic questioning and minimum distinguishing descriptions / pragmatic reference games.
