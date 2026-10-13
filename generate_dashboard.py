#!/usr/bin/env python3
"""Construit le tableau de bord musculation sans service externe."""

from __future__ import annotations

import argparse
import ast
from datetime import date, timedelta
from html import escape
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PROGRAM_PATH = ROOT / "programme_muscu.md"
SETTINGS_PATH = ROOT / "data" / "settings.json"
LOG_PATH = ROOT / "data" / "seances.json"
OUTPUT_PATH = ROOT / "docs" / "index.html"
REPO_FULL_NAME = "alexananasa/coach-ia"

JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
JOURS_COURTS = ("lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim.")
MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre")
EQUIPEMENT_PDC = ("lest", "barres parallèles")
PAS_MATERIEL = (
    ("barre", 2.5), ("haltère", 2.0), ("machine", 2.5),
    ("poulie", 2.5), ("lest", 2.5),
)
POIDS_BARRE = 20.0

CSS = """
:root{color-scheme:light;--ink:#192a24;--muted:#68766f;--line:#e1e8e3;--paper:#f4f7f4;--card:#fff;--green:#176b50;--green2:#dff2e9;--lime:#c8eb78;--orange:#f4a943;--red:#b9483c}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--green)}.wrap{max-width:1180px;margin:0 auto;padding:28px 24px 64px}
.hero{position:relative;overflow:hidden;border-radius:26px;background:linear-gradient(120deg,#123c30,#1d6b51 62%,#2e805f);color:#fff;padding:34px 38px;margin-bottom:22px}
.hero:after{content:"";position:absolute;width:320px;height:320px;border:1px solid #ffffff24;border-radius:50%;right:-70px;top:-160px;box-shadow:0 0 0 35px #ffffff0a,0 0 0 72px #ffffff08}
.eyebrow,.kicker{text-transform:uppercase;letter-spacing:.12em;font-size:.72rem;font-weight:750;color:#c7ebd9;margin:0 0 8px}
h1{font-size:clamp(2rem,4vw,3.1rem);line-height:1.08;letter-spacing:-.04em;margin:0}
.hero p.sub{max-width:650px;margin:13px 0 0;color:#e0eee7}.hero-meta{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px;position:relative;z-index:1}
.pill{display:inline-flex;align-items:center;border:1px solid #ffffff4d;border-radius:999px;padding:6px 11px;font-size:.78rem;color:#fff;background:#ffffff12}
.topline{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;position:relative;z-index:1}
.state{background:var(--lime);color:#18392b;border:0;font-weight:800}
.nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 20px}
.nav a{background:#fff;border:1px solid var(--line);padding:8px 13px;border-radius:999px;text-decoration:none;font-size:.84rem;color:var(--ink)}
.nav a:hover{border-color:#8ab89f}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:18px}
.card,.kpi{background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:0 4px 16px #18352a08}
.kpi{padding:17px 18px}.kpi .label{font-size:.78rem;color:var(--muted);font-weight:650}.kpi strong{display:block;font-size:1.45rem;margin-top:5px;letter-spacing:-.03em}
.section{margin-top:26px}.section-head{display:flex;align-items:end;justify-content:space-between;gap:20px;margin:0 2px 12px}
h2{font-size:1.35rem;letter-spacing:-.025em;margin:0}.section-head p{margin:4px 0 0;color:var(--muted);font-size:.9rem}
.today{padding:22px;display:grid;grid-template-columns:minmax(210px,.7fr) 1.3fr;gap:22px;background:linear-gradient(135deg,#fff,#f7fcf8)}
.today-side{border-right:1px solid var(--line);padding-right:18px}.today-date{font-size:1.4rem;font-weight:800;letter-spacing:-.03em}.today-label{color:var(--muted);font-size:.88rem}.phase{display:inline-block;margin-top:12px;padding:5px 9px;border-radius:8px;background:var(--green2);color:#155b43;font-weight:750;font-size:.78rem}
.exercise-list{display:grid;gap:9px}.exercise{padding:13px 14px;border:1px solid var(--line);border-radius:13px;background:#fff}
.exercise-top{display:flex;justify-content:space-between;gap:12px;align-items:start}.exercise-name{font-weight:800}.load{font-weight:800;color:var(--green);text-align:right;white-space:nowrap}
.exercise-meta{display:flex;gap:7px;flex-wrap:wrap;margin-top:8px}.tag{display:inline-flex;background:#f1f5f2;border-radius:7px;padding:3px 7px;font-size:.75rem;color:#52635a}
.muted{color:var(--muted)}
details.tech{margin-top:8px;color:#52635a;font-size:.82rem}details.tech summary{cursor:pointer;color:var(--green);font-weight:700}details.tech p{margin:6px 0}.tech b{color:var(--ink)}
.week-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px}
.day{background:#fff;border:1px solid var(--line);border-radius:13px;padding:12px;min-height:104px}.day.today-day{border-color:var(--green);box-shadow:0 0 0 2px #176b5015}.day .date{font-size:.74rem;color:var(--muted)}.day strong{display:block;margin-top:7px;font-size:.87rem}.day small{display:block;color:var(--muted);margin-top:4px}
.volume{padding:20px;display:grid;gap:12px}.volume-row{display:grid;grid-template-columns:140px 1fr 38px;align-items:center;gap:12px;font-size:.87rem}.bar{height:10px;border-radius:999px;background:#edf2ee;overflow:hidden}.bar span{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#2d8c68,#9ccd67)}
.programme-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}
.session-card{padding:18px}.session-head{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:12px}.session-head h3{margin:0;font-size:1.08rem}.session-head span{font-size:.78rem;color:var(--muted)}
.projection{padding:18px;overflow-x:auto}.projection table{width:100%;border-collapse:collapse;min-width:720px}.projection th,.projection td{text-align:left;padding:10px 9px;border-bottom:1px solid var(--line);font-size:.84rem}.projection th{font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted)}.projection td strong{color:var(--green)}
.spark{display:flex;align-items:end;height:30px;gap:3px;min-width:90px}.spark i{display:block;flex:1;min-width:5px;background:#80bca0;border-radius:3px 3px 1px 1px}.spark i:last-child{background:var(--green)}
.chart-card{padding:18px;overflow:hidden}.chart-card h3{font-size:1rem;margin:0}.chart-note{font-size:.83rem;color:var(--muted);margin:6px 0 14px}.chart-svg{display:block;width:100%;height:auto;overflow:visible}.chart-gridline{stroke:#e8eeea;stroke-width:1}.chart-axis{fill:#718078;font:11px ui-monospace,monospace}.chart-legend{display:flex;gap:10px 16px;flex-wrap:wrap;margin-top:12px;color:var(--muted);font-size:.78rem}.chart-legend span{display:inline-flex;align-items:center;gap:6px}.chart-legend i{width:9px;height:9px;border-radius:50%;display:inline-block}.chart-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.projection-card{padding:16px;min-width:0}.projection-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.projection-head h3{font-size:.96rem;margin:0}.projection-context{font-size:.77rem;color:var(--muted);text-align:right}.projection-foot{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:.79rem;color:var(--muted);margin-top:4px}.projection-foot strong{color:var(--green)}
.heatmap-wrap{overflow-x:auto}.heatmap{display:grid;grid-template-columns:52px repeat(7,minmax(22px,1fr));gap:5px;min-width:320px}.heat-week{font-size:.67rem;color:var(--muted);display:flex;align-items:center}.heat-day-label{font-size:.64rem;text-align:center;color:var(--muted)}.heat-cell{height:24px;border-radius:6px;background:#edf2ee;border:1px solid transparent}.heat-cell.done{background:#72bf98}.heat-cell.short{background:#f4b34e}.heat-cell.absent{background:#cad2cc}.heat-cell.future{background:#eaf1ed;border:1px dashed #aac0b2}.heat-cell.rest{background:#f6f8f6}.heat-legend{display:flex;gap:10px 16px;flex-wrap:wrap;margin-top:12px;font-size:.75rem;color:var(--muted)}.heat-legend span{display:inline-flex;align-items:center;gap:6px}.heat-legend i{width:10px;height:10px;border-radius:3px;display:inline-block}.history-empty{padding:15px;border-radius:12px;background:#f4f7f4;color:var(--muted);font-size:.85rem}.history-item{margin-top:12px}.history-item h4{font-size:.88rem;margin:0 0 4px}.metric-line{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}.metric-chip{background:#eff5f0;border-radius:8px;padding:5px 8px;font-size:.77rem;color:#52635a}
.callout{padding:16px 18px;border-radius:14px;background:#fff8e9;border:1px solid #f1dfbd;color:#684c20;font-size:.88rem}
.log-panel{padding:20px}.log-panel p{margin-top:0;color:var(--muted)}.button{display:inline-flex;background:var(--green);color:white;text-decoration:none;padding:10px 14px;border-radius:10px;font-weight:750;font-size:.86rem}.button:hover{background:#0f563f}
pre{white-space:pre-wrap;overflow:auto;background:#f5f7f5;border:1px solid var(--line);padding:13px;border-radius:10px;font-size:.78rem;color:#3b4b42}
footer{margin-top:28px;color:var(--muted);font-size:.78rem;text-align:center}
@media(max-width:850px){.kpis{grid-template-columns:repeat(2,1fr)}.week-grid{grid-template-columns:repeat(4,1fr)}.today{grid-template-columns:1fr}.today-side{border-right:0;border-bottom:1px solid var(--line);padding:0 0 14px}.programme-grid,.chart-grid{grid-template-columns:1fr}}
@media(max-width:520px){.wrap{padding:15px 13px 44px}.hero{padding:25px 20px;border-radius:20px}.topline{display:block}.hero .state{margin-top:14px}.kpis{gap:8px}.kpi{padding:13px}.kpi strong{font-size:1.15rem}.week-grid{grid-template-columns:repeat(2,1fr)}.volume-row{grid-template-columns:95px 1fr 28px;gap:8px}.section-head{display:block}}
"""


