#!/usr/bin/env python3
"""Give every <td> in a .mt-responsive-table a data-th="<column header>" attribute, so LibreTexts can label
stacked cells on phones (its CSS shows attr(data-th) before each cell below 37.5em). Row-header <th scope="row">
cells are left alone. Idempotent.  python3 tools/add_data_th.py drafts/ch01/*.html drafts/ch02/*.html"""
import re, sys, html
def strip(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s))).strip()
def fix_table(t):
    m=re.search(r'<thead>(.*?)</thead>',t,re.S)
    if not m: return t
    heads=[strip(h) for h in re.findall(r'<th[^>]*>(.*?)</th>',m.group(1),re.S)]
    def fix_row(rm):
        row=rm.group(0); cells=list(re.finditer(r'<(td|th)(\s[^>]*)?>',row)); out=row; shift=0
        for i,c in enumerate(cells):
            if i>=len(heads): break
            tag,attrs=c.group(1),c.group(2) or ''
            if tag=='th' or 'data-th=' in attrs: continue
            new=f'<td{attrs} data-th="{html.escape(heads[i],quote=True)}">'
            out=out[:c.start()+shift]+new+out[c.end()+shift:]; shift+=len(new)-len(c.group(0))
        return out
    body=re.search(r'<tbody>(.*?)</tbody>',t,re.S)
    if not body: return t
    nb=re.sub(r'<tr[^>]*>.*?</tr>',fix_row,body.group(1),flags=re.S)
    return t[:body.start(1)]+nb+t[body.end(1):]
STYLE='<style type="text/css">@media (max-width: 37.49em) { .mt-content-container .mt-responsive-table td[data-th] { padding-left: 9.5em !important; } }</style>'
# LibreTexts' site rule ".mt-content-container table td {padding:.4em !important}" hides the stacked-cell labels on phones;
# this page-level rule (phones only, placed right before the first table, never at position 0 or inside <p>) restores the label column.
for f in sys.argv[1:]:
    s=open(f).read()
    n=re.sub(r'<table class="mt-responsive-table".*?</table>',lambda m:fix_table(m.group(0)),s,flags=re.S)
    if 'data-th=' in n and STYLE not in n:
        i=n.index('<table class="mt-responsive-table"')
        # put it before the paragraph/box that holds the table's lead-in, at a block boundary
        n=n[:i]+STYLE+'\n'+n[i:]
    if n!=s: open(f,'w').write(n); print('updated',f,n.count('data-th='))
