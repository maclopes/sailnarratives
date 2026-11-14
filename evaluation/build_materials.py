"""Build the printable interview materials (sheets 1 to 3) and the recording templates.

    python evaluation/build_materials.py [--game ../fragateiro] [--pdf]

Reads the items to ask about (evaluation/items.yaml), the tool's data (data/workbench/), the
game's world list (domains/sailing/game-world.json) and, from a checkout of the game, its
Portuguese texts and boat pictures. Writes evaluation/materiais/: folha-1, folha-2, folha-3 as
HTML, folha-2b (activities, shown blind) (and PDF with --pdf, using the pre-installed Playwright), registo.csv (one row per item, to
fill in per participant) and recordacao-livre.csv (the step-1 answers).
"""

from __future__ import annotations

import argparse
import csv
import glob
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "workbench"
OUT = ROOT / "evaluation" / "materiais"

CSS = """
@page { size: A4; margin: 16mm 14mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 15pt; line-height: 1.35; color: #111; }
h1 { font-size: 22pt; margin: 0 0 4mm; } h2 { font-size: 18pt; margin: 8mm 0 3mm; page-break-after: avoid; }
p.sub { font-size: 13pt; color: #333; margin: 0 0 4mm; }
table { width: 100%; border-collapse: collapse; margin-bottom: 4mm; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #555; padding: 2.2mm 2mm; vertical-align: top; text-align: left; }
th { background: #eee; font-size: 12pt; }
td.box { width: 12mm; text-align: center; font-size: 13pt; white-space: nowrap; }
td.id { width: 10mm; font-size: 11pt; color: #444; }
td.n { width: 14mm; font-size: 12pt; color: #444; text-align: center; }
.opt { display: block; margin: 1mm 0; } .sq { display: inline-block; width: 5mm; height: 5mm; border: 1.5px solid #222; margin-right: 2mm; vertical-align: -1mm; }
.lines div { border-bottom: 1px solid #999; height: 10mm; }
.boat { display: flex; gap: 4mm; align-items: flex-start; } .boat img { width: 42mm; height: 28mm; object-fit: cover; border: 1px solid #999; }
.small { font-size: 12pt; color: #444; }
.pb { page-break-before: always; }
"""

SQ = '<span class="sq"></span>'


def page(title: str, body: str) -> str:
    return f'<!doctype html><html lang="pt"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>'


def lines(n: int) -> str:
    return '<div class="lines">' + "<div></div>" * n + "</div>"


def latest_report() -> dict:
    reps = [json.loads(Path(f).read_text(encoding="utf-8")) for f in glob.glob(str(DATA / "reports" / "*.json"))]
    return max(reps, key=lambda r: r["createdAt"])


def source_counts() -> dict[str, int]:
    """Number of independent sources behind each item the items refer to."""
    out: dict[str, int] = {}
    rep = latest_report()
    for kind in ("boats", "places"):
        for e in rep[kind]:
            for n in [e["name"], *e.get("also", [])]:
                out.setdefault(f"{kind[:-1]}:{n}", len(e["sources"]))
    cands = {}
    for f in glob.glob(str(DATA / "candidates" / "*.json")):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        for x in d["items"]:
            cands[x["id"]] = d["sourceId"]
    for c in json.loads((DATA / "concepts" / "current.json").read_text(encoding="utf-8"))["concepts"]:
        n = len({cands[i] for i in c["members"] if i in cands and not cands[i].startswith("m-sim")})
        out[f"concept:{c['id']}"] = n
        out.setdefault(f"concept:{c['label']}", n)
    pc = {}
    for f in glob.glob(str(DATA / "practiceCands" / "*.json")):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        for x in d["items"]:
            pc[x["id"]] = d["sourceId"]
    for p in json.loads((DATA / "practices" / "current.json").read_text(encoding="utf-8"))["practices"]:
        out[f"practice:{p['id']}"] = len({pc[i] for i in p["members"] if i in pc})
    return out