def _literal_block(text: str, name: str):
    """Lit une valeur littérale Python sans jamais exécuter le contenu du document."""
    match = re.search(rf"^{re.escape(name)}\s*=\s*", text, re.MULTILINE)
    if not match:
        return None
    start, i = match.start(), match.end()
    depth = 0
    opened = False
    quote = None
    escaped = False
    comment = False
    while i < len(text):
        char = text[i]
        if comment:
            if char == "\n":
                comment = False
            i += 1
            continue
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            i += 1
            continue
        if char == "#":
            comment = True
        elif char in ("'", '"'):
            quote = char
        elif char in "{[(":
            depth += 1
            opened = True
        elif char in "}])":
            depth -= 1
            if opened and depth == 0:
                return ast.literal_eval(text[match.end():i + 1].strip())
        elif not opened and char == "\n":
            return ast.literal_eval(text[match.end():i].strip())
        i += 1
    raise ValueError(f"Bloc {name} incomplet dans {PROGRAM_PATH.name}")


def load_program():
    text = PROGRAM_PATH.read_text(encoding="utf-8")
    names = (
        "PROGRAMME", "CYCLE_RIR", "SEMAINE_DECHARGE", "FACTEUR_DECHARGE",
        "MAXES", "MACHINES", "TARES", "PAS", "ORDRE_MUSCLES", "MUSCLES",
        "TECHNIQUE",
    )
    raw = {name: _literal_block(text, name) for name in names}
    days = {}
    for day_name, session in (raw["PROGRAMME"] or {}).items():
        day_index = JOURS.index(day_name.lower())
        exercises = []
        for source in session.get("exercices", []):
            reps = source.get("reps", (8, 12))
            exercises.append({
                "nom": str(source["nom"]),
                "materiel": str(source.get("materiel", "")),
                "series": int(source.get("series", 3)),
                "lo": int(reps[0]),
                "hi": int(reps[1]),
                "unilat": "par jambe" if source.get("par_jambe") else (
                    "par bras" if source.get("par_bras") else ""),
                "repos": str(source.get("repos", "")),
            })
        days[day_index] = {
            "jour": day_name.lower(),
            "nom": str(session.get("nom", day_name.title())),
            "exercices": exercises,
        }
    return {
        "programme": days,
        "rir": {int(k): int(v) for k, v in (raw["CYCLE_RIR"] or {}).items()},
        "deload_week": int(raw["SEMAINE_DECHARGE"]),
        "deload_factor": float(raw["FACTEUR_DECHARGE"]),
        "maxes": raw["MAXES"] or {},
        "machines": raw["MACHINES"] or {},
        "tares": raw["TARES"] or {},
        "pas": raw["PAS"] or {},
        "ordre_muscles": raw["ORDRE_MUSCLES"] or [],
        "muscles": raw["MUSCLES"] or {},
        "technique": raw["TECHNIQUE"] or {},
    }


def load_settings():
    defaults = {
        "cycle_anchor": "2026-10-12",
        "bodyweight_kg": 72.0,
        "bodyweight_reference_kg": 71.7,
        "journal_keep_days": 180,
        "max_gain_per_cycle": 0.05,
        "max_cycles_per_step": 4,
        "machine_addon_kg": 2.3,
        "machine_addons_max": 2,
    }
    if SETTINGS_PATH.exists():
        defaults.update(json.loads(SETTINGS_PATH.read_text(encoding="utf-8")))
    anchor = date.fromisoformat(defaults["cycle_anchor"])
    if anchor.weekday() != 0:
        raise ValueError("cycle_anchor doit être un lundi (format AAAA-MM-JJ).")
    return defaults, anchor


