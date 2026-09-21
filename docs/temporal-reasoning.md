# Temporal Reasoning & Earliest Supported Observations

Satellite observations are discrete temporal samples. TerraSeek implements rigorous temporal logic to prevent incorrect historical deductions.

## Key Principles

1. **Baseline Requirement**:
   To declare that a change occurred, a usable historical observation prior to the change must exist. If baseline imagery is unavailable, TerraSeek returns `INSUFFICIENT_EVIDENCE` rather than fabricating a conclusion.

2. **Observation Gap Analysis**:
   If the duration between consecutive satellite passes exceeds the acceptable threshold (e.g. > 365 days), the result is flagged for human review (`NEEDS_REVIEW`) to account for unobserved temporal gaps.

3. **Earliest Supported Observation**:
   TerraSeek determines the exact satellite pass that first evidences the physical change. The platform distinguishes between:
   - "Earliest Supported Observation" (the verifiable pass date).
   - Exact event occurrence date (which cannot be known without continuous surveillance).
