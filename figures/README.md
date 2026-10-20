# Figures

This folder contains the figures in the manuscript. Both are drawn by [`code/build_network.py`](../code/build_network.py). To change a figure, edit the code and rerun it; don't edit the image files.

## Which file to use

Each figure is saved twice, from the same drawing:

| Format | Use it for |
|---|---|
| `.pdf` (vector) | **LaTeX / Overleaf.** Text stays sharp at any zoom. |
| `.png` (300 dpi) | Word, Google Docs, slides, GitHub |

Both are drawn at their **printed size: 7 in wide**. That is the full text width of the two-column article template. At that width no text is smaller than 6.5 pt.

**Insert them at full width, never smaller.** Shrinking a figure shrinks its text with it. That is what made Figure 1 of the proposal unreadable: the earlier 12-inch version of the food web was scaled down to 5.3 in, which left its labels at about 3 pt.

In the LaTeX template, use the two-column-wide float:

```latex
\begin{figure*}
  \includegraphics[width=\textwidth]{cadiz_foodweb.pdf}
  \caption{...}
  \label{fig:foodweb}
\end{figure*}
```

In Word or Google Docs, insert the PNG at the full page width (6.5 in with 1-inch margins).

## Contents

| Files | What it shows | Used in |
|---|---|---|
| `cadiz_foodweb.pdf` / `.png` | The food web, with height = trophic level. Node colour = broad category; node size = importance as prey (summed diet share); arrow width = diet share (prey → predator); ring = cannibalism. Edges below 0.01 are drawn faint. | Proposal, Figure 1 (old 12-inch version) |
| `cadiz_diet_matrix.pdf` / `.png` | The culled 43 × 43 diet matrix as a heatmap on a log colour scale, with both axes ordered by trophic level. Category strips run along the axes, and cannibalism cells are outlined. | not yet |

### `cadiz_foodweb`

![Gulf of Cadiz food web drawn by trophic level](cadiz_foodweb.png)

### `cadiz_diet_matrix`

![Gulf of Cadiz diet matrix heatmap](cadiz_diet_matrix.png)