def read_log():
    if not LOG_PATH.exists():
        return {"_lisez_moi": [], "seances": []}
    data = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("seances"), list):
        raise ValueError("data/seances.json doit contenir un objet avec une liste seances.")
    return data


def cycle_week(day: date, anchor: date, block_len: int):
    monday = day - timedelta(days=day.weekday())
    if monday < anchor:
        return None
    elapsed_weeks = (monday - anchor).days // 7
    return elapsed_weeks % block_len + 1


def cycle_index(day: date, anchor: date, block_len: int):
    monday = day - timedelta(days=day.weekday())
    if monday < anchor:
        return None
    return (monday - anchor).days // (7 * block_len)


def sets_for_week(base_sets: int, week: int, deload_week: int, deload_factor: float):
    if week != deload_week:
        return base_sets
    return max(1, math.ceil(base_sets * deload_factor))


def reps_for_week(lo: int, hi: int, sets: int, week: int, deload_week: int):
    if week == deload_week:
        return [lo] * sets
    step = max(0, week - 1)
    first = min(lo + 1 + step, hi)
    rest = min(lo + step, hi)
    return [first] + [rest] * (sets - 1)


def material_increment(material: str, exercise: str, program):
    specific = program["pas"].get(exercise)
    if specific:
        return float(specific)
    normalized = material.casefold()
    for key, step in PAS_MATERIEL:
        if key in normalized:
            return step
    return 1.0


def machine_stack(exercise: str, program, settings):
    raw = program["machines"].get(exercise) or []
    notches = sorted({float(value) for value in raw if isinstance(value, (int, float))})
    if len(notches) < 2:
        return notches
    min_gap = min(b - a for a, b in zip(notches, notches[1:]))
    addon = float(settings["machine_addon_kg"])
    if min_gap <= addon:
        return notches
    additions = {
        round(weight + count * addon, 1)
        for weight in notches
        for count in range(1, int(settings["machine_addons_max"]) + 1)
    }
    return sorted(weight for weight in set(notches) | additions if weight <= notches[-1])


def round_load(weight: float, material: str, exercise: str, bodyweight: float,
               program, settings):
    if weight is None:
        return None
    stack = machine_stack(exercise, program, settings)
    if stack:
        return min(stack, key=lambda value: (abs(value - weight), value))
    step = material_increment(material, exercise, program)
    normalized = material.casefold()
    if any(key in normalized for key in EQUIPEMENT_PDC):
        added = round((weight - bodyweight) / step) * step
        return round(bodyweight + added, 2)
    tare = float(program["tares"].get(exercise, 0) or 0)
    if tare:
        discs = max(0.0, round((weight - tare) / step) * step)
        return round(tare + discs, 2)
    rounded = max(step, round(weight / step) * step)
    if normalized.strip() == "barre":
        return max(POIDS_BARRE, rounded)
    return rounded


def step_cost(step: float, base: float, settings):
    if not base or not step or step <= 0:
        return 1
    cap = float(settings["max_gain_per_cycle"]) * base
    return max(1, min(int(settings["max_cycles_per_step"]), math.ceil(step / cap)))


def load_after_cycles(base: float, material: str, exercise: str, earned: int,
                      program, settings):
    if not base or earned <= 0:
        return base
    stack = machine_stack(exercise, program, settings)
    if stack:
        index = min(range(len(stack)), key=lambda i: abs(stack[i] - base))
        remaining = earned
        while index + 1 < len(stack):
            cost = step_cost(round(stack[index + 1] - stack[index], 2), stack[index], settings)
            if remaining < cost:
                break
            remaining -= cost
            index += 1
        return float(stack[index])
    step = material_increment(material, exercise, program)
    weight = base
    remaining = earned
    while True:
        cost = step_cost(step, weight, settings)
        if remaining < cost:
            return round(weight, 2)
        remaining -= cost
        weight += step


def bodyweight_offset(material: str, settings):
    if any(key in material.casefold() for key in EQUIPEMENT_PDC):
        return float(settings["bodyweight_kg"]) - float(settings["bodyweight_reference_kg"])
    return 0.0


def working_weight(exercise: dict, earned: int, program, settings, rir_week_one: int):
    max_value = program["maxes"].get(exercise["nom"])
    if not isinstance(max_value, (int, float)) or max_value <= 0:
        return None
    # Approximation Epley : la charge correspond au bas de la fourchette
    # avec le RIR de la première semaine du cycle.
    reps_at_effort = exercise["lo"] + rir_week_one
    fraction = 1 / (1 + reps_at_effort / 30)
    raw = float(max_value) * fraction + bodyweight_offset(exercise["materiel"], settings)
    start = round_load(raw, exercise["materiel"], exercise["nom"],
                       float(settings["bodyweight_kg"]), program, settings)
    return load_after_cycles(start, exercise["materiel"], exercise["nom"],
                             earned, program, settings)


def display_load(weight, material, exercise, settings, program):
    if weight is None:
        return "charge à renseigner"
    bodyweight = float(settings["bodyweight_kg"])
    if any(key in material.casefold() for key in EQUIPEMENT_PDC):
        delta = weight - bodyweight
        step = material_increment(material, exercise, program)
        if abs(delta) < step:
            return "poids de corps"
        extra = round(abs(delta) / step) * step
        label = "corps +" if delta > 0 else "corps −"
        return f"{label} {fmt_number(extra)} kg" + ("" if delta > 0 else " (assisté)")
    tare = float(program["tares"].get(exercise, 0) or 0)
    if tare:
        discs = round(weight - tare, 2)
        return f"{fmt_number(discs)} kg de disques · {fmt_number(weight)} kg total"
    return f"{fmt_number(weight)} kg"


def fmt_number(value):
    if value is None:
        return "—"
    text = f"{float(value):.1f}"
    if text.endswith(".0"):
        text = text[:-2]
    return text.replace(".", ",")


