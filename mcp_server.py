"""
MCP Server for Cardiac Pulse Pressure Variation (PPV) Skill.
Provides standard Model Context Protocol JSON-RPC tool endpoints.
"""

import sys
import json
from client import PulsePressureVariationClient


def main():
    client = PulsePressureVariationClient()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "evaluate_respiratory_variations",
                            "description": "Calculates Pulse Pressure Variation (PPV%) and Stroke Volume Variation (SVV%) to predict fluid responsiveness under mechanical ventilation.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "sbp_max_mmhg": {
                                        "type": "number",
                                        "description": "Maximal systolic arterial pressure during respiratory cycle (mmHg)."
                                    },
                                    "dbp_max_mmhg": {
                                        "type": "number",
                                        "description": "Diastolic pressure corresponding to maximal systolic beat (mmHg)."
                                    },
                                    "sbp_min_mmhg": {
                                        "type": "number",
                                        "description": "Minimal systolic arterial pressure during respiratory cycle (mmHg)."
                                    },
                                    "dbp_min_mmhg": {
                                        "type": "number",
                                        "description": "Diastolic pressure corresponding to minimal systolic beat (mmHg)."
                                    },
                                    "sv_max_ml": {
                                        "type": "number",
                                        "description": "Maximal stroke volume in mL (optional)."
                                    },
                                    "sv_min_ml": {
                                        "type": "number",
                                        "description": "Minimal stroke volume in mL (optional)."
                                    },
                                    "tidal_volume_ml_kg_pbw": {
                                        "type": "number",
                                        "description": "Ventilator tidal volume in mL/kg predicted body weight (default: 8.0)."
                                    },
                                    "heart_rhythm_regular": {
                                        "type": "boolean",
                                        "description": "Whether cardiac rhythm is regular sinus rhythm (default: true)."
                                    }
                                },
                                "required": [
                                    "sbp_max_mmhg",
                                    "dbp_max_mmhg",
                                    "sbp_min_mmhg",
                                    "dbp_min_mmhg"
                                ]
                            }
                        }
                    ]
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})

            if name == "evaluate_respiratory_variations":
                try:
                    out = client.evaluate_respiratory_variations(**args)
                    res = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(out, indent=2)}]
                        }
                    }
                except Exception as e:
                    res = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "isError": True,
                        "error": {"code": -32000, "message": str(e)}
                    }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()
