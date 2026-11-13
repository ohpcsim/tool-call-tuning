"""Check the built site. Exit 1 on any failure.

1. Every table on the results page matches what the CSV files give, computed here independently.
2. Every page carries the banner.
3. No forbidden word or internal name appears in the built text.
4. The registry check on the results page ran and printed its line.
5. No internal name appears in the published text files under pipeline/ and data/.
6. The to-do counts typed on the home page and in the gate page's table match todo.csv.

Usage: .venv/bin/python check_site.py   (after ./build_site.sh)
"""
import csv
import json
import pathlib
import re
import sys
from collections import OrderedDict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "_build" / "html"
TABLES = ROOT / "data" / "tables"
BANNER = "Working benchmark: open validation only; not held-out; no confirmatory claim"
PAGES = ["index", "premise", "project", "results", "gate", "serving", "sealed-test", "measured", "tools", "build"]

# Words the study's records rule out for these results (study facts, section 2).
FORBIDDEN = [r"held-out", r"confirmed", r"reproduced", r"passed", r"accepted", r"fixed", r"safe", r"eliminated",
             r"solved", r"eligible", r"deleted tasks", r"real mutations", r"passes the selection rule",
             r"e3 is better"]
# The only uses allowed: the banner, the recorded negative verdict, and the study's exact sealed-test wording.
ALLOWED = [r"not held-out", r"not reproduced",
           # Three exact phrases from the study owner's own explanations of labels in the published files (November 12).
           # Each describes a label or a training run, not a result of a model.
           r"the hypothesis a later held-out evaluation would test",
           r"the run passed the study.s training-health check",
           r"todo-select-v1-no-eligible",
           r"The held-out evaluation on that test was not run",
           r"Until a held-out evaluation is run and reported, every result on this site is open validation only",
           r"The final head passed independent review"]
# Things that must never appear on a public page: local paths, machine addresses and session identifiers.
INTERNAL = [r"mcp:", r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", r"/home/",
            r"[A-Za-z]:[/\\]Users", r"~/", r"localhost"]
# A site maintainer can list further private names, one regular expression per line, in a local file
# that is never committed. The check uses it when it is present.
_extra = pathlib.Path(__file__).with_name("private-names.txt")
N_PUBLIC = len(INTERNAL)  # patterns after this index are private: report them by number, never by text
if _extra.exists():
    INTERNAL += [line.strip() for line in _extra.read_text().splitlines() if line.strip() and not line.startswith("#")]

failures = []


class Text(HTMLParser):
    """Visible text, and the cells of every table."""

    def __init__(self):
        super().__init__()
        self.text, self.tables, self._skip, self._cell = [], [], 0, None

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag == "table":
            self.tables.append([])
        elif tag == "tr":
            self.tables[-1].append([])
        elif tag in ("td", "th"):
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        elif tag in ("td", "th"):
            self.tables[-1][-1].append("".join(self._cell).strip())
            self._cell = None

    def handle_data(self, data):
        if self._skip:
            return
        self.text.append(data)
        if self._cell is not None:
            self._cell.append(data)


def parse(html):
    p = Text()
    p.feed(html)
    return p


