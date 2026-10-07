"""Static checks only; cloud and framework integration remain separate gates."""
from pathlib import Path
import ast
import base64
from html.parser import HTMLParser
import json
import re
import subprocess
import xml.etree.ElementTree as ET
import yaml

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / 'books.json').read_text())
sources = {}
counts = dict(chapters=0, words=0, code_blocks=0, mermaid_blocks=0, images=0)

class ReaderCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.images = set(), [], 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.links.append(attrs['href'][1:])
        if tag == 'img':
            assert attrs['src'].startswith('data:image/svg+xml;base64,')
            ET.fromstring(base64.b64decode(attrs['src'].split(',', 1)[1]))
            self.images += 1

for entry in config:
    md = ROOT / (entry['name'] + '.md')
    text = md.read_text()
    assert '{{code:' not in text
    assert sum(line.startswith('```') for line in text.splitlines()) % 2 == 0
    counts['chapters'] += len(re.findall(r'^## ', text, re.M))
    counts['words'] += len(text.split())
    for language, block in re.findall(r'(?ms)^```([^\n]*)\n(.*?)^```\s*$', text):
        counts['code_blocks'] += 1
        if language == 'json': json.loads(block)
        if language == 'yaml': list(yaml.safe_load_all(block))
        if language == 'xml': ET.fromstring(block)
        if language == 'mermaid':
            counts['mermaid_blocks'] += 1
            assert block.splitlines()[0] in {'flowchart TD', 'sequenceDiagram', 'stateDiagram-v2'}
            assert '%%{init' not in block
            # Structure only: no Mermaid engine is installed.
        if language == 'http':
            for line in block.splitlines():
                if line.startswith('{') and line.endswith('}'):
                    json.loads(line)
    for label, url in re.findall(r'(?<!!)\[([^\]]+)\]\((https?://[^)]+)\)', text):
        sources.setdefault(url, {'label': label, 'guides': set()})['guides'].add(entry['name'])
    expected_images = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)
    for image in expected_images: assert (ROOT / image).is_file(), image
    reader = ReaderCheck()
    reader.feed((ROOT / (entry['name'] + '.html')).read_text())
    assert all(link in reader.ids for link in reader.links)
    assert reader.images == len(expected_images)
    counts['images'] += reader.images

python_files = list((ROOT / 'code').rglob('*.py')) + list((ROOT / 'delivery').glob('*.py')) + list((ROOT / 'learning_labs').glob('*.py'))
for file in python_files: ast.parse(file.read_text(), filename=str(file))
for file in list((ROOT / 'code').rglob('*.yml')) + list((ROOT / 'code').rglob('*.yaml')):
    list(yaml.safe_load_all(file.read_text()))
ET.parse(ROOT / 'code/spring/pom.xml')
for file in (ROOT / 'images').glob('*.svg'): ET.parse(file)
shell_files = list((ROOT / 'delivery').glob('*.sh'))
for file in shell_files: subprocess.run(['bash', '-n', str(file)], check=True)
counts.update(primary_sources=len(sources), python_sources=len(python_files), shell_sources=len(shell_files))
source_lines = ['# Primary-source index', '', 'Original research: 16–17 September 2026; selected Spring AI/MCP version references refreshed 7 October 2026. Inline links appear beside the supported claims. Calculations, scenarios and diagrams are original teaching examples; they are not vendor benchmark claims.', '']
for i, (url, entry) in enumerate(sorted(sources.items()), 1):
    source_lines.append(f"{i}. [{entry['label']}]({url}) — {', '.join(sorted(entry['guides']))}")
(ROOT / 'SOURCES.md').write_text('\n'.join(source_lines) + '\n')
(ROOT / 'validation_counts.json').write_text(json.dumps(counts, indent=2) + '\n')
print(json.dumps(counts, indent=2))
