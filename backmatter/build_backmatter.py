#!/usr/bin/env python3
"""Build LibreTexts back matter for the CHEM 3A Revision Draft from glossary_3A.json and index_3A.json.

Outputs (in this folder):
  glossary_page.html  - body for the book's Glossary page: the LibreTexts glossary table
                        (Word(s) | Definition | Image | Caption | Link | Source), same format as the CHEM 3B book.
  index_tags.json     - {page_id: [tag, ...]} plan for the Index. LibreTexts builds the printed Index from page tags,
                        so each term is added as a tag on the pages listed in index_3A.json.
                        Hyphenated terms also get an en-dash copy (the CHEM 3B print build dropped hyphen tags).
Nothing is uploaded. Section -> page id map below comes from CLAUDE.md / REORDER notes and must be checked against
the live Workbench tree (GET pages/{book}/tree) before any write.
"""
import json, os, html, collections
HERE = os.path.dirname(os.path.abspath(__file__))

IDS = {'1.1': 597677, '1.2': 597495, '1.2.1': 597593, '1.2.2': 597594, '1.3': 597496, '1.3.1': 597595,
       '1.3.2': 597596, '1.4': 597497, '1.4.1': 597597, '1.4.2': 597598, '1.4.3': 597599, '1.5': 597678,
       '1.6': 597679, '1.7': 597680, '1.8': 597681, '1.9': 597682, '1.9.1': 597498, '1.10': 597683,
       '1.11': 597684, '1.12': 597500, '1.13': 597685}
def run(ch, first_id, n):
    for i in range(1, n + 1): IDS[f'{ch}.{i}'] = first_id + i - 1
for ch, fid, n in [(2, 597862, 9), (3, 597878, 9), (4, 597891, 9), (5, 597906, 7), (6, 597922, 11), (7, 597944, 12),
                   (8, 597962, 9), (9, 597980, 11), (10, 597999, 9), (11, 598016, 9), (12, 598030, 9), (13, 598045, 8)]:
    run(ch, fid, n)
IDS.update({'14.1': 598058, '14.2': 598059, '14.3': 598060, '14.4': 598061, '14.5': 598062, '14.6': 598063,
            '14.7': 598071, '14.8': 598064, '14.9': 598065, '14.10': 598066})

def skey(s): return [int(x) for x in s.split('.')]

G = json.load(open(os.path.join(HERE, 'glossary_3A.json')))
X = json.load(open(os.path.join(HERE, 'index_3A.json')))

rows = []
for g in sorted(G, key=lambda g: g['term'].lower()):
    words = ', '.join([g['term']] + g.get('synonyms', []))
    sec = g['section']; pid = IDS[sec]
    tag = ' (Going Further, not on CHEM 3A exams)' if g.get('going_further') else ''
    rows.append(f'<tr><td data-th="Word(s)">{words}</td><td data-th="Definition">{g["definition"]}</td>'
                f'<td data-th="Image">&nbsp;</td><td data-th="Caption">&nbsp;</td>'
                f'<td data-th="Link"><a href="/@go/page/{pid}">Section {sec}</a>{tag}</td>'
                f'<td data-th="Source">CC BY 4.0; Daniel Kwasniewski</td></tr>')
page = ('<p>Key terms from the 14 chapters of this book, with the section where each is taught. Definitions are written from '
        'the book\'s own text (CC BY 4.0, Daniel Kwasniewski). Terms marked Going Further come from optional sections.</p>\n'
        '<table class="mt-responsive-table"><thead><tr><th>Word(s)</th><th>Definition</th><th>Image</th><th>Caption</th>'
        '<th>Link</th><th>Source</th></tr></thead><tbody>\n' + '\n'.join(rows) + '\n</tbody></table>\n')
open(os.path.join(HERE, 'glossary_page.html'), 'w').write(page)

tags = collections.defaultdict(set)
for e in X:
    t = html.unescape(e['term']).replace('<sub>', '').replace('</sub>', '').replace('<sup>', '').replace('</sup>', '')
    for s in e['sections']:
        tags[IDS[s]].add(t)
        if '-' in t: tags[IDS[s]].add(t.replace('-', '–'))
plan = {str(k): sorted(v, key=str.lower) for k, v in sorted(tags.items())}
json.dump(plan, open(os.path.join(HERE, 'index_tags.json'), 'w'), ensure_ascii=False, indent=1)
missing = sorted({s for e in X for s in e['sections']} - set(IDS), key=skey)
print('glossary rows', len(rows), '| index pages', len(plan), '| tags', sum(len(v) for v in plan.values()), '| unmapped sections', missing)
