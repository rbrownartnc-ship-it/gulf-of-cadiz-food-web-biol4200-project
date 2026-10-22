"""Independent check of the extinction rule used by node_removal.py and
edge_removal.py.

    python code/checks/verify_cascade.py

Re-implements the rule from the edge list as matrix algebra (no shared code
with foodweb.Cascade or foodweb.LinkRemoval) and compares, at thresholds of
all / 3/4 / 1/2 / 1/4 of the diet:
  - every single-group removal and 300 random multi-group removals,
  - every single-link cut and 300 random sets of cut links,
  - the incremental LinkRemoval against the batch Cascade along 50 random
    link-cutting sequences.
Then it runs a deliberately broken copy of the checker (strict instead of
non-strict threshold) and confirms that copy fails, so a pass means something.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from foodweb import OUT, load_web, Cascade, LinkRemoval

e = pd.read_csv(OUT / "cadiz_edges.csv")
e = e[e.prey != e.predator]                                   # cannibalism never sustains
names = sorted(set(e.prey) | set(e.predator))
ix = {n: i for i, n in enumerate(names)}
N = len(names)
D = np.zeros((N, N))                                           # D[prey, predator]
for r in e.itertuples():
    D[ix[r.prey], ix[r.predator]] = r.diet_share_renorm
consumer = D.sum(0) > 0
LINKS = [(r.prey, r.predator) for r in e.itertuples()]


def matrix_cascade(removed, theta, cut_links=(), strict=False):
    """Groups that starve after removing `removed` and cutting `cut_links`."""
    A = D.copy()
    for p, n in cut_links:
        A[ix[p], ix[n]] = 0
    alive = np.ones(N, bool)
    alive[[ix[n] for n in removed]] = False
    while True:
        avail = A.T @ alive
        limit = 1 - theta
        dead = alive & consumer & ((avail < limit - 1e-12) if strict else (avail <= limit + 1e-12))
        if not dead.any():
            break
        alive &= ~dead
    return {names[i] for i in range(N) if not alive[i]} - set(removed)


def run_checks(strict=False):
    G, _ = load_web()
    cas = Cascade(G)
    rng = np.random.default_rng(1)
    n_checks = 0
    for theta in (1.0, 0.75, 0.5, 0.25):
        for n in names:                                           # single groups
            assert matrix_cascade([n], theta, strict=strict) == cas.run([n], theta)[1], ("group", n, theta)
            n_checks += 1
        for _ in range(300):                                      # random sets of groups
            rem = list(rng.choice(names, rng.integers(2, 20), replace=False))
            assert matrix_cascade(rem, theta, strict=strict) == cas.run(rem, theta)[1], ("groups", theta)
            n_checks += 1
        for link in LINKS:                                        # single links
            got = cas.run([], theta, removed_links=[link])[1]
            assert matrix_cascade([], theta, [link], strict=strict) == got, ("link", link, theta)
            n_checks += 1
        for _ in range(300):                                      # random sets of links
            cut = [LINKS[i] for i in rng.choice(len(LINKS), rng.integers(2, 200), replace=False)]
            got = cas.run([], theta, removed_links=cut)[1]
            assert matrix_cascade([], theta, cut, strict=strict) == got, ("links", theta)
            n_checks += 1
        for _ in range(50):                                       # incremental vs batch
            order = [LINKS[i] for i in rng.permutation(len(LINKS))]
            st = LinkRemoval(cas, theta)
            for k, link in enumerate(order, 1):
                st.remove_link(*link)
                if k % 25 == 0:
                    assert st.secondary == matrix_cascade([], theta, order[:k], strict=strict), ("seq", theta, k)
                    n_checks += 1
    return n_checks


if __name__ == "__main__":
    n = run_checks()
    print(f"{n} comparisons: repo cascade == independent matrix cascade")
    try:
        run_checks(strict=True)
    except AssertionError as err:
        print(f"mutation test: the deliberately broken checker fails as it should ({err.args[0][:2]})")
    else:
        raise SystemExit("mutation test FAILED: a broken checker still passed, so the check proves nothing")