def compute_credits(log, program, today, anchor, block_len):
    monday = today - timedelta(days=today.weekday())
    cycles_done = 0 if monday < anchor else (monday - anchor).days // (7 * block_len)
    missed = {}
    for entry in log.get("seances", []):
        try:
            day = date.fromisoformat(str(entry.get("date", ""))[:10])
        except ValueError:
            continue
        index = cycle_index(day, anchor, block_len)
        if index is None or index >= cycles_done:
            continue
        if entry.get("absent"):
            names = [ex["nom"] for ex in program["programme"].get(day.weekday(), {}).get("exercices", [])]
            for name in names:
                missed.setdefault(name, set()).add(index)
            continue
        for item in entry.get("exercices", []):
            reps = item.get("reps") or []
            target = item.get("prescrit_reps") or []
            if not isinstance(reps, list) or not reps or not isinstance(target, list) or not target:
                continue
            try:
                actual = [int(value) for value in reps]
                prescribed = [int(value) for value in target]
            except (TypeError, ValueError):
                continue
            short = len(actual) != len(prescribed) or any(a < p for a, p in zip(actual, prescribed))
            if short:
                name = str(item.get("nom") or "").strip()
                if name:
                    missed.setdefault(name, set()).add(index)
    result = {}
    for day_program in program["programme"].values():
        for ex in day_program["exercices"]:
            name = ex["nom"]
            result[name] = max(0, cycles_done - len(missed.get(name, set())))
    return result


def build_entry(day, week, session, earned, program, settings):
    items = []
    rir = program["rir"].get(week, 2)
    for ex in session["exercices"]:
        shown_sets = sets_for_week(ex["series"], week, program["deload_week"], program["deload_factor"])
        target = reps_for_week(ex["lo"], ex["hi"], shown_sets, week, program["deload_week"])
        load = working_weight(ex, earned.get(ex["nom"], 0), program, settings,
                              program["rir"].get(1, 3))
        items.append({
            "nom": ex["nom"],
            "prescrit_reps": target,
            "prescrit": "/".join(str(value) for value in target),
            "charge_prescrite": round(load, 2) if load is not None else None,
            "reps": [],
            "charge": None,
        })
    return {
        "date": day.isoformat(),
        "seance": session["nom"],
        "semaine_cycle": week,
        "rir": rir,
        "exercices": items,
    }