def line_text(ref: str) -> dict:
    _, game, lid = ref.split(":")
    rec = json.loads((DATA / "narrativeLines" / f"{game}.json").read_text(encoding="utf-8"))
    return next(x for x in rec["lines"] if x["id"] == lid)


def game_texts(game: Path) -> dict[str, str]:
    f = game / "content" / "texts" / "pt.txt"
    out = {}
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines():
            if "=" in ln and not ln.startswith("#"):
                k, v = ln.split("=", 1)
                out[k.strip()] = re.sub(r"<[^>]+>", "", v.strip())
    return out


def sheet1() -> str:
    b = ['<h1>Folha 1 · Registo da entrevista</h1><p class="sub">Para o entrevistador. Anotar os nomes tal como são ditos.</p>',
         '<table><tr><th>Participante</th><td style="width:35%"></td><th>Data</th><td></td></tr>',
         '<tr><th>Autorização</th><td>' + SQ + 'sim ' + SQ + 'não</td><th>Gravação</th><td>' + SQ + 'sim ' + SQ + 'não</td></tr></table>',
         '<h2>Perfil</h2><table>',
         '<tr><th style="width:38%">Relação com o Tejo e os barcos</th><td>' + "".join(f'<span class="opt">{SQ}{t}</span>' for t in ["marinheiro de barco tradicional", "pescador", "construtor naval", "historiador / investigador", "museu", "outro: ____________"]) + "</td></tr>",
         '<tr><th>Anos de experiência</th><td></td></tr><tr><th>Barcos que conhece ou em que navegou</th><td style="height:18mm"></td></tr>',
         '<tr><th>Zona do rio que conhece melhor</th><td></td></tr>',
         '<tr><th>Idade</th><td>' + " ".join(f"{SQ}{t}" for t in ["&lt;40", "40–60", "60–75", "&gt;75"]) + "</td></tr></table>"]
    for i, (t, n) in enumerate([("1. Barcos (para que servia, onde andava)", 9), ("2. Lugares (portos, cais, praias, pesqueiros, partes do rio)", 8),
                                ("3. Trabalhos (o que se fazia, quem fazia)", 8), ("4. Épocas (até quando, porquê acabou)", 6),
                                ("5. Palavras (manobras, partes do barco, pessoas a bordo)", 7), ("6. Erros comuns", 5),
                                ("Passo 2 · O que falta no jogo", 6), ("Fecho · Outras coisas; outras pessoas a ouvir", 5)]):
        b.append(f'<h2{" class=pb" if i in (2, 6) else ""}>{html.escape(t)}</h2>' + lines(n))
    b.append('<p class="small">Duração da entrevista: ______ min</p>')
    return page("Folha 1", "".join(b))


def sheet2(world: dict, tx: dict, img_dir: Path) -> str:
    def row3(label: str, extra: str = "", img: str = "") -> str:
        cell = f'<div class="boat">{img}<div><b>{label}</b>{("<br><span class=small>" + extra + "</span>") if extra else ""}</div></div>' if img else f"<b>{label}</b>{('<br><span class=small>' + extra + '</span>') if extra else ''}"
        return f'<tr><td>{cell}</td><td class="box">{SQ}</td><td class="box">{SQ}</td><td class="box">{SQ}</td></tr>'
    head = '<tr><th></th><th>Certo</th><th>Errado</th><th>Não sei</th></tr>'
    b = ['<h1>Folha 2 · O que o jogo tem hoje</h1><p class="sub">Para cada coisa: está certa, está errada, ou não sabe? No fim: o que falta?</p>',
         '<h2>Barcos</h2><table>' + head]
    for bt in world["boats"]:
        key = bt["name"].lower()
        name = bt["name"] + (" (ainda em preparação)" if bt.get("in_development") else "")
        img = f'<img src="img/{key}.jpg" alt="">' if (img_dir / f"{key}.jpg").exists() else ""
        desc = tx.get(f"boat.{key}.desc", bt.get("description", ""))
        desc = " ".join(x for x in re.split(r"(?<=[.!?])\s+", desc) if not re.search(r"modelo 3D|Meshy|No jogo", x))
        b.append(row3(html.escape(name), html.escape(desc), img))
    b.append("</table>")
    b.append('<h2 class="pb">Zonas do jogo</h2><table>' + head)
    for a in world["ports"]:
        b.append(row3(html.escape(tx.get(f"area.{a}", world["area_names"].get(a, a)))))
    b.append("</table>")
    for a, title in (("tejo", "Lugares do mapa do Tejo (estuário)"), ("medio", "Lugares do mapa do Médio Tejo")):
        if a in world["ports"]:
            b.append(f"<h2>{title}</h2><table>" + head + "".join(row3(html.escape(p)) for p in world["ports"][a]) + "</table>")
    # the game's activities are not listed here: they are on Folha 2B, mixed blind with the tool's
    b.append("<h2>O que falta no jogo?</h2>" + lines(6))
    return page("Folha 2", "".join(b))


