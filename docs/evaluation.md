# Evaluation Framework & Benchmark Metrics

TerraSeek provides an objective evaluation framework to benchmark retrieval and spatial/temporal precision against ground-truth manifests.

## Evaluated Metrics
- **Precision@K**: Measures fraction of relevant satellite candidates within top-K retrieved.
- **Recall@K**: Measures coverage of target sites in top-K candidates.
- **Intersection over Union (IoU)**: Validates accuracy of delineated change boundary masks against ground-truth polygons.
- **Spatial Constraint Accuracy**: Measures topological adherence (e.g. distance to river within buffer).
- **Temporal Continuity Accuracy**: Measures accuracy of earliest supported observation detection.
- **No-Match Accuracy**: Validates that unmatchable or nonexistent targets (e.g. "new airport") produce strict `NO_MATCH` without false positives.

## Running Evaluation Benchmark

```bash
python -m terraseek.cli evaluate
```