def strings(node):
    """Every string in a page's JSON, which holds the text and the executed outputs."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v)


def outputs(node):
    """Executed cell outputs on a page, in order."""
    if isinstance(node, dict):
        if "jupyter_data" in node:
            yield node["jupyter_data"]
        for v in node.values():
            yield from outputs(v)
    elif isinstance(node, list):
        for v in node:
            yield from outputs(v)


def rows(name):
    with open(TABLES / name, newline="") as f:
        return list(csv.DictReader(f))


def only(values):
    values = set(values)
    if len(values) != 1:
        failures.append(f"expected one denominator, got {sorted(values)}")
    return values.pop()


def expected_tables():
    names = OrderedDict([("t-base", "Base model, before tuning"), ("t-new-R16-e1", "Tuned, 1 epoch"),
                         ("t-new-R16-e2", "Tuned, 2 epochs"), ("t-new-R16-e3", "Tuned, 3 epochs"),
                         ("t-a8", "Earlier reference model (control, optimistic)")])
    todo = [r for r in rows("todo.csv") if r["pool"] == "t-new" and r["arm"] in names]
    n = only(r["primary_n"] for r in todo)
    registry = rows("registry.csv")
    registered = {r["arm"]: f"{r['artifact']}@{r['version']}" for r in registry}
    t1 = [["Model", "Run", f"Correct, of {n}", "Wrong destructive", "Registered version"]]
    t1 += [[names[r["arm"]], r["arm"], r["primary_k"], r["wrong_destructive"],
            registered.get(r["arm"], "not registered")] for r in todo]

    base = next(r for r in todo if r["role"] == "reference")
    change = [["Model", f"Correct, of {n}, change from the base model",
               "Wrong destructive, change from the base model"]]
    change += [[names[r["arm"]], f"{int(r['primary_k']) - int(base['primary_k']):+d}",
                f"{int(r['wrong_destructive']) - int(base['wrong_destructive']):+d}"]
               for r in todo if r["role"] == "candidate"]

    desk = rows("desk.csv")
    t2 = [["Run", "Role", f"Exact, of {only(r['primary_n'] for r in desk)}",
           f"False actions, of {only(r['must_clarify_n'] for r in desk)}"]]
    t2 += [[r["arm"], r["role"], r["primary_k"], r["false_actions_must_clarify"]] for r in desk]

    t3 = [["Run", "Experiment", "Commit", "Artifact", "Version", "Stage"]]
    t3 += [[r["arm"], r["experiment_ref"].split("/")[-1], r["commit"][:7], r["artifact"], r["version"], r["stage"]]
           for r in registry]

    studies = OrderedDict()
    for r in rows("cost.csv"):
        studies.setdefault(r["study"], []).append(r)
    t4 = [["Study", "Training runs", "Training job wall-clock minutes", "Validation GPU minutes"]]
    for study, rs in studies.items():
        minutes = round(sum(float(r["training_job_wall_minutes"]) for r in rs), 2)
        t4.append([study, str(len(rs)), minutes, only(r["validation_gpu_minutes"] for r in rs)])
    return [t1, change, t2, t3, t4]


def same(got, want):
    if len(got) != len(want):
        return False
    for g_row, w_row in zip(got, want):
        if len(g_row) != len(w_row):
            return False
        for g, w in zip(g_row, w_row):
            if isinstance(w, float):
                try:
                    if abs(float(g) - w) > 1e-9:
                        return False
                except ValueError:
                    return False
            elif g != w:
                return False
    return True


def check_results(page_json):
    outs = list(outputs(page_json["mdast"]))
    shown = [parse(o["data"]["text/html"]["content"]).tables[0] for o in outs
             if "text/html" in o.get("data", {})]
    want = expected_tables()
    if len(shown) != len(want):
        failures.append(f"results: {len(shown)} tables shown, expected {len(want)}")
    for i, (got, w) in enumerate(zip(shown, want), 1):
        if not same(got, w):
            failures.append(f"results: table {i} differs from the CSV files\n  shown: {got}\n  want:  {w}")
    registry = rows("registry.csv")
    line = f"{len(registry)} registered versions. Stages: {', '.join(sorted({r['stage'] for r in registry}))}.\n"
    if not any(o.get("text") == line for o in outs):
        failures.append(f"results: registry summary line missing or wrong, expected {line!r}")
    if not any(re.fullmatch(r"All 12 version tags in pipeline/registry/versions\.txt point at the commits "
                            r"in registry\.csv and experiment-graph\.csv\.\n", o.get("text", "")) for o in outs):
        failures.append("results: the registry check's line is missing or wrong")
    todo = [r for r in rows("todo.csv") if r["pool"] == "t-new" and r["role"] == "candidate"]
    zero = f"{sum(r['wrong_destructive'] == '0' for r in todo)} of {len(todo)}.\n"
    if not any(o.get("text", "").startswith("Tuned models with zero wrong destructive actions") and
               o["text"].endswith(zero) for o in outs):
        failures.append("results: the zero-count line is missing or wrong")
    if any(o.get("output_type") == "error" for o in outs):
        failures.append("results: a code cell raised an error")


def check_typed(home_text, gate_tables):
    """Typed to-do counts on the home page and the 'before' half of the gate table, against todo.csv."""
    todo = {r["arm"]: r for r in rows("todo.csv") if r["pool"] == "t-new"}
    for arm in ("t-base", "t-new-R16-e1", "t-new-R16-e2", "t-new-R16-e3"):
        if not re.search(rf"\b{todo[arm]['primary_k']}\b", home_text):
            failures.append(f"index: the correct count for {arm} is not on the home page")
    arms = {"Tuned, 2 epochs": "t-new-R16-e2", "Tuned, 1 epoch": "t-new-R16-e1", "Tuned, 3 epochs": "t-new-R16-e3",
            "Earlier reference model": "t-a8", "Base model, before tuning": "t-base"}
    table = next((t for t in gate_tables if t and t[0][:1] == ["Model"]), None)
    if table is None or len(table) != len(arms) + 1:
        failures.append("gate: the added-check table is missing or has a different number of rows")
        return
    for model, correct, wrong in table[1:]:
        arm = next((a for label, a in arms.items() if model.startswith(label)), None)
        if arm is None:
            failures.append(f"gate: unknown row {model!r}")
        elif (correct.split(",")[0], wrong.split(",")[0]) != (todo[arm]["primary_k"], todo[arm]["wrong_destructive"]):
            failures.append(f"gate: the counts before the added check for {model!r} differ from todo.csv")


def scan(label, text):
    clean = text
    for a in ALLOWED:
        clean = re.sub(a, " ", clean, flags=re.IGNORECASE)
    for w in FORBIDDEN:
        for m in re.finditer(rf"\b{w}\b", clean, flags=re.IGNORECASE):
            failures.append(f"{label}: forbidden word {m.group(0)!r} in ...{clean[max(0, m.start() - 60):m.end() + 60]!r}...")
    # A model, run or system is never said to pass or meet a rule here: no amended selection has been run or signed.
    # Negative statements ("no model met the rules") and software checks ("the test passed") are fine.
    for sent in re.split(r"(?<=[.!?])\s+", clean):
        m = re.search(r"\b(models?|runs?|systems?|adapters?|candidates?)\s+(?:\w+\s+){0,2}(pass|passes|passed|meets|met)\b", sent, flags=re.IGNORECASE)
        if m and "?" not in sent and not re.search(r"\b(no|none|not|never|neither|nothing|didn't|did not|does not|cannot|has to|must|would|should|could|may|if|once|until|before)\b", sent, flags=re.IGNORECASE):
            failures.append(f"{label}: a model, run or system is said to pass or meet something in ...{sent[:160]!r}...")
    internal(label, text)


def internal(label, text):
    for i, pat in enumerate(INTERNAL):
        for m in re.finditer(pat, text):
            if i >= N_PUBLIC:  # the check's output can be public, so a private match is not printed
                failures.append(f"{label}: private pattern {i - N_PUBLIC + 1} matches")
                break
            failures.append(f"{label}: internal name {m.group(0)!r} in ...{text[max(0, m.start() - 60):m.end() + 60]!r}...")


def main():
    if not (HTML / "index.html").exists():
        sys.exit("No built site. Run ./build_site.sh first.")
    for page in PAGES:
        html_file = HTML / ("index.html" if page == "index" else f"{page}/index.html")
        page_json = json.loads((HTML / f"{page}.json").read_text())
        parsed = parse(html_file.read_text())
        visible = " ".join(parsed.text)
        if page == "index":
            home_text = visible
        if page == "gate":
            gate_tables = parsed.tables
        if BANNER not in visible:
            failures.append(f"{page}: banner missing")
        # Page JSON holds the same text plus executed outputs, which the browser renders.
        scan(page, visible + "\n" + "\n".join(strings(page_json["mdast"])) + "\n" + page_json["frontmatter"].get("title", ""))
        if page == "results":
            check_results(page_json)
    check_typed(home_text, gate_tables)
    for svg in sorted((HTML / "_public").glob("*.svg")):
        scan(svg.name, " ".join(parse(svg.read_text()).text))
    sources = [f for d in ("pipeline", "data") for f in sorted((ROOT / d).rglob("*")) if f.is_file()]
    for f in sources:
        internal(str(f.relative_to(ROOT)), f.read_text())
    if failures:
        print("\n".join(failures))
        print(f"FAIL: {len(failures)} problem(s)")
        sys.exit(1)
    private = f"{len(INTERNAL) - N_PUBLIC} private patterns used" if len(INTERNAL) > N_PUBLIC else "private pattern list not present"
    print(f"OK: {len(PAGES)} pages carry the banner, 5 results tables match the CSV files, the typed to-do counts on the home and gate pages match todo.csv, "
          f"the registry check ran, no forbidden word or internal name found on the pages, "
          f"no internal name found in {len(sources)} files under pipeline/ and data/ ({private}).")


if __name__ == "__main__":
    main()