def sheet2b(items: dict) -> str:
    """The game's activities and the tool's proposals in one list, with no sign of their origin."""
    b = ['<h1>Folha 2B · Atividades para o jogo</h1><p class="sub">Atividades que o jogo pode ter. Para cada uma: os barcos do Tejo faziam isto? '
         'O barco é o certo para isto? É importante mostrá-lo num jogo sobre o Tejo?</p>',
         '<table><tr><th></th><th>Atividade</th><th>Faziam isto?<br>sim · não · não sei</th><th>Barco certo?<br>sim · não · não sei</th><th>Importante?<br>1 · 2 · 3</th></tr>']
    for it in items.get("activities", []):
        b.append(f'<tr><td class="id">{it["id"]}</td><td>{html.escape(it["pt"])}</td>'
                 f'<td class="box">{SQ}{SQ}{SQ}</td><td class="box">{SQ}{SQ}{SQ}</td><td class="box">{SQ}{SQ}{SQ}</td></tr>')
    b.append("</table><h2>Que outras atividades mostraria?</h2>" + lines(6))
    return page("Folha 2B", "".join(b))


def sheet3(items: dict, counts: dict) -> str:
    def rows(sec: list, with_n: bool = True) -> str:
        h = '<table><tr><th></th><th>Afirmação</th><th>Certo?<br>sim · não · não sei</th><th>Importante?<br>1 · 2 · 3</th><th>Já sabia?<br>sim · não</th></tr>'
        for it in sec:
            h += (f'<tr><td class="id">{it["id"]}</td><td>{html.escape(it["pt"])}</td>'
                  f'<td class="box">{SQ}{SQ}{SQ}</td><td class="box">{SQ}{SQ}{SQ}</td><td class="box">{SQ}{SQ}</td></tr>')
        return h + "</table>"
    b = ['<h1>Folha 3 · O que a ferramenta encontrou</h1><p class="sub">Uma ferramenta leu livros, artigos e páginas sobre o Tejo e tirou estas conclusões. Estão certas?</p>',
         '<h2>A. Barcos que as fontes referem e que o jogo não tem</h2>', rows(items["boats"]),
         '<h2 class="pb">B. Lugares que as fontes referem e que o jogo não tem (ou não sabe situar)</h2>', rows(items["places"]),
         '<h2 class="pb">C. Trabalhos e práticas</h2>', rows(items["practices"]),
         '<h2 class="pb">D. As fontes contradizem-se: qual está certa?</h2><table><tr><th></th><th>Pergunta</th><th>Versões (assinalar)</th><th>Como sabe?</th></tr>']
    for c in items["conflicts"]:
        opts = "".join(f'<span class="opt">{SQ}{html.escape(o)}</span>' for o in c["options"] + ["as duas / várias", "nenhuma", "não sei"])
        b.append(f'<tr><td class="id">{c["id"]}</td><td>{html.escape(c["pt"])}</td><td>{opts}</td><td style="width:22%"></td></tr>')
    b.append('</table><h2 class="pb">E. Que palavra usavam os marinheiros do Tejo?</h2><table><tr><th></th><th>Significado</th><th>Palavras (assinalar; pode ser mais de uma)</th><th>Outra</th></tr>')
    for t in items["terms"]:
        opts = "".join(f'<span class="opt">{SQ}{html.escape(o)}</span>' for o in t["options"])
        b.append(f'<tr><td class="id">{t["id"]}</td><td>{html.escape(t["pt"])}</td><td>{opts}</td><td style="width:20%"></td></tr>')
    b.append('</table><h2 class="pb">F. Falas escritas para o jogo</h2><p class="sub">Ditas por personagens inventadas. O que dizem sobre os barcos e o rio está certo? Um homem do rio diria assim?</p>'
             '<table><tr><th></th><th>Fala</th><th>Certo?<br>sim · não · não sei</th><th>Diria assim?<br>sim · não</th></tr>')
    for f in items["lines"]:
        ln = line_text(f["ref"])
        b.append(f'<tr><td class="id">{f["id"]}</td><td>«{html.escape(ln["pt"])}»</td><td class="box">{SQ}{SQ}{SQ}</td><td class="box">{SQ}{SQ}</td></tr>')
    b.append("</table>")
    return page("Folha 3", "".join(b))