def ensure_session_log(log, today, anchor, program, settings, earned):
    sessions = {str(entry.get("date")): entry for entry in log.get("seances", []) if isinstance(entry, dict)}
    keep_days = int(settings["journal_keep_days"])
    block_len = max(program["rir"])
    for offset in range(-7, 8):
        day = today + timedelta(days=offset)
        if day < anchor:
            continue
        session = program["programme"].get(day.weekday())
        if session is None:
            continue
        week = cycle_week(day, anchor, block_len)
        if week is None:
            continue
        generated = build_entry(day, week, session, earned, program, settings)
        old = sessions.get(day.isoformat())
        if old is not None:
            existing = {str(item.get("nom")): item for item in old.get("exercices", []) if isinstance(item, dict)}
            for item in generated["exercices"]:
                if item["nom"] in existing:
                    prior = existing[item["nom"]]
                    prior["prescrit_reps"] = item["prescrit_reps"]
                    prior["prescrit"] = item["prescrit"]
                    prior["charge_prescrite"] = item["charge_prescrite"]
                    prior.setdefault("reps", [])
                    prior.setdefault("charge", None)
                else:
                    old.setdefault("exercices", []).append(item)
            old["seance"] = generated["seance"]
            old["semaine_cycle"] = generated["semaine_cycle"]
            old["rir"] = generated["rir"]
        else:
            sessions[day.isoformat()] = generated
    kept = []
    for key, entry in sorted(sessions.items()):
        try:
            day = date.fromisoformat(key[:10])
        except ValueError:
            continue
        if (today - day).days <= keep_days:
            kept.append(entry)
    output = {
        "_lisez_moi": [
            "Reps vide = prescription atteinte.",
            "Saisis reps si une série est sous la cible.",
            "absent: true empêche de créditer le cycle.",
            "charge est facultative et ne remplace pas la prescription.",
        ],
        "seances": kept,
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    if not LOG_PATH.exists() or LOG_PATH.read_text(encoding="utf-8") != serialized:
        LOG_PATH.write_text(serialized, encoding="utf-8")
    return output


def weekly_sets(program, week):
    counts = {}
    total = 0
    for session in program["programme"].values():
        for ex in session["exercices"]:
            shown = sets_for_week(ex["series"], week, program["deload_week"], program["deload_factor"])
            group = program["muscles"].get(ex["nom"], "autres")
            counts[group] = counts.get(group, 0) + shown
            total += shown
    return counts, total


def session_data(session, week, earned, program, settings):
    result = []
    rir = program["rir"].get(week, 2)
    for ex in session["exercices"]:
        series = sets_for_week(ex["series"], week, program["deload_week"], program["deload_factor"])
        reps = reps_for_week(ex["lo"], ex["hi"], series, week, program["deload_week"])
        weight = working_weight(ex, earned.get(ex["nom"], 0), program, settings,
                                program["rir"].get(1, 3))
        result.append({
            **ex, "series_affichees": series, "reps_affichees": reps,
            "poids": weight, "poids_texte": display_load(
                weight, ex["materiel"], ex["nom"], settings, program),
            "rir": rir,
            "technique": program["technique"].get(ex["nom"], {}),
        })
    return result


def next_session(today, anchor, program):
    for offset in range(8):
        day = today + timedelta(days=offset)
        if day >= anchor and day.weekday() in program["programme"]:
            return day, program["programme"][day.weekday()]
    return None, None


def date_fr(day):
    return f"{JOURS[day.weekday()].capitalize()} {day.day} {MOIS[day.month - 1]} {day.year}"


def date_short(day):
    return f"{JOURS_COURTS[day.weekday()]} {day.day}"


def session_card(day, session, entries, today=None, compact=False):
    total_sets = sum(item["series_affichees"] for item in entries)
    rows = []
    for item in entries:
        tags = [
            f'{item["series_affichees"]} séries',
            f'{"/".join(str(value) for value in item["reps_affichees"])} reps' + (f' · {item["unilat"]}' if item["unilat"] else ""),
            f'RIR {item["rir"]}',
            item["materiel"],
        ]
        if item["repos"]:
            tags.append("repos " + item["repos"])
        technique = item["technique"]
        tech_html = ""
        if technique:
            pieces = []
            for key, label in (("reglages", "Réglages"), ("execution", "Exécution"), ("erreurs", "À surveiller")):
                value = technique.get(key)
                if value:
                    pieces.append(f'<p><b>{label} :</b> {escape(str(value))}</p>')
            tech_html = f'<details class="tech"><summary>Technique</summary>{"".join(pieces)}</details>'
        rows.append(
            '<article class="exercise">'
            '<div class="exercise-top">'
            f'<div class="exercise-name">{escape(item["nom"])}</div>'
            f'<div class="load">{escape(item["poids_texte"])}</div>'
            '</div><div class="exercise-meta">'
            + "".join(f'<span class="tag">{escape(tag)}</span>' for tag in tags)
            + f'</div>{tech_html}</article>'
        )
    heading = f'<h3>{escape(session["nom"])}</h3>'
    day_label = date_fr(day) if day else ""
    return (
        '<div class="card session-card">'
        f'<div class="session-head"><div>{heading}<span>{escape(day_label)}</span></div>'
        f'<span>{total_sets} séries</span></div>'
        f'<div class="exercise-list">{"".join(rows)}</div>'
        '</div>'
    )


def render_spark(values):
    if not values:
        return "—"
    lo, hi = min(values), max(values)
    bars = []
    for value in values:
        height = 24 if hi == lo else 8 + round(18 * (value - lo) / (hi - lo))
        bars.append(f'<i style="height:{height}px" title="{fmt_number(value)} kg"></i>')
    return f'<span class="spark" aria-label="Projection de progression">{"".join(bars)}</span>'


def projection_rows(program, settings, earned):
    seen = set()
    rows = []
    for day_index in sorted(program["programme"]):
        session = program["programme"][day_index]
        for ex in session["exercices"]:
            key = (ex["nom"], ex["lo"], ex["hi"], ex["series"])
            if key in seen:
                continue
            seen.add(key)
            current = working_weight(ex, earned.get(ex["nom"], 0), program, settings,
                                     program["rir"].get(1, 3))
            if current is None:
                values = []
            else:
                values = [
                    load_after_cycles(current, ex["materiel"], ex["nom"], i, program, settings)
                    for i in range(7)
                ]
            rows.append((ex, current, values, earned.get(ex["nom"], 0)))
    return rows


def projection_week_points(ex, current, today, anchor, program, settings, cycles=6):
    """Charges par semaine sur six cycles, avec la décharge visible."""
    if current is None:
        return []
    block_len = max(program["rir"])
    week = cycle_week(today, anchor, block_len) or 1
    cycle_start = (today - timedelta(days=today.weekday() + 7 * (week - 1)))
    if today < anchor:
        cycle_start = anchor
    points = []
    for cycle_offset in range(cycles):
        first_week = week if cycle_offset == 0 else 1
        weight = load_after_cycles(current, ex["materiel"], ex["nom"],
                                   cycle_offset, program, settings)
        for week_no in range(first_week, block_len + 1):
            monday = cycle_start + timedelta(days=7 * (cycle_offset * block_len + week_no - 1))
            sets = sets_for_week(ex["series"], week_no,
                                 program["deload_week"], program["deload_factor"])
            reps = reps_for_week(ex["lo"], ex["hi"], sets,
                                 week_no, program["deload_week"])
            points.append({
                "date": monday,
                "cycle": cycle_offset + 1,
                "week": week_no,
                "kg": weight,
                "sets": sets,
                "reps": "/".join(str(value) for value in reps),
                "deload": week_no == program["deload_week"],
            })
    return points


def progression_svg(ex, points, width=620, height=220):
    if not points:
        return '<div class="history-empty">Charge de départ à renseigner dans le programme.</div>'
    left, right, top, bottom = 48, 12, 14, 38
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [float(point["kg"]) for point in points]
    low, high = min(values), max(values)
    if high == low:
        margin = max(1.0, high * 0.04)
    else:
        margin = (high - low) * 0.16
    low, high = low - margin, high + margin
    if high <= low:
        high = low + 1

    def x_at(index):
        return left + (index / max(1, len(points) - 1)) * plot_w

    def y_at(value):
        return top + ((high - value) / (high - low)) * plot_h

    grid = []
    for tick in range(4):
        value = low + (high - low) * tick / 3
        y = y_at(value)
        grid.append(
            f'<line class="chart-gridline" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/>'
            f'<text class="chart-axis" x="{left-7}" y="{y+4:.1f}" text-anchor="end">{fmt_number(value)}</text>'
        )
    spacing = plot_w / max(1, len(points) - 1)
    deloads = []
    for index, point in enumerate(points):
        if point["deload"]:
            x = x_at(index)
            deloads.append(
                f'<rect x="{max(left, x-spacing*.42):.1f}" y="{top}" '
                f'width="{min(spacing*.84, width-right-max(left, x-spacing*.42)):.1f}" '
                f'height="{plot_h}" fill="#f4a943" opacity=".18"><title>Semaine de décharge</title></rect>'
            )
    path = [f'M {x_at(0):.1f} {y_at(values[0]):.1f}']
    for index in range(1, len(points)):
        path.append(f'H {x_at(index):.1f}')
        path.append(f'V {y_at(values[index]):.1f}')
    dots = []
    labels = []
    previous_cycle = None
    for index, point in enumerate(points):
        x, y = x_at(index), y_at(float(point["kg"]))
        date_label = f'{point["date"].day} {MOIS[point["date"].month - 1]}'
        detail = (f'Semaine du {date_label} · {fmt_number(point["kg"])} kg · '
                  f'{point["sets"]} séries · {point["reps"]} reps' +
                  (' · décharge' if point['deload'] else ''))
        dots.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.1" fill="{"#f4a943" if point["deload"] else "#176b50"}">'
            f'<title>{escape(detail)}</title></circle>'
        )
        if point["cycle"] != previous_cycle:
            labels.append(
                f'<text class="chart-axis" x="{x:.1f}" y="{height-10}" text-anchor="middle">C{point["cycle"]}</text>'
            )
            previous_cycle = point["cycle"]
    aria = escape(f'Projection de charge pour {ex["nom"]}, sur six cycles')
    return (
        f'<svg class="chart-svg" viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">'
        f'<title>{aria}</title>'
        + ''.join(deloads) + ''.join(grid)
        + f'<path d="{" ".join(path)}" fill="none" stroke="#176b50" stroke-width="2.5" stroke-linejoin="round"/>'
        + ''.join(dots) + ''.join(labels)
        + '</svg>'
    )


