from flask import Flask, request, jsonify
import bisect

app = Flask(__name__)

# Datos conocidos del diagrama P-v (solo para T > 30°C → P >= 3.0 MPa)
saturation_data = [
    {"pressure": 3.0, "v_l": 0.00108, "v_v": 0.0745},
    {"pressure": 5.0, "v_l": 0.00115, "v_v": 0.0713},
    {"pressure": 7.5, "v_l": 0.00123, "v_v": 0.0660},
    {"pressure": 10.0, "v_l": 0.0035,  "v_v": 0.0035},  # Punto crítico
]

def interpolate(pressure):
    for i in range(len(saturation_data) - 1):
        p1 = saturation_data[i]["pressure"]
        p2 = saturation_data[i + 1]["pressure"]

        if p1 <= pressure <= p2:
            # Interpolación lineal
            ratio = (pressure - p1) / (p2 - p1)
            v_l = saturation_data[i]["v_l"] + ratio * (saturation_data[i + 1]["v_l"] - saturation_data[i]["v_l"])
            v_v = saturation_data[i]["v_v"] + ratio * (saturation_data[i + 1]["v_v"] - saturation_data[i]["v_v"])
            return round(v_l, 5), round(v_v, 5)
    return None, None

@app.route("/phase-change-diagram-v1", methods=["GET"])
def get_phase_change():
    try:
        pressure = float(request.args.get("pressure"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid pressure parameter"}), 400

    if pressure < 3.0 or pressure > 10.0:
        return jsonify({"error": "Pressure must be between 3.0 and 10.0 MPa"}), 400

    # Revisa si es un valor exacto
    for entry in saturation_data:
        if pressure == entry["pressure"]:
            return jsonify({
                "specific_volume_liquid": entry["v_l"],
                "specific_volume_vapor": entry["v_v"]
            })

    # Interpolación
    v_l, v_v = interpolate(pressure)
    if v_l is not None:
        return jsonify({
            "specific_volume_liquid": v_l,
            "specific_volume_vapor": v_v
        })

    return jsonify({"error": "Could not interpolate value"}), 500


def handle_phase_change_request(pressure):
    critical_pressure = 10 # MPa
    vc = 0.0035 # m³/kg (critical specific volume)
    saturated_vapor_volume = 0.05 # m³/kg (from the "saturated vapor line" note)

    if pressure == critical_pressure:
        return {
            "specific_volume_liquid": vc,
            "specific_volume_vapor": vc
        }
    elif pressure < critical_pressure:
        return {
            "specific_volume_liquid": vc, # Assumed constant near critical point
            "specific_volume_vapor": saturated_vapor_volume # From the "0.05" clue
        }
    else:
        # Handle invalid pressure (optional)
        return {"error": "Invalid pressure"}


@app.route("/phase-change-diagram-v2", methods=["GET"])
def get_phase_change_v2():
    try:
        pressure = float(request.args.get("pressure"))
        return handle_phase_change_request(pressure)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid pressure parameter"}), 400


SATURATION_TABLE = [
    # (0.005, 0.00105, 30.0),
    # (0.01, 0.0010, 15.5),
    # (0.1, 0.0010, 1.672),
    # (0.5, 0.0011, 0.328),
    # (1.0, 0.0011, 0.194),
    # (2.0, 0.0012, 0.125),
    # (4.0, 0.0013, 0.078),
    # (6.0, 0.0014, 0.055),
    # (8.0, 0.0015, 0.045),
    # (9.75, 0.00155, 0.0035),  # Punto cercano al critico
    # (10.0, 0.00155, 0.0035),  # Punto asumido como el critico

    (0.05	, 0.00105,	30.00),
    (0.1	, 0.00108,	27.12),
    (0.6	, 0.00139,	21.35),
    (1.2	, 0.00171,	15.58),
    (1.8	, 0.00202,	9.81),
    (2.4	, 0.00234,	4.04),
    (3	    , 0.00265,	3.27),
    (4	    , 0.00297,	2.5),
    (6	    , 0.00328,	1.73),
    (8	    , 0.0036,	0.96),
    (10	    , 0.0035,	0.0035)
]

def interpolate_v2(pressure: float):
    """interpolate_v2"""
    pressures = [p[0] for p in SATURATION_TABLE]

    if pressure <= pressures[0]:
        return SATURATION_TABLE[0][1], SATURATION_TABLE[0][2]
    if pressure >= pressures[-1]:
        return SATURATION_TABLE[-1][1], SATURATION_TABLE[-1][2]

    idx = bisect.bisect_left(pressures, pressure)
    p1, v1_l, v1_v = SATURATION_TABLE[idx - 1]
    p2, v2_l, v2_v = SATURATION_TABLE[idx]

    factor = (pressure - p1) / (p2 - p1)
    v_l = v1_l + factor * (v2_l - v1_l)
    v_v = v1_v + factor * (v2_v - v1_v)

    return v_l, v_v

@app.route("/phase-change-diagram", methods=["GET"])
def get_phase_change_v3():
    try:
        pressure = float(request.args.get("pressure"))
        v_l, v_v = interpolate_v2(pressure)
        return {
            "specific_volume_liquid": round(v_l, 5),
            "specific_volume_vapor": round(v_v, 5)
        }
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid pressure parameter"}), 400


if __name__ == "__main__":
    app.run(debug=False, port=5001)