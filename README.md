# Triadic macrostate regime detection

Code and results for *Interpretable Temporal Regime Detection in Complex Networks Using Triadic Macrostate Representations*.

The method turns each snapshot of a temporal interaction network into a small, interpretable descriptor built from **triadic macrostates** (64 directed-triad microstates aggregated into six macrostates, S1-S6), fuses it with temporal and semantic features, learns a temporal embedding with a GRU, and then finds regimes with **PELT** (change points) and **HDBSCAN** (clusters).

Two public SNAP datasets are used: the Higgs Twitter activity stream and the Reddit Hyperlink Network.

## Repository layout

```
notebooks/
  01_pipeline.ipynb                    full pipeline for one seed (data, features, model, baselines, ablations)
  02_aggregate_seeds.ipynb             mean ± SD over seeds -> results/aggregated/
  03a_early_comparison_reproduction_higgs.ipynb
  03b_early_comparison_reproduction_reddit.ipynb
                                       provenance of the baseline rows of an earlier comparison (see PROVENANCE.md)
scripts/
  parse_run_logs.py                    collects quantities that the pipeline prints (lambda sweep, drift, bootstrap)
results/
  seed1 ... seed5/                     tables/, manifest.json, run_log.txt (seed1 also has figures/)
  aggregated/                          multi-seed tables (.csv, .tex) and long-format run records
figures/                               figures used in the paper (seed 1)
docs/
  TABLE_MAP.md                         which file produces which table / figure of the paper
  RUN_NOTES.md                         protocol details and known limitations
PROVENANCE.md
```

## Quick start

The pipeline was run on Google Colab with a GPU runtime, one seed per session. A run is long (temporal-embedding sweeps and TGN training dominate), and the notebook logs per-cell timings to `triadic_seed_runs/timings_seed<K>.csv`.

1. Open `notebooks/01_pipeline.ipynb` in Colab (or locally with `pip install -r requirements.txt`).
2. Set `RUN_SEED` in the first code cell and choose *Run all*. Datasets are downloaded from `snap.stanford.edu` and cached in `triadic_seed_runs/data_cache`.
3. The notebook writes `experiment_results_seed<K>.zip` (tables, figures, manifest). Repeat for seeds 1-5.
4. Put the unzipped folders under `results/seed<K>/` and run `notebooks/02_aggregate_seeds.ipynb`.

To inspect the numbers without re-running anything, use `results/aggregated/`: `manuscript_tables_all.csv` holds every method / dataset / resolution cell, and `all_runs_long.csv` has one row per run.

## Main findings (five seeds, mean ± SD, Silhouette)

| Higgs, 1 h | valid/runs | Silhouette |
|---|---|---|
| Proposed, structural-only | 5/5 | 0.827 ± 0.082 |
| TGN (PyG reference) | 5/5 | 0.748 ± 0.039 |
| Low-order degree statistics | 5/5 | 0.739 |
| Proposed, full multimodal (normalised loss) | 5/5 | 0.663 ± 0.124 |
| Community (Louvain) | 5/5 | 0.511 ± 0.069 |
| Motif counts | 0/5 | no valid clustering |

On Reddit no method is consistently best and the ordering changes with resolution. See the paper and `results/aggregated/` for all tables.

## Protocol in brief

- **Seeds:** five runs (1-5); triad sampling, network initialisation, Louvain seeding and UMAP vary with the seed.
- **Validity:** a clustering is invalid if its smallest cluster has fewer than 3 points or fewer than 2 clusters survive. Invalid runs are counted (`valid/runs`), never dropped silently.
- **Selection:** the PELT penalty is chosen by a knee-point criterion with an over-segmentation guard; HDBSCAN `min_cluster_size` by contiguous-block cross-validation (no shuffled folds). All methods use the same clustering procedure.
- **Reddit window:** only the 500 most recent snapshots of each series are analysed (about 21, 125 and 250 days at 1 h, 6 h and 12 h).
- **Excluded baselines:** a spectral DSBM approximation (unstable) and a JODIE reimplementation (no valid clustering) are implemented in the pipeline for transparency but not reported.
- **Smoothness weight:** λ = 2 was fixed from exploratory runs before the five-seed sweep. The sweep (`results/aggregated/lambda_sweep_long.csv`) shows that it is not the separability-maximising value.

See `docs/RUN_NOTES.md` for details and limitations.

## Data

| Dataset | Source |
|---|---|
| Higgs Twitter | https://snap.stanford.edu/data/higgs-twitter.html (`higgs-activity_time.txt.gz`) |
| Reddit Hyperlink Network | https://snap.stanford.edu/data/soc-RedditHyperlinks.html (`soc-redditHyperlinks-title.tsv`) |

The public Higgs release contains no tweet text, so its semantic features are interaction-type frequencies (RT / MT / RE). For Reddit, the 86-dimensional LIWC-style property vector shipped with the dataset is used.

## License

MIT, see `LICENSE`.
