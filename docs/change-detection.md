# Change Detection & Spectral Analysis

TerraSeek evaluates multi-temporal optical observations across four key change domains:

## 1. Building & Structural Development (`BUILDING`)
- Delineates newly constructed building footprints, residential developments, and industrial sites.
- **Production Interface**: Siamese U-Net with ResNet-34 backbone (`UNetResNet34ChangeModel`).
- **Demo Mode**: Normalized difference thresholding with structural edge delineation (`DemoChangeDetectionModel`).

## 2. Infrastructure & Roads (`ROAD`)
- Detects linear corridor grading, asphalt laying, and highway bypass expansions.

## 3. Vegetation Dynamics (`VEGETATION`)
- Computes the Normalized Difference Vegetation Index (NDVI):
  $$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$
- Delineates canopy loss, deforestation, and agricultural seasonal clearing.

## 4. Water Extent Fluctuations (`WATER`)
- Computes Modified Normalized Difference Water Index (MNDWI):
  $$\text{MNDWI} = \frac{\text{Green} - \text{SWIR}}{\text{Green} + \text{SWIR}}$$
- Delineates shoreline changes, reservoir contraction, and flood inundation.