def volume_cycle_chart(program):
    block_len = max(program["rir"])
    palette = ("#176b50", "#4589c8", "#c77e25", "#8a5ab7", "#c75454", "#4a9e9a", "#87943b")
    order = program["ordre_muscles"] + [
        name for name in program["muscles"].values() if name not in program["ordre_muscles"]
    ]
    groups = list(dict.fromkeys(order))
    series = {group: [] for group in groups}
    for week in range(1, block_len + 1):
        values, _ = weekly_sets(program, week)
        for group in groups:
            series[group].append(values.get(group, 0))
    active = [group for group in groups if any(series[group])]
    max_value = max((value for group in active for value in series[group]), default=1)
    max_value = max(4, math.ceil(max_value / 4) * 4)
    width, height = 720, 270
    left, right, top, bottom = 44, 18, 16, 42
    plot_w, plot_h = width - left - right, height - top - bottom

    def x_at(index):
        return left + (index / max(1, block_len - 1)) * plot_w

    def y_at(value):
        return top + (1 - value / max_value) * plot_h

    grid = []
    for tick in range(5):
        value = max_value * tick / 4
        y = y_at(value)
        grid.append(
            f'<line class="chart-gridline" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/>'
            f'<text class="chart-axis" x="{left-8}" y="{y+4:.1f}" text-anchor="end">{value:g}</text>'
        )
    paths, dots, legend = [], [], []
    dash_styles = ("", "7 4", "2 4", "9 3 2 3", "4 3", "1 3", "11 4")
    for index, group in enumerate(active):
        color = palette[index % len(palette)]
        values = series[group]
        coords = [(x_at(i), y_at(value)) for i, value in enumerate(values)]
        dash = dash_styles[index % len(dash_styles)]
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        paths.append(
            f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in coords)}" '
            f'fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"{dash_attr}/>'
        )
        for i, ((x, y), value) in enumerate(zip(coords, values)):
            dots.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}">'
                f'<title>{escape(group.capitalize())} · semaine {i+1} · {value} séries</title></circle>'
            )
        legend.append(f'<span><i style="background:{color}"></i>{escape(group.capitalize())}</span>')
    labels = ''.join(
        f'<text class="chart-axis" x="{x_at(i):.1f}" y="{height-12}" text-anchor="middle">Semaine {i+1}</text>'
        for i in range(block_len)
    )
    return (
        '<div class="card chart-card"><h3>Volume musculaire au fil du cycle</h3>'
        '<p class="chart-note">Séries prescrites par muscle ; la semaine de décharge reprend la baisse de volume du programme.</p>'
        f'<svg class="chart-svg" viewBox="0 0 {width} {height}" role="img" aria-label="Séries prescrites par groupe musculaire pendant le cycle">'
        f'<title>Séries prescrites par groupe musculaire pendant le cycle</title>'
        + ''.join(grid) + ''.join(paths) + ''.join(dots) + labels
        + '</svg><div class="chart-legend">' + ''.join(legend) + '</div></div>'
    )


def _entry_has_shortfall(entry):
    for item in entry.get("exercices", []):
        reps = item.get("reps") or []
        target = item.get("prescrit_reps") or []
        if not reps or not target or not isinstance(reps, list) or not isinstance(target, list):
            continue
        try:
            actual = [int(value) for value in reps]
            prescribed = [int(value) for value in target]
        except (TypeError, ValueError):
            continue
        if len(actual) != len(prescribed) or any(a < p for a, p in zip(actual, prescribed)):
            return True
    return False


def adherence_chart(log, program, today, anchor, weeks=12):
    monday = today - timedelta(days=today.weekday())
    first = monday - timedelta(days=7 * (weeks - 1))
    sessions = {
        str(entry.get("date", ""))[:10]: entry
        for entry in log.get("seances", []) if isinstance(entry, dict)
    }
    labels = ("L", "Ma", "Me", "J", "V", "S", "D")
    cells, headers = [], []
    successful = planned = 0
    for label in labels:
        headers.append(f'<span class="heat-day-label">{label}</span>')
    for week_index in range(weeks):
        week_start = first + timedelta(days=week_index * 7)
        cells.append(f'<span class="heat-week">{week_start.day:02d}/{week_start.month:02d}</span>')
        for day_offset in range(7):
            day = week_start + timedelta(days=day_offset)
            session = program["programme"].get(day.weekday()) if day >= anchor else None
            if not session:
                cells.append('<span class="heat-cell rest" title="Repos"></span>')
                continue
            entry = sessions.get(day.isoformat(), {})
            if day >= today:
                status, label_text = "future", "À venir"
            elif entry.get("absent"):
                status, label_text = "absent", "Absence déclarée"
            elif _entry_has_shortfall(entry):
                status, label_text = "short", "Répétitions sous la prescription"
                planned += 1
            else:
                status, label_text = "done", "Séance réussie selon le journal"
                planned += 1
                successful += 1
            title = escape(f'{date_fr(day)} · {session["nom"]} · {label_text}', quote=True)
            cells.append(f'<span class="heat-cell {status}" title="{title}" aria-label="{title}"></span>')
    ratio = f'{round(100 * successful / planned)} %' if planned else "En attente"
    summary = (
        f'{successful}/{planned} séances réalisées · {ratio}' if planned else
        "Le suivi de régularité démarrera à la première séance passée."
    )
    legend = (
        ('done', 'Réussie'), ('short', 'À reprendre'),
        ('absent', 'Absence déclarée'), ('future', 'À venir'), ('rest', 'Repos'),
    )
    legend_html = ''.join(
        f'<span><i class="heat-cell {kind}"></i>{label}</span>'
        for kind, label in legend
    )
    return (
        '<div class="card chart-card"><h3>Régularité des séances</h3>'
        f'<p class="chart-note">{escape(summary)} · 12 semaines · les absences déclarées sont exclues du taux.</p>'
        '<div class="heatmap-wrap"><div class="heatmap">'
        + '<span class="heat-week"></span>' + ''.join(headers) + ''.join(cells)
        + '</div></div><div class="heat-legend">' + legend_html + '</div>'
        '<p class="chart-note" style="margin:12px 0 0;">Dans ce journal, une séance passée sans saisie vaut réussite. Déclare une absence ou note les répétitions manquantes pour corriger le suivi.</p>'
        '</div>'
    )


