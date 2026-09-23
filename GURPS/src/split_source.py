from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
HTML_DIR = SRC / 'html'
CSS_DIR = SRC / 'css'

HTML_MARKERS = [
    ("00-setup.html", "", "<!-- ===== ===== ===== ===== TABS ===== ===== ===== ===== -->"),
    ("10-tabs.html", "<!-- ===== ===== ===== ===== TABS ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== TRAITS TAB ===== ===== ===== ===== -->"),
    ("20-traits.html", "<!-- ===== ===== ===== ===== TRAITS TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== MISCELLANEOUS TAB ===== ===== ===== ===== -->"),
    ("30-misc.html", "<!-- ===== ===== ===== ===== MISCELLANEOUS TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== SKILLS TAB ===== ===== ===== ===== -->"),
    ("40-skills.html", "<!-- ===== ===== ===== ===== SKILLS TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== COMBAT TAB ===== ===== ===== ===== -->"),
    ("50-combat.html", "<!-- ===== ===== ===== ===== COMBAT TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== ITEMS TAB ===== ===== ===== ===== -->"),
    ("60-items.html", "<!-- ===== ===== ===== ===== ITEMS TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== GRIMOIRE TAB ===== ===== ===== ===== -->"),
    ("70-grimoire.html", "<!-- ===== ===== ===== ===== GRIMOIRE TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== CHASE CONTROL SHEET TAB ===== ===== ===== ===== -->"),
    ("80-chase.html", "<!-- ===== ===== ===== ===== CHASE CONTROL SHEET TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== VEHICLE SHEET TAB ===== ===== ===== ===== -->"),
    ("90-vehicle.html", "<!-- ===== ===== ===== ===== VEHICLE SHEET TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== Revision History TAB ===== ===== ===== ===== -->"),
    ("99-updates-footer.html", "<!-- ===== ===== ===== ===== Revision History TAB ===== ===== ===== ===== -->", "<!-- ===== ===== ===== ===== LOGO ===== ===== ===== ===== -->"),
    ("100-logo.html", "<!-- ===== ===== ===== ===== LOGO ===== ===== ===== ===== -->", "<script type=\"text/worker\">"),
    ("110-worker.html", "<script type=\"text/worker\">", "</script>", True),
]

CSS_MARKERS = [
    ("00-base.css", "", "/* ===== CUSTOM TABLES ===== */"),
    ("10-custom-tables.css", "/* ===== CUSTOM TABLES ===== */", "/* -- TRAITS -- */"),
    ("20-traits.css", "/* -- TRAITS -- */", "/* -- MISC TAB -- */"),
    ("30-misc.css", "/* -- MISC TAB -- */", "/* -- SKILLS -- */"),
    ("40-skills.css", "/* -- SKILLS -- */", "/* -- COMBAT -- */"),
    ("50-combat.css", "/* -- COMBAT -- */", "/* -- INVENTORY -- */"),
    ("60-inventory.css", "/* -- INVENTORY -- */", "/* -- SPELLS -- */"),
    ("70-spells.css", "/* -- SPELLS -- */", "/* -- FOOTER -- */"),
    ("99-footer.css", "/* -- FOOTER -- */", ""),
]


def extract_segment(text: str, start_marker: str, end_marker: str, include_end: bool = False) -> str:
    if not start_marker:
        start_index = 0
    else:
        start_index = text.index(start_marker)

    if not end_marker:
        end_index = len(text)
    else:
        end_index = text.index(end_marker)
        if include_end:
            end_index += len(end_marker)

    return text[start_index:end_index]


def write_html_sections() -> list[str]:
    html_text = (ROOT / 'gurps.html').read_text(encoding='utf-8')
    html_paths = []
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    for filename, start_marker, end_marker, *rest in HTML_MARKERS:
        include_end = bool(rest and rest[0])
        content = extract_segment(html_text, start_marker, end_marker, include_end)
        target = HTML_DIR / filename
        target.write_text(content, encoding='utf-8')
        html_paths.append(f'html/{filename}')
    return html_paths


def write_css_sections() -> list[str]:
    css_text = (ROOT / 'gurps.css').read_text(encoding='utf-8')
    css_paths = []
    CSS_DIR.mkdir(parents=True, exist_ok=True)
    for filename, start_marker, end_marker in CSS_MARKERS:
        content = extract_segment(css_text, start_marker, end_marker)
        target = CSS_DIR / filename
        target.write_text(content, encoding='utf-8')
        css_paths.append(f'css/{filename}')
    return css_paths


def write_manifest(html_paths: list[str], css_paths: list[str]):
    manifest = {
        'outputs': {
            'html': {
                'input': html_paths,
                'output': '../gurps.html',
                'description': 'HTML is split into stable section files to preserve the original final output order.',
            },
            'css': {
                'input': css_paths,
                'output': '../gurps.css',
                'description': 'CSS is split into stable section files to preserve the original final output ordering.',
            },
        }
    }
    (SRC / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    html_paths = write_html_sections()
    css_paths = write_css_sections()
    write_manifest(html_paths, css_paths)
    print('HTML parts:', html_paths)
    print('CSS parts:', css_paths)
    print('Manifest updated:', SRC / 'manifest.json')
