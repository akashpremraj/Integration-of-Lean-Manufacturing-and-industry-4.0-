from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

out = Path(__file__).resolve().parents[1] / "data-samples"
out.mkdir(parents=True, exist_ok=True)

start = datetime(2023, 7, 1)
rows, lines = [], ["BodyShop", "Assembly"]

for i in range(90):
    day = start + timedelta(days=i)
    for line in lines:
        planned = 8*60
        changeover = 20 if line == "Assembly" else 15
        downtime = 40 if line == "BodyShop" else 50
        run = planned - changeover - downtime
        ideal_rate = 0.8 if line == "Assembly" else 0.5
        total = int(run * ideal_rate * (0.95 + 0.1*(i%7)/6))
        scrap = int(total * (0.03 if line=="BodyShop" else 0.02))
        rows.append({
            "date": day.date().isoformat(),
            "line": line,
            "planned_time_min": planned,
            "run_time_min": run,
            "downtime_min": downtime,
            "good_units": total - scrap,
            "scrap_units": scrap,
            "changeover_min": changeover,
            "energy_kwh": round(400 + (50 if line=="BodyShop" else 35) + (i%10)*2, 1),
            "maint_cost_gbp": round(30 + (5 if line=="BodyShop" else 8) + (i%5), 2)
        })

pd.DataFrame(rows).to_csv(out/"line_production.csv", index=False)
print("Created data-samples/line_production.csv")