def performance_history_charts(log):
    history = {}
    for entry in log.get("seances", []):
        if not isinstance(entry, dict) or entry.get("absent"):
            continue
        day = str(entry.get("date", ""))[:10]
        try:
            date.fromisoformat(day)
        except ValueError:
            continue
        for item in entry.get("exercices", []):
            reps = item.get("reps") or []
            if not isinstance(reps, list) or not reps:
                continue
            try:
                actual_reps = [int(value) for value in reps]
            except (TypeError, ValueError):
                continue
            weight = item.get("charge")
            if not isinstance(weight, (int, float)):
                weight = item.get("charge_prescrite")
            if not isinstance(weight, (int, float)):
                continue
            history.setdefault(str(item.get("nom", "Exercice")), []).append({
                "date": day,
                "kg": float(weight),
                "reps": "/".join(str(value) for value in actual_reps),
            })
    entries = []
    for name, points in sorted(history.items()):
        points.sort(key=lambda point: point["date"])
        # Deux dates réelles sont le minimum pour montrer une tendance.
        if len({point["date"] for point in points}) < 2:
            continue
        values = [point["kg"] for point in points]
        width, height = 560, 170
        left, right, top, bottom = 42, 12, 12, 30
        plot_w, plot_h = width - left - right, height - top - bottom
        low, high = min(values), max(values)
        margin = max(1.0, (high - low) * .15)
        low, high = low - margin, high + margin
        coords = []
        for index, point in enumerate(points):
            x = left + (index / max(1, len(points) - 1)) * plot_w
            y = top + (1 - (point["kg"] - low) / (high - low)) * plot_h
            coords.append((x, y))
        line = ' '.join(f'{x:.1f},{y:.1f}' for x, y in coords)
        dots = ''.join(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#176b50">'
            f'<title>{escape(points[i]["date"])} · {fmt_number(points[i]["kg"])} kg · {escape(points[i]["reps"])} reps</title></circle>'
            for i, (x, y) in enumerate(coords)
        )
        svg = (
            f'<svg class="chart-svg" viewBox="0 0 {width} {height}" role="img" aria-label="Historique de charge, {escape(name)}">'
            f'<title>Historique de charge · {escape(name)}</title>'
            f'<line class="chart-gridline" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}"/>'
            f'<polyline points="{line}" fill="none" stroke="#176b50" stroke-width="2.5"/>'
            + dots
            + f'<text class="chart-axis" x="{left}" y="{height-5}">{escape(points[0]["date"])}</text>'
            + f'<text class="chart-axis" x="{width-right}" y="{height-5}" text-anchor="end">{escape(points[-1]["date"])}</text>'
            + '</svg>'
        )
        entries.append(
            '<article class="card history-item">'
            f'<h4>{escape(name)}</h4><p class="chart-note">Charge notée par séance, en kg.</p>'
            f'{svg}</article>'
        )
    if not entries:
        return (
            '<div class="history-empty">Aucun historique de charge exploitable pour l’instant. '
            'Il apparaîtra après deux séances enregistrées avec leurs répétitions.</div>'
        )
    return '<div class="chart-grid">' + ''.join(entries) + '</div>'


def render_dashboard(today, program, settings, anchor, log, earned):
    block_len = max(program["rir"])
    week = cycle_week(today, anchor, block_len)
    deload = week == program["deload_week"]
    current_phase = "Cycle à venir" if week is None else (
        "Semaine de décharge" if deload else "Développement")
    week_label = "Départ le " + date_fr(anchor) if week is None else f"Semaine {week}/{block_len}"
    rir = program["rir"].get(week, program["rir"].get(1, 3)) if week else program["rir"].get(1, 3)
    volume_counts, total_sets = weekly_sets(program, week or 1)
    next_day, next_plan = next_session(today, anchor, program)
    today_plan = program["programme"].get(today.weekday()) if today >= anchor else None
    display_day = today if today_plan else next_day
    display_plan = today_plan or next_plan
    display_week = cycle_week(display_day, anchor, block_len) if display_day else week
    earned_for_display = compute_credits(log, program, display_day or today, anchor, block_len)
    today_session_html = (
        session_card(display_day, display_plan,
                     session_data(display_plan, display_week or 1, earned_for_display, program, settings))
        if display_day and display_plan else
        '<div class="card log-panel"><h3>Programme en attente</h3><p>Renseigne un lundi de départ dans data/settings.json.</p></div>'
    )
    this_monday = today - timedelta(days=today.weekday())
    week_cells = []
    for offset in range(7):
        day = this_monday + timedelta(days=offset)
        session = program["programme"].get(day.weekday()) if day >= anchor else None
        day_week = cycle_week(day, anchor, block_len) if session else None
        if session:
            if day_week:
                day_sets = sum(
                    sets_for_week(e["series"], day_week, program["deload_week"], program["deload_factor"])
                    for e in session["exercices"]
                )
                small = f"Semaine {day_week} · {day_sets} séries"
            else:
                small = "à venir"
            week_cells.append(
                f'<div class="day{" today-day" if day == today else ""}">'
                f'<span class="date">{escape(date_short(day))}</span>'
                f'<strong>{escape(session["nom"])}</strong>'
                f'<small>{escape(small)}</small>'
                '</div>'
            )
        else:
            week_cells.append(
                f'<div class="day{" today-day" if day == today else ""}">'
                f'<span class="date">{escape(date_short(day))}</span>'
                '<strong>Repos</strong><small>aucune séance prescrite</small></div>'
            )
    max_volume = max(volume_counts.values(), default=1)
    volume_rows = []
    group_order = program["ordre_muscles"] + [group for group in volume_counts if group not in program["ordre_muscles"]]
    for group in group_order:
        amount = volume_counts.get(group, 0)
        if amount <= 0:
            continue
        width = max(4, round(100 * amount / max_volume))
        volume_rows.append(
            f'<div class="volume-row"><span>{escape(group.capitalize())}</span>'
            f'<span class="bar"><span style="width:{width}%"></span></span>'
            f'<strong>{amount}</strong></div>'
        )
    rows = []
    projection_cards = []
    projection_week = week or 1
    for ex, current, values, credits in projection_rows(program, settings, earned):
        next_load = values[1] if len(values) > 1 else current
        status = "à renseigner" if current is None else f'{fmt_number(current)} kg'
        projection = "—" if current is None else f'{fmt_number(next_load)} kg'
        spark = render_spark(values)
        range_label = f'{ex["lo"]}-{ex["hi"]} reps'
        rows.append(
            '<tr>'
            f'<td><b>{escape(ex["nom"])}</b><br><span class="muted">{escape(range_label)}</span></td>'
            f'<td>{escape(ex["materiel"])}</td>'
            f'<td><strong>{escape(status)}</strong></td>'
            f'<td>{escape(projection)} · prochain palier si objectifs tenus</td>'
            f'<td>{credits}</td><td>{spark}</td></tr>'
        )
        points = projection_week_points(ex, current, today, anchor, program, settings)
        group = program["muscles"].get(ex["nom"], "autres").capitalize()
        chart = progression_svg(ex, points)
        end_load = fmt_number(points[-1]["kg"]) + " kg" if points else "à renseigner"
        current_load = fmt_number(current) + " kg" if current is not None else "à renseigner"
        reps_text = f'{range_label} · {ex["materiel"]}'
        projection_cards.append(
            '<article class="card projection-card">'
            '<div class="projection-head">'
            f'<h3>{escape(ex["nom"])}</h3>'
            f'<span class="projection-context">{escape(group)} · {escape(reps_text)}</span>'
            '</div>'
            + chart
            + '<div class="projection-foot">'
            f'<span>Actuelle : <strong>{escape(current_load)}</strong></span>'
            f'<span>Fin des 6 cycles : <strong>{escape(end_load)}</strong></span>'
            f'<span>{credits} cycle(s) acquis</span></div></article>'
        )
    log_url = f"https://github.com/{REPO_FULL_NAME}/edit/main/data/seances.json"
    current_date = date_fr(today)
    save_notice = "Automatisation : actualisation quotidienne via GitHub Actions"
    status_text = "La charge de départ est une estimation ; corrige les maxima si nécessaire."
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#123c30">
<meta name="description" content="Programme personnel de musculation, progression et journal.">
<title>Coach IA</title>
<style>{CSS}</style>
</head>
<body><main class="wrap">
<header class="hero">
  <div class="topline"><div><p class="eyebrow">Ton entraînement, organisé</p>
  <h1>Coach IA</h1>
  <p class="sub">Ton programme de musculation, tes charges et ton cycle de progression au même endroit.</p></div>
  <span class="pill state">{escape(current_phase)} · {escape(week_label)}</span></div>
  <div class="hero-meta"><span class="pill">{escape(current_date)}</span>
  <span class="pill">Cycle {block_len} semaines · RIR {rir}</span>
  <span class="pill">{len(program["programme"])} séances par semaine</span></div>
