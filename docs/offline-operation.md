# Offline-First Operation & Zero-Internet Deployments

TerraSeek is architected to operate securely in air-gapped or offline analytical environments without external internet connectivity.

## Design Safeguards

1. **Zero External Tile Dependencies**:
   MapLibre GL and the frontend UI do not depend on remote cloud map tiles (Mapbox, Google Maps, or remote XYZ servers). The map renders local SVG coordinate grids, relief features, and GeoJSON overlays natively.

2. **Self-Contained Vector Storage**:
   Qdrant operates locally via Docker or in-memory mode without external cloud API calls.

3. **Deterministic Local Model Adapters**:
   When production foundation model weights (GeoRSCLIP or Siamese U-Net) are not pre-downloaded, TerraSeek uses deterministic local adapters rather than blocking startup or failing silently.

4. **Bundled Static Assets**:
   Demonstration GeoTIFFs, thumbnails, and vector layers are generated and bundled locally.
