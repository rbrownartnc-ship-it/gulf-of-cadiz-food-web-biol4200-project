"""Shared functions for the food web analyses.

These functions are used by every analysis script and by the checks in code/checks/. Everything here works on the cleaned web that build_network.py writes to output/, so that has to run first.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
FIG = ROOT / "figures"
NONLIVING = {"Detritus", "Discard"}
SEED = 4200

# ---------------------------------------------------------------- data
def load_web():
    """The cleaned Gulf of Cadiz web as a DiGraph with edges prey -> predator.

    Edge attributes: w = original diet share, d = diet share rescaled so each predator's diet sums to 1. Node attributes: category, trophic_level, living. Returns (G, traits) where traits is output/cadiz_node_traits.csv.
    """
    edges = pd.read_csv(OUT / "cadiz_edges.csv")
    traits = pd.read_csv(OUT / "cadiz_node_traits.csv", index_col=0)
    G = nx.DiGraph()
    for n, r in traits.iterrows():
        G.add_node(n, category=r.category, trophic_level=r.trophic_level,
                   living=bool(r.living))
    for r in edges.itertuples():
        G.add_edge(r.prey, r.predator, w=r.diet_share, d=r.diet_share_renorm)
    assert G.number_of_nodes() == 43 and G.number_of_edges() == 411
    return G, traits


def simple(G):
    """The same web without cannibalistic self-loops and without weights."""
    H = nx.DiGraph()
    H.add_nodes_from(G)
    H.add_edges_from((u, v) for u, v in G.edges if u != v)
    return H

# ---------------------------------------------------------------- extinctions
class Cascade:
    """Secondary extinctions after removing groups from a food web.

    A consumer goes secondarily extinct once it has lost at least `theta` of its diet (rescaled diet shares; cannibalism never keeps a group alive).
      theta = 1   topological rule (Dunne, Williams & Martinez 2002): a
                  consumer dies only when every one of its prey is gone.
      theta < 1   weighted rule: e.g. 0.5 = dies after losing half its diet.
    Groups with no prey (phytoplankton, detritus, discard) never starve; they disappear only when removed directly.
    """

    def __init__(self, G):
        self.G = G
        self.diet = {n: {p: G[p][n]["d"] for p in G.predecessors(n) if p != n}
                     for n in G}

    def run(self, removed, theta=1.0, present=None, removed_links=()):
        """Remove the groups `removed` and the feeding links `removed_links` (pairs (prey, predator)) from `present` (default: every group), and return (still_present, secondary_extinctions)."""
        present = set(self.G if present is None else present) - set(removed)
        cut = set(removed_links)
        secondary = set()
        changed = True
        while changed:
            changed = False
            for n in sorted(present):
                diet = self.diet[n]
                if not diet:                         # basal: never starves
                    continue
                left = sum(s for p, s in diet.items() if p in present and (p, n) not in cut)
                if left <= (1 - theta) + 1e-12:
                    present.discard(n)
                    secondary.add(n)
                    changed = True
        return present, secondary


class LinkRemoval:
    """A faster version of Cascade for cutting feeding links one at a time (hundreds of steps), with the same extinction rule, so a consumer starves once its uncut links from living prey carry no more than 1 - theta of its diet. Losing predators never kills a group, so basal groups always stay. theta = None cuts links without any starvation (link percolation)."""

    def __init__(self, cascade, theta):
        self.diet, self.theta = cascade.diet, theta
        self.alive = set(cascade.G)
        self.links = {(p, n) for n, d in self.diet.items() for p in d}
        self.predators = {n: [] for n in cascade.G}
        for n, d in self.diet.items():
            for p in d:
                self.predators[p].append(n)
        self.secondary = set()

    def _starving(self, n):
        diet = self.diet[n]
        if not diet or self.theta is None:       # theta None: cut links, nothing starves
            return False
        left = sum(s for p, s in diet.items() if p in self.alive and (p, n) in self.links)
        return left <= (1 - self.theta) + 1e-12

    def _die(self, n):
        stack = [n]
        while stack:
            m = stack.pop()
            if m not in self.alive:
                continue
            self.alive.discard(m)
            self.secondary.add(m)
            for q in self.predators[m]:
                if q in self.alive and (m, q) in self.links and self._starving(q):
                    stack.append(q)

    def remove_link(self, prey, predator):
        """Cut one link and let starvation cascade."""
        if (prey, predator) not in self.links:
            return
        self.links.discard((prey, predator))
        if predator in self.alive and prey in self.alive and self._starving(predator):
            self._die(predator)

    def graph(self, G):
        """The surviving web: living groups and uncut links."""
        H = nx.DiGraph()
        H.add_nodes_from(self.alive)
        H.add_edges_from((p, n) for p, n in self.links if p in self.alive and n in self.alive)
        return H


def largest_wcc(G, present):
    """Size of the largest weakly connected component among `present`."""
    H = G.subgraph(present)
    return max((len(c) for c in nx.weakly_connected_components(H)), default=0)


def largest_scc(G, present):
    """Size of the largest strongly connected component (a feeding loop) among `present`; a lone group counts as 1."""
    H = G.subgraph(present)
    return max((len(c) for c in nx.strongly_connected_components(H)), default=0)

# ---------------------------------------------------------------- binary structure
def prey_averaged_tl(H):
    """Unweighted trophic level: 1 + mean trophic level of the prey (self-loops ignored), basal = 1. Used for the null-model comparison, where webs have no weights. Returns None if some group cannot be reached from a basal group."""
    nodes = list(H)
    k = {n: sum(1 for p in H.predecessors(n) if p != n) for n in nodes}
    i = {n: j for j, n in enumerate(nodes)}
    A = np.eye(len(nodes))
    for u, v in H.edges:
        if u != v:
            A[i[v], i[u]] -= 1 / k[v]
    try:
        tl = np.linalg.solve(A, np.ones(len(nodes)))
    except np.linalg.LinAlgError:
        return None
    if not np.all(np.isfinite(tl)) or tl.max() > 100:
        return None
    return dict(zip(nodes, tl))


def shortest_path_tl(H):
    """1 + length of the shortest food chain down to any basal group."""
    basal = [n for n in H if not any(p != n for p in H.predecessors(n))]
    dist = nx.multi_source_dijkstra_path_length(H, basal) if basal else {}
    return {n: 1 + dist[n] for n in dist}


def food_web_properties(G):
    """Standard food-web descriptors (Williams & Martinez 2000) for a web with edges prey -> predator. Self-loops count as cannibalism."""
    S = G.number_of_nodes()
    L = G.number_of_edges()
    H = simple(G)
    n_prey = {n: sum(1 for p in G.predecessors(n) if p != n) for n in G}
    n_pred = {n: sum(1 for q in G.successors(n) if q != n) for n in G}
    basal = [n for n in G if n_prey[n] == 0]
    top = [n for n in G if n_pred[n] == 0 and n_prey[n] > 0]
    sptl = shortest_path_tl(H)
    omn = [n for n in G if n_prey[n] > 1 and
           len({sptl.get(p) for p in G.predecessors(n) if p != n}) > 1]
    reachable = len(sptl) == S          # every group sits on a chain from a basal group
    tl = prey_averaged_tl(H)
    in_loop = sum(len(c) for c in nx.strongly_connected_components(H) if len(c) > 1)
    U = H.to_undirected()
    giant = U.subgraph(max(nx.connected_components(U), key=len))
    gen = np.array([G.in_degree(n) for n in G]) / (L / S)
    vul = np.array([G.out_degree(n) for n in G]) / (L / S)
    mutual = sum(1 for u, v in H.edges if H.has_edge(v, u)) / H.number_of_edges()
    # Trophic coherence (Johnson et al. 2014): SD over links of the difference in (unweighted) trophic level between predator and prey.
    q = np.std([tl[v] - tl[u] for u, v in H.edges]) if tl else np.nan
    return {
        "connectance": L / S**2,
        "link_density": L / S,
        "frac_basal": len(basal) / S,
        "frac_intermediate": (S - len(basal) - len(top)) / S,
        "frac_top": len(top) / S,
        "frac_cannibal": sum(1 for n in G if G.has_edge(n, n)) / S,
        "frac_omnivore": len(omn) / S if reachable else np.nan,
        "frac_in_loops": in_loop / S,
        "mean_trophic_level": np.mean(list(tl.values())) if tl else np.nan,
        "max_trophic_level": max(tl.values()) if tl else np.nan,
        "generality_sd": gen.std(),
        "vulnerability_sd": vul.std(),
        "clustering": nx.average_clustering(U),
        "path_length": nx.average_shortest_path_length(giant),
        "frac_mutual_links": mutual,
        "assortativity": nx.degree_assortativity_coefficient(U),
        "trophic_coherence_q": q,
    }


def niche_model(S, C, rng):
    """One niche-model web (Williams & Martinez 2000) with S species and expected directed connectance C, edges prey -> predator."""
    beta = 1 / (2 * C) - 1
    n = rng.uniform(0, 1, S)
    r = n * rng.beta(1, beta, S)
    r[np.argmin(n)] = 0                       # lowest niche value is basal
    c = rng.uniform(r / 2, n)
    lo, hi = c - r / 2, c + r / 2
    eats = (n[None, :] >= lo[:, None]) & (n[None, :] <= hi[:, None])   # [i, j]: i eats j
    G = nx.DiGraph()
    G.add_nodes_from(range(S))
    G.add_edges_from((j, i) for i, j in zip(*np.nonzero(eats)))
    return G


def acceptable_niche_web(G, C_target, tol=0.03):
    """The usual acceptance rules: connectance within tol of the target, one connected web, and every species reachable from a basal species."""
    S, L = G.number_of_nodes(), G.number_of_edges()
    if abs(L / S**2 - C_target) > tol * C_target:
        return False
    if not nx.is_weakly_connected(G):
        return False
    return prey_averaged_tl(simple(G)) is not None and len(shortest_path_tl(simple(G))) == S

# ---------------------------------------------------------------- importance
def pagerank_importance(H):
    """PageRank importance from Allesina & Pascual (2009). This runs PageRank on the web with links pointing from consumer to resource, plus a 'root' that every basal group points to and that points to every group. A group is important if important groups depend on it. The root is dropped at the end and the scores are rescaled to sum to 1."""
    R = H.reverse(copy=True)
    R.add_node("_root")
    for n in H:
        R.add_edge("_root", n)
        if not any(p != n for p in H.predecessors(n)):
            R.add_edge(n, "_root")
    pr = nx.pagerank(R, alpha=0.99, max_iter=10_000, tol=1e-12)
    pr.pop("_root")
    s = sum(pr.values())
    return {n: v / s for n, v in pr.items()}


# ---------------------------------------------------------------- figures
# Same setup as build_network.py. Figures are drawn at print size (7 in is the full page width of the two-column template and 3.4 in is one column), with text of at least 6.5 pt, and saved as a PDF and a 300-dpi PNG. Each figure shows one idea, and they go in numbered folders in figures/ by analysis.
COLUMN, FULL = 3.4, 7.0
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e1e0d9"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#898781"
CATEGORY_STYLE = {   # color + marker, so category never rests on color alone
    "invertebrates & plankton": (BLUE, "o"),
    "fishes": (ORANGE, "s"),
    "marine mammals, birds, turtles": (AQUA, "^"),
    "non-living": (GREY, "X"),
}

def use_style():
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 7.5,
                         "axes.labelsize": 7.5, "axes.titlesize": 7.5,
                         "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
                         "legend.fontsize": 6.5, "text.color": INK,
                         "axes.labelcolor": INK2, "xtick.color": INK2,
                         "ytick.color": INK2, "axes.edgecolor": GRID,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42})


def save(fig, folder, stem, width=COLUMN):
    """Save figures/<folder>/<stem>.pdf and .png, then close the figure. The canvas is narrowed until the cropped figure (labels included) is exactly `width` inches, so it prints at that width without shrinking."""
    for _ in range(6):
        w = fig.get_tightbbox(fig.canvas.get_renderer()).width + 0.08   # + pad_inches on both sides
        if abs(w - width) < 0.01:
            break
        fig.set_figwidth(fig.get_figwidth() - (w - width))
    d = FIG / folder
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.04,
                metadata={"CreationDate": None})
    fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def plain_log_ticks(axis):
    """Tick labels on a log axis as plain numbers (0.01, 0.1, 1; 1e−6 for tiny values) instead of 10^n, whose superscripts print below 5 pt."""
    from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter
    def fmt(v, _):
        if v <= 0:
            return ""
        return f"{v:g}" if v >= 0.001 else f"1e−{round(-np.log10(v))}"
    axis.set_major_locator(LogLocator(base=10))
    axis.set_major_formatter(FuncFormatter(fmt))
    axis.set_minor_formatter(NullFormatter())


def wrap_label(text, width=30):
    """Break a long tick label onto two lines: before its parenthesis if it has one, otherwise at a space (never inside a hyphenated word)."""
    import textwrap
    if len(text) <= width:
        return text
    if " (" in text:
        i = text.index(" (")
        return text[:i] + "\n" + text[i + 1:]
    lines = textwrap.wrap(text, width, break_on_hyphens=False)
    return text if len(lines) <= 1 else lines[0] + "\n" + " ".join(lines[1:])


def tidy(ax, grid="both"):
    """Recessive grid and ticks, shared by every single-panel figure."""
    if grid:
        ax.grid(axis=grid, color=GRID, lw=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(length=2, pad=1.5)


def category_legend(fig, y=-0.02, ncol=2):
    """Legend for color + marker by broad category, below the axes."""
    from matplotlib.lines import Line2D
    h = [Line2D([], [], ls="", marker=mk, color=c, markersize=4.5, label=cat)
         for cat, (c, mk) in CATEGORY_STYLE.items()]
    fig.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, y), ncol=ncol,
               frameon=False, handletextpad=0.2, columnspacing=1.0)


# ---------------------------------------------------------------- food web drawing
FOOD_WEB_RC = {"font.family": "sans-serif", "font.size": 8, "axes.labelsize": 8,
               "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
               "text.color": "#0b0b0b", "axes.labelcolor": "#52514e",
               "xtick.color": "#52514e", "ytick.color": "#52514e", "pdf.fonttype": 42}

def draw_food_web(G, tl, color, legend, path, weight="weight", height=6.6, crowded=False):
    """Draw a food web at 7 in wide: y = trophic level, x from a 1-D force layout (y held fixed), then nodes are pushed sideways until no two labels overlap. `color` maps each node to its color and `legend` lists (label, color) pairs. Node size = importance as prey, arrow width = diet share, ring = cannibalism. With `crowded`, a row of more than 8 groups at the same trophic level gets vertical labels under its nodes, as their names cannot fit side by side at 7 in. Saves path.pdf and path.png."""
    from itertools import combinations
    import matplotlib.patheffects as pe
    from matplotlib.lines import Line2D
    from matplotlib.transforms import Bbox
    INK_, INK2_, GRID_ = "#0b0b0b", "#52514e", "#e1e0d9"
    with plt.rc_context(FOOD_WEB_RC):
        names = list(G)
        loops = sorted(nx.nodes_with_selfloops(G))
        rng = np.random.default_rng(4)
        y = {n: tl[n] for n in G}
        x = {n: rng.uniform(-1, 1) for n in G}
        U = G.to_undirected()
        for _ in range(400):
            for n in G:
                pull = np.mean([x[m] for m in U[n] if m != n])
                push = sum(np.sign(x[n] - x[m]) * 0.012 / (abs(x[n] - x[m]) + 0.05)
                           for m in G if m != n and abs(y[n] - y[m]) < 0.35)
                x[n] = 0.85 * x[n] + 0.15 * pull + push
        xs = np.array(list(x.values()))
        x = {n: (x[n] - xs.min()) / (xs.max() - xs.min()) for n in G}

        below = set()                            # nodes with a vertical label underneath
        if crowded:
            for level in sorted({round(v, 2) for v in y.values()}):
                row = sorted((n for n in G if round(y[n], 2) == level), key=lambda n: x[n])
                if len(row) > 8:
                    below |= set(row)
                    for k, n in enumerate(row):  # start the crowded row evenly spaced
                        x[n] = k / (len(row) - 1)

        def wrap(name, width=15):
            """Break a long group name onto two lines at the space nearest the middle."""
            if len(name) <= width or " " not in name:
                return name
            cut = min((i for i, c in enumerate(name) if c == " "),
                      key=lambda i: abs(i - len(name) / 2))
            return name[:cut] + "\n" + name[cut + 1:]

        strength = pd.Series({n: G.out_degree(n, weight=weight) for n in names})
        size = 10 + 80 * np.sqrt(strength / strength.max())     # marker area, pt^2
        RING = 38                                               # extra area for the ring
        fig, ax = plt.subplots(figsize=(7.0, height))
        fig.subplots_adjust(left=0.07, right=0.995, top=0.99, bottom=0.1)
        ax.set_ylim(0.8, max(y.values()) + 0.25)
        def offset(n):
            d = 5.5 if n in loops else 3.5
            return (0, -d - 2) if n in below else (0, d)
        labels = {n: ax.annotate(n if n in below else wrap(n), (x[n], y[n]), xytext=offset(n),
                                 textcoords="offset points", ha="center",
                                 va="top" if n in below else "bottom",
                                 rotation=90 if n in below else 0,
                                 fontsize=6.5, linespacing=0.95, color=INK_, zorder=4,
                                 path_effects=[pe.withStroke(linewidth=1.8,
                                                             foreground="white")])
                  for n in G}
        def node_box(n):
            r = (np.sqrt(size[n] + (RING if n in loops else 0)) / 2 + 1.5) * fig.dpi / 72
            cx, cy = ax.transData.transform((x[n], y[n]))
            return Bbox.from_extents(cx - r, cy - r, cx + r, cy + r)

        rel = {}
        def measure():
            """Each label's box relative to its node, from one redraw at the current zoom."""
            fig.canvas.draw()
            for n in G:
                b = labels[n].get_window_extent()
                cx, cy = ax.transData.transform((x[n], y[n]))
                rel[n] = (b.x0 - cx, b.y0 - cy, b.x1 - cx, b.y1 - cy)

        def overlapping_pairs(redraw=False):
            """Every pair of nodes whose marker or label boxes touch. Label boxes move with their node, so one redraw per zoom is enough (redraw=True re-measures)."""
            if redraw or not rel:
                measure()
            pad = 3 * fig.dpi / 72                  # at least 6 pt between any two labels
            box = {}
            for n in G:
                cx, cy = ax.transData.transform((x[n], y[n]))
                x0, y0, x1, y1 = rel[n]
                box[n] = [Bbox.from_extents(cx + x0 - pad, cy + y0 - pad / 3, cx + x1 + pad,
                                            cy + y1 + pad / 3), node_box(n)]
            hits = []
            for a, b in combinations(G, 2):
                gaps = [min(ba.x1, bb.x1) - max(ba.x0, bb.x0)
                        for ba in box[a] for bb in box[b] if ba.overlaps(bb)]
                if gaps:
                    hits.append((a, b, gaps[0]))
            return hits

        pads = [0.06, 0.06]                      # room left and right of the outermost nodes
        def solve():
            # Push overlapping nodes apart at a fixed zoom; if the spread no longer fits that zoom, widen the view (which shrinks everything) and solve again.
            for _ in range(25):
                assert np.isfinite(list(x.values())).all(), "the labels cannot fit at this width"
                lo_x, hi_x = min(x.values()) - pads[0], max(x.values()) + pads[1]
                ax.set_xlim(lo_x, hi_x)
                px_per_x = ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]
                measure()
                for _ in range(400):
                    hits = overlapping_pairs()
                    if not hits:
                        break
                    for a, b, gap in hits:
                        d = (gap / 2 + 1) / px_per_x
                        lo, hi = (a, b) if (x[a], a) < (x[b], b) else (b, a)
                        x[lo] -= d
                        x[hi] += d
                    for n in G:
                        labels[n].xy = (x[n], y[n])
                if min(x.values()) - pads[0] >= lo_x and max(x.values()) + pads[1] <= hi_x:
                    break

        solve()
        for _ in range(10):                      # a label at either edge must stay inside the plot
            fig.canvas.draw()
            ext = [labels[n].get_window_extent() for n in G]
            px_per_x = ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]
            left, right = fig.bbox.x0 - min(e.x0 for e in ext), max(e.x1 for e in ext) - fig.bbox.x1
            if left <= 0 and right <= 0:
                break
            pads[0] += max(left, 0) * 1.2 / px_per_x
            pads[1] += max(right, 0) * 1.2 / px_per_x
            solve()
        assert not overlapping_pairs(redraw=True), "labels still overlap"
        pos = {n: (x[n], y[n]) for n in G}

        for u, v, d in sorted(G.edges(data=True), key=lambda e: e[2][weight]):
            if u == v:
                continue
            wt = d[weight]
            ax.annotate("", xy=pos[v], xytext=pos[u],
                        arrowprops=dict(arrowstyle="-|>", mutation_scale=4 + 4 * wt,
                                        lw=0.2 + 1.9 * wt, color=INK2_,
                                        alpha=0.07 + 0.6 * wt, shrinkA=3.5, shrinkB=3.5,
                                        connectionstyle="arc3,rad=0.08"))
        for n in G:
            ax.scatter(*pos[n], s=size[n], color=color[n],
                       edgecolor="white", linewidth=0.6, zorder=3)
            if n in loops:                          # ring marks cannibalism
                ax.scatter(*pos[n], s=size[n] + RING, facecolor="none",
                           edgecolor=INK_, linewidth=0.6, zorder=2)
        ax.set_ylabel("trophic level")
        ax.set_xticks([])
        for s in ("top", "right", "bottom"):
            ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(GRID_)
        ax.grid(axis="y", color=GRID_, lw=0.4)
        ax.set_axisbelow(True)
        handles = [Line2D([], [], marker="o", ls="", color=c, markersize=5, label=g)
                   for g, c in legend]
        handles += [Line2D([], [], marker="o", ls="", markerfacecolor="none",
                           markeredgecolor=INK_, markersize=6.5,
                           label="cannibalism (self-loop)"),
                    Line2D([], [], color=INK2_, lw=1.6, alpha=0.6,
                           label="prey → predator, width = diet share")]
        fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
                   columnspacing=1.2)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.04,
                    metadata={"CreationDate": None})
        fig.savefig(path.with_suffix(".png"), dpi=300, bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)
