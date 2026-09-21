# Vector Retrieval & Similarity Search

TerraSeek integrates Qdrant for semantic and visual vector similarity retrieval.

## Embedding Providers

1. **GeoRSCLIPEmbeddingModel**:
   - Production vision-language model trained specifically on remote sensing optical imagery.
   - Computes dense 512-dimensional or 768-dimensional normalized feature vectors.
   - Explicitly checks for loaded model weights; fails with a clean `RuntimeError` rather than fabricating vectors if weights are unconfigured.

2. **DemoEmbeddingModel**:
   - Deterministic local hash-projection adapter designed for offline development and testing.
   - Generates reproducible unit vectors based on text tokenization or image content hashes.
   - Clearly labeled as `ModelTier.DEMO` across all API and UI responses.

## Retrieval Workflow
1. Natural language query or uploaded image patch is converted into a query vector.
2. Qdrant performs fast approximate cosine similarity search.
3. Candidate results are filtered by spatial bounding boxes and semantic tags.
4. Candidates are forwarded to spatial, temporal, and change engines for verification. Vector score alone is **never** treated as final proof.
