const fs = require('fs');
const path = require('path');
const modules = process.env.ATLAS_NODE_MODULES || path.join(__dirname, 'node_modules');
const { marked } = require(path.join(modules, 'marked'));
const sharp = require(path.join(modules, 'sharp'));
const root = __dirname;
const escape = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');

async function build() {
  const images = path.join(root, 'images');
  for (const file of fs.readdirSync(images).filter(f => f.endsWith('.svg'))) {
    await sharp(path.join(images, file)).png().toFile(path.join(images, file.replace('.svg', '.png')));
  }
  const css = fs.readFileSync(path.join(root, 'reader.css'), 'utf8');
  const config = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
  for (const book of config) {
    const source = fs.readFileSync(path.join(root, book.name + '.md'), 'utf8');
    let chapters = [];
    let transformed = source.replace(/^## (.+)$/gm, (_, title) => {
      const id = `chapter-${chapters.length + 1}`;
      chapters.push({id, title});
      return `<h2 id="${id}">${escape(title)}</h2>`;
    });
    let html = marked.parse(transformed);
    html = html.replace(/src="images\/([^\"]+)"/g, (_, name) => {
      const file = path.join(images, name.replace(/\.png$/, '.svg'));
      return `src="data:image/svg+xml;base64,${fs.readFileSync(file).toString('base64')}"`;
    });
    html = html.replace(/<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g,
      '<details class="diagram-source"><summary>Editable Mermaid diagram source</summary><pre><code>$1</code></pre></details>');
    html = html.replace(/<table>/g, '<div class="table-scroll"><table>').replace(/<\/table>/g, '</table></div>');
    const nav = `<details open><summary>Chapters</summary><ol>${chapters.map(c => `<li><a href="#${c.id}">${escape(c.title)}</a></li>`).join('')}</ol></details>`;
    const words = source.trim().split(/\s+/).length;
    const figures = (source.match(/!\[/g) || []).length;
    const output = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escape(book.title)}</title><style>${css}</style></head>
<body><div id="progress"></div><header class="top"><strong>ATLAS / ENGINEERING GUIDES</strong><span class="date">Learning edition · 7 October 2026</span><button onclick="window.print()">Print / save PDF</button></header>
<div class="layout"><nav aria-label="Chapters">${nav}<p>Use your browser's Find command to search this guide.</p></nav>
<main><section class="cover"><div class="eyebrow">SENIOR BACKEND ENGINEERING SERIES</div><h1>${escape(book.title)}</h1><p>${escape(book.subtitle)}</p>
<div class="chips"><span>${chapters.length} chapters</span><span>${words.toLocaleString()} words including examples</span><span>${figures} embedded illustrations</span><span>Primary-source references</span></div></section>
<section class="start"><strong>How to use this edition.</strong> Read the worked example, trace the failure path, then rebuild the design without looking. Click an illustration to enlarge it. Mermaid source remains available for editing. Runnable labs, Markdown and delivery templates are in the learning-guides directory. Open index.html to switch guides. Examples distinguish executed local checks from integrations that require your own services.</section>
<article>${html}</article><footer class="foot">Original teaching examples and diagrams. Original research: 16–17 September 2026. Spring AI and MCP version references refreshed 7 October 2026. Cloud, model and framework integrations were not executed; see VALIDATION.md in this directory for exact checks.</footer></main></div>
<script>document.querySelectorAll('article img').forEach(img=>{img.tabIndex=0;img.addEventListener('click',()=>img.classList.toggle('zoom'));img.addEventListener('keydown',e=>{if(e.key==='Enter')img.classList.toggle('zoom')})});document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('img.zoom').forEach(i=>i.classList.remove('zoom'))});window.addEventListener('scroll',()=>{const d=document.documentElement;document.getElementById('progress').style.width=(d.scrollHeight>d.clientHeight?100*d.scrollTop/(d.scrollHeight-d.clientHeight):0)+'%'},{passive:true});</script></body></html>`;
    fs.writeFileSync(path.join(root, book.name + '.html'), output);
    console.log(`${book.name}: ${chapters.length} chapters, ${words} words, ${figures} illustrations`);
  }
}
build().catch(error => { console.error(error); process.exit(1); });