</header>
<nav class="nav" aria-label="Sections du tableau de bord">
  <a href="#aujourdhui">Séance</a><a href="#semaine">Semaine</a><a href="#volume">Volume</a>
  <a href="#regularite">Régularité</a><a href="#programme">Programme</a>
  <a href="#progression">Progression</a><a href="#historique">Historique</a><a href="#journal">Journal</a>
</nav>
<section class="kpis" aria-label="Résumé">
  <div class="kpi"><span class="label">Phase du cycle</span><strong>{escape(week_label)}</strong></div>
  <div class="kpi"><span class="label">RIR cible</span><strong>{rir} répétitions en réserve</strong></div>
  <div class="kpi"><span class="label">Séries prescrites cette semaine</span><strong>{total_sets}</strong></div>
  <div class="kpi"><span class="label">Volume par groupes</span><strong>{len(volume_counts)} groupes suivis</strong></div>
</section>
<section class="section" id="aujourdhui">
  <div class="section-head"><div><h2>{"Ta séance" if today_plan else "À venir"}</h2>
  <p>{escape(date_fr(display_day) if display_day else "Aucune séance planifiée")}</p></div></div>
  {today_session_html}
</section>
<section class="section" id="semaine">
  <div class="section-head"><div><h2>Cette semaine</h2><p>Quatre séances prévues ; les jours sans séance restent libres.</p></div></div>
  <div class="week-grid">{"".join(week_cells)}</div>
</section>
<section class="section" id="volume">
  <div class="section-head"><div><h2>Volume hebdomadaire</h2><p>Nombre de séries prescrites par groupe musculaire.</p></div></div>
  <div class="card volume">{"".join(volume_rows)}</div>
  <div style="margin-top:12px;">{volume_cycle_chart(program)}</div>
</section>
<section class="section" id="regularite">
  <div class="section-head"><div><h2>Assiduité</h2><p>Vue calendrier du programme de musculation sur les douze dernières semaines.</p></div></div>
  {adherence_chart(log, program, today, anchor)}
</section>
<section class="section" id="programme">
  <div class="section-head"><div><h2>Programme complet</h2><p>Les prescriptions affichées suivent la semaine du cycle en cours.</p></div></div>
  <div class="programme-grid">{"".join(session_card(None, program["programme"][d], session_data(program["programme"][d], week or 1, earned, program, settings)) for d in sorted(program["programme"]))}</div>
</section>
<section class="section" id="progression">
  <div class="section-head"><div><h2>Progression des charges</h2><p>Projection par exercice sur six cycles ; les bandes orange marquent les semaines de décharge.</p></div></div>
  <p class="chart-note">La charge progresse uniquement après un cycle validé. Les courbes montrent le plan si les répétitions prescrites sont atteintes ; elles ne prédisent pas tes performances.</p>
  <div class="chart-grid">{"".join(projection_cards)}</div>
  <div class="section-head" style="margin-top:20px;"><div><h2>Repères par exercice</h2><p>La charge actuelle, le prochain palier et les cycles déjà validés.</p></div></div>
  <div class="card projection"><table><thead><tr><th>Exercice · fourchette</th><th>Matériel</th><th>Charge actuelle</th><th>Après un cycle</th><th>Cycles acquis</th><th>7 cycles</th></tr></thead>
  <tbody>{"".join(rows)}</tbody></table></div>
</section>
<section class="section" id="historique">
  <div class="section-head"><div><h2>Historique des charges</h2><p>Courbes construites à partir des répétitions réellement saisies dans le journal.</p></div></div>
  {performance_history_charts(log)}
</section>
<section class="section" id="journal">
  <div class="section-head"><div><h2>Journal</h2><p>{escape(save_notice)}</p></div></div>
  <div class="card log-panel"><p>{escape(status_text)} Une répétition sous la prescription bloque le crédit de progression de cet exercice pour le cycle.</p>
  <p>Le journal reste dans ce dépôt. La page ne stocke pas les saisies dans le navigateur.</p>
  <a class="button" href="{escape(log_url)}" target="_blank" rel="noopener">Modifier mon journal sur GitHub</a>
  <h3>Format d’une entrée</h3>
<pre>{{
  "date": "2026-10-12",
  "seance": "Bas",
  "exercices": [
    {{"nom": "Squat barre haute", "prescrit_reps": [7, 6, 6], "reps": []}}
  ]
}}</pre>
  <p>Après modification, l’action GitHub régénère la page automatiquement.</p></div>
</section>
<div class="section callout"><b>À garder en tête.</b> Le programme et le volume jambes sont repris du dépôt source. La partie course et Garmin n’est pas suivie dans cette application.</div>
<footer>Tableau de bord personnel · Aucun appel Garmin, Gemini ou Firebase · Généré le {escape(current_date)}</footer>
</main></body></html>
"""


def main():
    parser = argparse.ArgumentParser(description="Génère Coach IA.")
    parser.add_argument("--today", help="Date de génération AAAA-MM-JJ (facultatif).")
    args = parser.parse_args()
    today = date.fromisoformat(args.today) if args.today else date.today()
    program = load_program()
    settings, anchor = load_settings()
    block_len = max(program["rir"])
    log = read_log()
    earned = compute_credits(log, program, today, anchor, block_len)
    log = ensure_session_log(log, today, anchor, program, settings, earned)
    earned = compute_credits(log, program, today, anchor, block_len)
    page = render_dashboard(today, program, settings, anchor, log, earned)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(page, encoding="utf-8")
    print(f"Dashboard écrit : {OUTPUT_PATH}")
    print(f"Cycle : {cycle_week(today, anchor, block_len) or 'à venir'} · {len(log['seances'])} entrées au journal")


if __name__ == "__main__":
    main()

