# Where each table and figure comes from

Per-seed files are in `results/seed<K>/tables/`; aggregated files in `results/aggregated/`. Table numbers follow the paper.

| Paper element | Content | Source |
|---|---|---|
| Table 4 | Tuning budget by method | Documented in the paper; settings in `results/seed<K>/manifest.json` (`config`) |
| Table 5 | Exploratory raw-feature comparison, Higgs 1 h | `table_ablation_higgs_1h.csv`, `table_headline_higgs_1h.csv` per seed |
| Table 6 | Pipeline-controlled modality ablation, Higgs 1 h | `aggregated/ablation_all_subsets.csv`, `table_D4_corrected_ablation_higgs_1h.csv` per seed |
| Table 7 | Baseline comparison, Higgs 1 h | `aggregated/manuscript_tables_all.csv` (Dataset = higgs, Resolution_h = 1), `aggregated/table_higgs_1h.tex` |
| Table 8 | Embedding drift | `aggregated/stability_long.csv` |
| Table 9 | Raw-feature modality ablation | `table_ablation_higgs_1h.csv` per seed |
| Table 10 | Reddit comparison, 6 h | `aggregated/manuscript_tables_all.csv` (reddit, 6), `aggregated/table_reddit_6h.tex` |
| Table 11 | Block bootstrap, Reddit | `aggregated/bootstrap_long.csv` |
| Table 12 | Temporal resolution, Reddit (change points and Silhouette) | `aggregated/d7_long.csv` (change points), `aggregated/ablation_all_subsets.csv` (Silhouette) |
| Tables 13-16 | Higgs 6 h / 12 h, Reddit 1 h / 12 h | `aggregated/table_<dataset>_<res>h.tex` |
| Smoothness sweep (Section 4.4) | Persistence and Silhouette against lambda | `aggregated/lambda_sweep_long.csv` |
| JSD values (Section 4.1) | Estimator fidelity | `results/seed<K>/run_log.txt` (JSD section) |

| Figure | File |
|---|---|
| JSD against resolution | `figures/fig_jsd_vs_resolution.png` |
| Penalty sweep, four representations (Higgs 1 h) | `figures/fig_penalty_curves_4panel_higgs_1h.png` |
| Penalty sweep (Reddit 1 h) | `figures/fig_penalty_sweep_reddit_1h.png` |
| UMAP, fused pre-GRU and regimes (Higgs 1 h) | `figures/fig_umap_fused_pregru_higgs_1h.png`, `figures/fig_umap_regimes_higgs_1h.png` |
| Regime timeline (Higgs 1 h) | `figures/fig_regime_timeline_higgs_1h.png` |
| Transition matrix (Higgs 1 h) | `figures/fig_transition_matrix_higgs_1h.png` |

Visual figures come from seed 1. All other figures of seed 1 are in `results/seed1/figures/`.
