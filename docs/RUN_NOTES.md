# Run notes

## Seeds
Five independent end-to-end runs (seeds 1-5) with the same notebook. Seed 3's final cells (README generation and the copy to Drive) raised an error after the results package was complete; the package itself is intact. Seed 4 was run from an earlier text of the notebook whose computation is the same; only comments and housekeeping cells differ.

## Validity rule
A clustering is **invalid** if the smallest non-noise cluster has fewer than 3 points or fewer than two clusters remain after filtering. Invalid runs appear as missing rows in the per-seed tables and are reported as `valid/runs` in the aggregates. HDBSCAN `min_cluster_size` is chosen by contiguous-block cross-validation; the PELT penalty by a knee-point criterion with an over-segmentation guard.

## Snapshots
Higgs gives 168 / 28 / 14 snapshots at 1 h / 6 h / 12 h and is never capped. Reddit series are cut to the most recent 500 snapshots (about 21 / 125 / 250 days). At Higgs 12 h the 14 snapshots are too few for the proposed variants to yield a valid clustering in any run.

## Estimator fidelity
Exhaustive triad enumeration is only feasible on small snapshots, so the Jensen-Shannon divergence between the hybrid estimator and exhaustive counts is computed on up to 15 snapshots per dataset and resolution with at most 400 nodes (Higgs 1 h: 1.2e-5, 6 h: 5.3e-7; Reddit: 0; Higgs 12 h: no snapshot qualifies). This measures approximation fidelity, not computational scalability; runtime and memory comparisons are not part of the reported results.

## Baselines
- **Low-order statistics, motif counts, Louvain community descriptors:** no training; clustered with the common procedure. Motif counts give no valid clustering on Higgs.
- **TGN:** PyG reference components, 2 epochs, 900 s cap. Valid in 5/5 runs on Higgs 1 h, but in only part of the runs on Higgs 6 h and Reddit (see `aggregated/manuscript_tables_all.csv`).
- **DSBM approximation (excluded):** spectral clustering on a sparse snapshot adjacency capped at 300 nodes. Valid in 2 of 5 runs on Higgs at every resolution with implausibly high Silhouette (0.90-0.99), and Silhouette 0.00 on Reddit at 6 h and 12 h.
- **JODIE reimplementation (excluded):** several rounds of debugging (embedding collapse, interaction coverage, numerical overflow, downstream data validity) did not produce a valid clustering on any series. This is an implementation limitation and says nothing about JODIE itself.
- Baselines use fixed documented settings, so the comparison is not budget-matched (see the tuning table in the paper). DySAT and DyRep are not implemented.

## Event-anchored transition metrics
The CERN announcement of the Higgs boson discovery (4-5 July 2012, tolerance of two snapshots) is a descriptive reference. At the selected penalty no change point is detected on Higgs for the representations used in the transition analysis, so Transition Recall is 0. No comparable event exists for Reddit.

## Known limitations
- The smoothness weight λ = 2 was fixed from exploratory runs; separability is highest at λ = 5 in all five seeds.
- Visual figures are from seed 1 only.
- The Reddit analysis covers only the end of the stream.
