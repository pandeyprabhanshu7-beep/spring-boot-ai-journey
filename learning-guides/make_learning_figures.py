from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parent
IMAGES=ROOT/"images"
IMAGES.mkdir(exist_ok=True)
COLORS = {"blue":("#eaf2ff", "#255bb2"), "teal":("#e3f6f2", "#117f74"),
          "purple":("#f0ebfc", "#7650ac"), "orange":("#fff0dc", "#a6691b")}

def render(name, title, subtitle, nodes, edges):
    width, bw, bh = 1400, 386, 104
    row_gap = 180
    rows = max(n[2] for n in nodes) + 1
    height = 210 + rows * row_gap
    positions = {n[0]:(60+n[1]*445, 150+n[2]*row_gap) for n in nodes}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
      '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#708096"/></marker></defs>',
      f'<rect width="{width}" height="{height}" rx="24" fill="#f8fafc"/>',
      f'<text x="60" y="62" font-family="DejaVu Sans, sans-serif" font-size="32" font-weight="700" fill="#172b45">{escape(title)}</text>',
      f'<text x="60" y="104" font-family="DejaVu Sans, sans-serif" font-size="21" fill="#53657b">{escape(subtitle)}</text>']
    for source,target,label in edges:
        x1,y1=positions[source]; x2,y2=positions[target]
        if y1 == y2:
            forward=x2>x1
            sx,sy=x1+(bw if forward else 0),y1+bh/2
            tx,ty=x2+(0 if forward else bw),y2+bh/2
            path=f'M {sx} {sy} L {tx} {ty}'
            lx,ly=(sx+tx)/2,sy-12
            if abs(tx-sx) < 130:
                label=""  # Tight adjacent boxes: node titles carry the relationship.
        else:
            down=y2>y1
            sx,sy=x1+bw/2,y1+(bh if down else 0)
            tx,ty=x2+bw/2,y2+(0 if down else bh)
            mid=(sy+ty)/2
            path=f'M {sx} {sy} C {sx} {mid}, {tx} {mid}, {tx} {ty}'
            lx,ly=(sx+tx)/2,(sy+ty)/2-9
        parts.append(f'<path d="{path}" fill="none" stroke="#708096" stroke-width="2.5" marker-end="url(#arrow)"/>')
        if label:
            tw=max(65,len(label)*10+18)
            parts.append(f'<rect x="{lx-tw/2}" y="{ly-19}" width="{tw}" height="27" rx="6" fill="#f8fafc"/>')
            parts.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="17" fill="#52647a">{escape(label)}</text>')
    for ident,col,row,title_,detail,color in nodes:
        x,y=positions[ident]; bg,fg=COLORS[color]
        parts += [f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="15" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>',
                  f'<rect x="{x}" y="{y+18}" width="5" height="{bh-36}" rx="2" fill="{fg}"/>',
                  f'<text x="{x+21}" y="{y+40}" font-family="DejaVu Sans, sans-serif" font-size="23" font-weight="700" fill="#192f49">{escape(title_)}</text>',
                  f'<text x="{x+21}" y="{y+75}" font-family="DejaVu Sans, sans-serif" font-size="17" fill="#4b6075">{escape(detail)}</text>']
    parts.append(f'<text x="60" y="{height-27}" font-family="DejaVu Sans, sans-serif" font-size="16" fill="#78889a">ATLAS ENGINEERING GUIDES  /  {escape(name.upper().replace("_"," "))}</text></svg>')
    (IMAGES / f"{name}.svg").write_text("\n".join(parts))


FIGURES = {'learning_transformer': ('Transformer: matching and information mixing', 'A conceptual block; exact normalization and layer order vary by model.', [('x', 1, 0, 'Token states', 'Embeddings and position information', 'blue'), ('q', 0, 1, 'Queries and keys', 'Learned matching projections', 'teal'), ('v', 2, 1, 'Values', 'Learned information projections', 'purple'), ('w', 0, 2, 'Attention weights', 'Scaled scores, mask and softmax', 'teal'), ('m', 1, 3, 'Weighted mixture', 'Combine contributions from values', 'purple'), ('f', 1, 4, 'Block update', 'Residual, normalization and FFN', 'orange')], [('x', 'q', 'project'), ('x', 'v', 'project'), ('q', 'w', 'compare'), ('w', 'm', 'weights'), ('v', 'm', 'content'), ('m', 'f', 'transform')]), 'learning_reconcile': ('A deployment is accepted before it is healthy', 'Controllers, scheduling and node startup are separate observable steps.', [('d', 0, 0, 'Desired Deployment', 'Three replicas of a verified digest', 'blue'), ('a', 1, 1, 'API and durable state', 'Authenticate, authorize and admit', 'teal'), ('c', 0, 2, 'Controllers', 'Create ReplicaSet and missing Pods', 'teal'), ('s', 2, 2, 'Scheduler', 'Choose nodes that satisfy constraints', 'purple'), ('n', 1, 3, 'Kubelet and runtime', 'Pull image and start containers', 'purple'), ('h', 1, 4, 'Observed health', 'Probes, endpoints and smoke tests', 'orange')], [('d', 'a', 'submit'), ('a', 'c', 'observe'), ('c', 's', 'unscheduled Pods'), ('s', 'n', 'assigned Pod'), ('n', 'h', 'report and verify')]), 'learning_request': ('One RAG request: keep each responsibility visible', 'The same application contracts can be implemented in Java or Python.', [('i', 1, 0, 'Identity and DTO', 'Trusted scope and bounded question', 'blue'), ('a', 1, 1, 'Admission and deadline', 'Reserve capacity for bounded work', 'teal'), ('r', 0, 2, 'Retrieval', 'Authorized passages and revisions', 'teal'), ('t', 2, 2, 'Optional tool', 'Current authorized observations', 'orange'), ('m', 1, 3, 'Model adapter', 'Messages, options and transport', 'purple'), ('v', 1, 4, 'Result validation', 'Shape, citations and domain checks', 'orange')], [('i', 'a', 'validate'), ('a', 'r', 'search'), ('a', 't', 'if required'), ('r', 'm', 'evidence'), ('t', 'm', 'result'), ('m', 'v', 'output')])}
for name, data in FIGURES.items():
    render(name, *data)