def templates(items: dict, counts: dict) -> None:
    with (OUT / "registo.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["participante", "seccao", "item", "ref", "fontes_ferramenta", "estado_ferramenta", "origem", "texto",
                    "certo (sim/nao/nao_sei)", "importante (1-3)", "ja_sabia (sim/nao)", "barco_certo (sim/nao/nao_sei)", "versao_escolhida", "termo_escolhido", "diria_assim (sim/nao)", "como_sabe", "notas"])
        # G (Folha 2B): "certo" is "faziam isto?"; origem and estado (the tool's blind match) are for the analysis
        for sec, key in (("G", "activities"), ("A", "boats"), ("B", "places"), ("C", "practices"), ("D", "conflicts"), ("E", "terms"), ("F", "lines")):
            for it in items.get(key, []):
                text = it.get("pt") or line_text(it["ref"])["pt"]
                w.writerow(["P?", sec, it["id"], it["ref"], counts.get(it["ref"], ""), it.get("status", it.get("match", "")), it.get("origin", ""), text] + [""] * 9)
    with (OUT / "recordacao-livre.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["participante", "tipo (barco/lugar/trabalho/epoca/palavra/erro)", "nome_como_dito", "detalhe (para que servia, onde, quando)", "notas"])
        w.writerow(["P1", "barco", "varino", "carga, Tejo", ""])


def to_pdf(files: list[Path]) -> None:
    js = """
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const f of process.argv.slice(1)){const p=await b.newPage();await p.goto('file://'+f);await p.pdf({path:f.replace(/\\.html$/,'.pdf'),format:'A4',printBackground:true});await p.close();}
await b.close();})();"""
    for f in files:  # one browser per file: more robust than one for all
        subprocess.run(["node", "-e", js, str(f)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--game", type=Path, default=ROOT.parent / "fragateiro")
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    items = yaml.safe_load((ROOT / "evaluation" / "items.yaml").read_text(encoding="utf-8"))
    world = json.loads((ROOT / "domains" / "sailing" / "game-world.json").read_text(encoding="utf-8"))
    counts = source_counts()
    missing = [it["ref"] for k in ("boats", "places", "practices", "conflicts", "terms") for it in items[k] if it["ref"] not in counts]
    if missing:
        print("refs with no source count:", ", ".join(missing))
    img = OUT / "img"
    img.mkdir(exist_ok=True)
    for f in (a.game / "src" / "assets" / "boats").glob("*.jpg"):
        shutil.copy(f, img / f.name)
    tx = game_texts(a.game)
    files = []
    for name, content in (("folha-1-registo", sheet1()), ("folha-2-o-jogo", sheet2(world, tx, img)), ("folha-2b-atividades", sheet2b(items)), ("folha-3-achados", sheet3(items, counts))):
        f = OUT / f"{name}.html"
        f.write_text(content, encoding="utf-8")
        files.append(f)
    templates(items, counts)
    if a.pdf:
        to_pdf(files)
    print("written:", ", ".join(p.name for p in sorted(OUT.iterdir())))


if __name__ == "__main__":
    main()
