"""
Example usage of Cardiac Pulse Pressure Variation (PPV) Skill.
Demonstrates hypovolemic fluid responsiveness vs normovolemic plateau state.
"""

import json
from client import PulsePressureVariationClient


def main():
    print("=== Testing Cardiac Pulse Pressure Variation (PPV) Skill ===")
    client = PulsePressureVariationClient()

    # 1. Hypovolemic septic patient under volume-controlled ventilation (PP_max=125-65=60, PP_min=105-70=35 -> PP_mean=47.5, PPV=52.6% -> Responsive)
    res_responsive = client.evaluate_respiratory_variations(
        sbp_max_mmhg=125.0,
        dbp_max_mmhg=65.0,
        sbp_min_mmhg=105.0,
        dbp_min_mmhg=70.0,
        sv_max_ml=68.0,
        sv_min_ml=46.0,
        tidal_volume_ml_kg_pbw=8.5,
        heart_rhythm_regular=True
    )
    print("\n[Case 1: Severe Volume Responsiveness (PPV > 13%)]")
    print(json.dumps(res_responsive, indent=2))

    # 2. Normovolemic stabilized patient (PP_max=120-72=48, PP_min=118-73=45 -> PP_mean=46.5, PPV=6.5% -> Non-Responsive)
    res_non_responsive = client.evaluate_respiratory_variations(
        sbp_max_mmhg=120.0,
        dbp_max_mmhg=72.0,
        sbp_min_mmhg=118.0,
        dbp_min_mmhg=73.0,
        sv_max_ml=62.0,
        sv_min_ml=59.0,
        tidal_volume_ml_kg_pbw=8.0,
        heart_rhythm_regular=True
    )
    print("\n[Case 2: Normovolemic Non-Responsive State (PPV < 9%)]")
    print(json.dumps(res_non_responsive, indent=2))

    # Assertions
    assert res_responsive["dynamic_indices"]["pulse_pressure_variation_ppv_pct"] > 13.0
    assert "Responsive" in res_responsive["interpretation"]["fluid_responsiveness"]
    assert res_non_responsive["dynamic_indices"]["pulse_pressure_variation_ppv_pct"] < 9.0
    assert "Non-Responsive" in res_non_responsive["interpretation"]["fluid_responsiveness"]
    print("\n[SUCCESS] Cardiac PPV tests passed!")


if __name__ == "__main__":
    main()
