"""
Cardiac Pulse Pressure Variation (PPV) & Stroke Volume Variation (SVV) Client.
Zero-mock pure Python standard library implementation.
Calculates Pulse Pressure Variation (PPV%), Stroke Volume Variation (SVV%),
and predicts fluid responsiveness under mechanical ventilation using the Michard index.
"""

import math
from typing import Dict, Any, Optional, List


class PulsePressureVariationClient:
    """
    Evaluates heart-lung interactions and preload responsiveness during positive pressure ventilation:
    PP = Systolic BP - Diastolic BP
    PP_max = SBP_max - DBP_max (typically inspiratory)
    PP_min = SBP_min - DBP_min (typically expiratory)
    PP_mean = (PP_max + PP_min) / 2.0
    PPV% = 100.0 * (PP_max - PP_min) / PP_mean
    SVV% = 100.0 * (SV_max - SV_min) / ((SV_max + SV_min) / 2.0)
    """

    def __init__(self):
        pass

    def evaluate_respiratory_variations(
        self,
        sbp_max_mmhg: float,
        dbp_max_mmhg: float,
        sbp_min_mmhg: float,
        dbp_min_mmhg: float,
        sv_max_ml: Optional[float] = None,
        sv_min_ml: Optional[float] = None,
        tidal_volume_ml_kg_pbw: Optional[float] = 8.0,
        heart_rhythm_regular: Optional[bool] = True
    ) -> Dict[str, Any]:
        """
        Calculates PPV and SVV metrics.
        sbp_max_mmhg, dbp_max_mmhg: peak systolic and corresponding diastolic pressures during breath cycle.
        sbp_min_mmhg, dbp_min_mmhg: minimum systolic and corresponding diastolic pressures during breath cycle.
        sv_max_ml, sv_min_ml: optional maximal and minimal stroke volumes (mL) from pulse contour or Doppler.
        tidal_volume_ml_kg_pbw: tidal volume in mL/kg predicted body weight (criterion requires >= 8 mL/kg).
        heart_rhythm_regular: sinus rhythm required (atrial fibrillation invalidates PPV).
        """
        if sbp_max_mmhg <= dbp_max_mmhg or sbp_min_mmhg <= dbp_min_mmhg:
            raise ValueError("Systolic pressures must be strictly greater than diastolic pressures.")
        if sbp_min_mmhg <= 0 or dbp_min_mmhg <= 0:
            raise ValueError("Blood pressures must be strictly positive.")

        pp_max = sbp_max_mmhg - dbp_max_mmhg
        pp_min = sbp_min_mmhg - dbp_min_mmhg

        if pp_max < pp_min:
            # Swap if inverted input
            pp_max, pp_min = pp_min, pp_max

        pp_mean = (pp_max + pp_min) / 2.0
        if pp_mean <= 0:
            raise ValueError("Mean pulse pressure must be positive.")

        ppv_pct = 100.0 * (pp_max - pp_min) / pp_mean

        # Stroke volume variation (SVV)
        svv_pct = None
        if sv_max_ml is not None and sv_min_ml is not None:
            if sv_max_ml > 0 and sv_min_ml > 0:
                if sv_max_ml < sv_min_ml:
                    sv_max_ml, sv_min_ml = sv_min_ml, sv_max_ml
                sv_mean = (sv_max_ml + sv_min_ml) / 2.0
                svv_pct = round(100.0 * (sv_max_ml - sv_min_ml) / sv_mean, 1)

        # Validity check for dynamic preload indices
        validity_warnings = []
        if not heart_rhythm_regular:
            validity_warnings.append("Arrhythmia / irregular rhythm present; beat-to-beat variability invalidates PPV/SVV interpretation.")
        if tidal_volume_ml_kg_pbw < 8.0:
            validity_warnings.append(f"Low tidal volume ({tidal_volume_ml_kg_pbw} mL/kg); threshold may underestimate true fluid responsiveness (Tidal Volume Challenge recommended).")

        # Clinical interpretation based on Michard & Marik criteria:
        # PPV >= 13%: Fluid Responsive (high probability of >15% increase in cardiac index with 500 mL crystalloid)
        # PPV 9 - 12%: Gray Zone (intermediate responsiveness, passive leg raising test indicated)
        # PPV < 9%: Fluid Non-Responsive (preload independent, risk of volume overload/pulmonary congestion)
        if ppv_pct >= 13.0:
            responsiveness = "Fluid Responsive (High Likelihood)"
            clinical_guidance = "Patient is operating on the steep ascending limb of the Frank-Starling curve. Intravenous fluid expansion is expected to augment cardiac output."
        elif ppv_pct >= 9.0:
            responsiveness = "Inconclusive / Gray Zone (9-12%)"
            clinical_guidance = "Borderline heart-lung interaction. Recommend Passive Leg Raising (PLR) maneuver or end-expiratory occlusion test before fluid loading."
        else:
            responsiveness = "Fluid Non-Responsive (Low Likelihood)"
            clinical_guidance = "Patient is operating on the flat plateau of the Frank-Starling curve. Fluid bolus is unlikely to increase stroke volume and may induce pulmonary edema."

        return {
            "status": "success",
            "hemodynamic_measurements": {
                "pp_max_mmhg": round(pp_max, 1),
                "pp_min_mmhg": round(pp_min, 1),
                "pp_mean_mmhg": round(pp_mean, 1)
            },
            "dynamic_indices": {
                "pulse_pressure_variation_ppv_pct": round(ppv_pct, 1),
                "stroke_volume_variation_svv_pct": svv_pct
            },
            "interpretation": {
                "fluid_responsiveness": responsiveness,
                "clinical_guidance": clinical_guidance,
                "validity_warnings": validity_warnings
            }
        }
