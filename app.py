from flask import Flask, render_template, request

app = Flask(__name__)

# 台データサンプル
machines = [
    {"name": "台A", "big_prob": 1/300, "at_prob": 1/500, "big_payout": 300, "at_payout": 500, "zone_start": 100, "zone_end": 200, "max_game": 800},
    {"name": "台B", "big_prob": 1/250, "at_prob": 1/450, "big_payout": 280, "at_payout": 450, "zone_start": 120, "zone_end": 220, "max_game": 750},
    {"name": "台C", "big_prob": 1/350, "at_prob": 1/600, "big_payout": 320, "at_payout": 550, "zone_start": 80, "zone_end": 180, "max_game": 900},
]

def calc_ev(machine, current_game, cost_per_game=5):
    remaining_game = max(0, machine["max_game"] - current_game)
    investment = remaining_game * cost_per_game
    zone_bonus = 1.1 if machine["zone_start"] <= current_game <= machine["zone_end"] else 1.0
    expected_big = machine["big_prob"] * zone_bonus * machine["big_payout"]
    expected_at = machine["at_prob"] * zone_bonus * machine["at_payout"]
    expected_return = expected_big + expected_at
    ev = expected_return - investment
    return {"name": machine["name"], "ev": ev, "investment": investment, "return": expected_return}

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        for machine in machines:
            current_game = int(request.form.get(machine["name"], 0))
            results.append(calc_ev(machine, current_game))
        results.sort(key=lambda x: x["ev"], reverse=True)
        results = results[:10]  # トップ10
    return render_template("index.html", machines=machines, results=results)

if __name__ == "__main__":
    app.run(debug=True)
