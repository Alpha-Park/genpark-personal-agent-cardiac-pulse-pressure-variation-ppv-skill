---
name: genpark-personal-agent-cardiac-pulse-pressure-variation-ppv-skill
version: 1.0.0
description: Calculates Pulse Pressure Variation (PPV%) and Stroke Volume Variation (SVV%) to predict fluid responsiveness under mechanical ventilation.
authors:
  - GenPark Ecosystem
tags:
  - personal-agent
  - cardiology
  - hemodynamics
  - ppv
  - svv
  - fluid-responsiveness
  - zero-dependency
---

# Cardiac Pulse Pressure Variation (PPV) Skill

## Mathematical Formulation

Pulse pressure calculation across positive pressure respiratory cycle:

$$\text{PP}_{\max} = \text{SBP}_{\max} - \text{DBP}_{\max}$$
$$\text{PP}_{\min} = \text{SBP}_{\min} - \text{DBP}_{\min}$$
$$\text{PP}_{\text{mean}} = \frac{\text{PP}_{\max} + \text{PP}_{\min}}{2}$$

Pulse Pressure Variation ($\text{PPV}\%$):

$$\text{PPV} \, (\%) = 100 \times \frac{\text{PP}_{\max} - \text{PP}_{\min}}{\text{PP}_{\text{mean}}}$$

Stroke Volume Variation ($\text{SVV}\%$):

$$\text{SVV} \, (\%) = 100 \times \frac{\text{SV}_{\max} - \text{SV}_{\min}}{(\text{SV}_{\max} + \text{SV}_{\min}) / 2}$$

## Clinical Decision Criteria (Michard Criteria)
- **$\text{PPV} \ge 13\%$**: Fluid Responsive (High probability of $\ge 15\%$ increase in stroke volume / cardiac output).
- **$9\% \le \text{PPV} < 13\%$**: Gray Zone (Passive leg raising or end-expiratory occlusion test warranted).
- **$\text{PPV} < 9\%$**: Fluid Non-Responsive (Preload plateau; fluid loading confers risk of congestion without hemodynamic benefit).
