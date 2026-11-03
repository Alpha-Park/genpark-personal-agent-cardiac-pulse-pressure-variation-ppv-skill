# Cardiac Pulse Pressure Variation (PPV) Personal Agent Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard%20JSON--RPC-orange.svg)]()
[![Production Ready](https://img.shields.io/badge/status-production--ready-green.svg)]()

Deterministic, zero-mock personal agent micro-skill for calculating Pulse Pressure Variation (PPV%) and Stroke Volume Variation (SVV%) to evaluate dynamic heart-lung interactions and predict fluid responsiveness under mechanical ventilation.

## Architecture

```mermaid
flowchart TD
    A[Arterial BP Waveform / Beat-by-Beat] --> B[Identify PP_max & PP_min Across Breath]
    B --> C[Compute PP_mean]
    C --> D[Compute PPV% = 100 * deltaPP / PP_mean]
    D --> E[Check Sinus Rhythm & Tidal Vol Validity]
    E --> F[Classify Fluid Responsive >= 13% vs Plateau]
```

## Quickstart

```python
from client import PulsePressureVariationClient

client = PulsePressureVariationClient()
result = client.evaluate_respiratory_variations(
    sbp_max_mmhg=125.0,
    dbp_max_mmhg=65.0,
    sbp_min_mmhg=105.0,
    dbp_min_mmhg=70.0,
    sv_max_ml=68.0,
    sv_min_ml=46.0,
    tidal_volume_ml_kg_pbw=8.5
)
print(result)
```

## License

Apache-2.0
