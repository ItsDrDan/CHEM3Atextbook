#!/usr/bin/env python3
"""Accessibility Conformance Report (WCAG 2.1 A/AA, VPAT style), 2026-11-19.
Fills drafts/front/accessibility_conformance_report.html from the template placeholders and the test results below.
Edit the RESULTS and ROWS when a test is rerun, then run: python3 tools/build_acr.py"""
import os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(R)
T = 'tools/acr_template.html'; OUT = 'drafts/front/accessibility_conformance_report.html'

RESULTS = dict(PAGES='163', IMGS='140', TABLES='186', IFRAMES='336', VIDEOS='107', DATE='November 19, 2026')
S, P, NA = 'Supports', 'Partially supports', 'Not applicable'
PLAT = ' (LibreTexts platform)'
ROWS = [
 ('1.1.1 Non-text Content', 'A', S, 'Every image has alternative text that gives its content, not just its name; data figures describe their values. Pictures inside practice questions (cylinders, burets, rulers, balances, targets) describe what a sighted reader sees. Embedded frames have titles.'),
 ('1.2.1 Audio-only and Video-only (Prerecorded)', 'A', NA, 'The book has no audio-only or video-only media.'),
 ('1.2.2 Captions (Prerecorded)', 'A', P, '106 of the 107 embedded videos have uploaded English captions. One video, &ldquo;Properties of Intermolecular Forces (Part 4),&rdquo; used in Sections 9.1, 9.7, 9.8 and 9.9, has only YouTube&rsquo;s automatic captions.'),
 ('1.2.3 Audio Description or Media Alternative (Prerecorded)', 'A', S, 'The videos are optional lectures. Each section&rsquo;s text, worked examples, and figures teach the same content, so the page itself is the media alternative.'),
 ('1.2.4 Captions (Live)', 'AA', NA, 'The book has no live media.'),
 ('1.2.5 Audio Description (Prerecorded)', 'AA', P, 'The videos have no separate audio-description track. The worked steps written on screen in the videos are given in the section text and Chapter Guides, which cover the same material.'),
 ('1.3.1 Info and Relationships', 'A', S, 'Headings, lists, and tables are marked up as such; every data table has header cells and a caption or lead-in sentence; hidden hints and answers use the standard details/summary disclosure; math is real text (MathJax) with speech support.'),
 ('1.3.2 Meaningful Sequence', 'A', S, 'Reading order in the code matches the visual order; boxes and figures follow the text they belong to.'),
 ('1.3.3 Sensory Characteristics', 'A', S, 'Instructions do not depend on shape, color, size, or position alone.'),
 ('1.3.4 Orientation', 'AA', S, 'Pages and practice boxes work in portrait and landscape.'),
 ('1.3.5 Identify Input Purpose', 'AA', NA, 'The book collects no personal information.'),
 ('1.4.1 Use of Color', 'A', S, 'Meaning is never carried by color alone; links in gray captions are underlined; right and wrong answers in Try It boxes are marked with words and icons as well as color.'),
 ('1.4.2 Audio Control', 'A', S, 'No audio plays automatically.'),
 ('1.4.3 Contrast (Minimum)', 'AA', S, 'Page text and the Try It boxes meet 4.5:1 (measured in every state). Text drawn inside figures is dark on light, and its content is also in the alternative text and caption.'),
 ('1.4.4 Resize Text', 'AA', S, 'Text can be enlarged to 200% with browser zoom without loss of content.'),
 ('1.4.5 Images of Text', 'AA', S, 'Formulas and equations are text, not pictures. Labels inside diagrams are part of the diagram, and the diagram&rsquo;s text is repeated in its description.'),
 ('1.4.10 Reflow', 'AA', '__REFLOW_LEVEL__', '__REFLOW__'),
 ('1.4.11 Non-text Contrast', 'AA', S, 'Answer buttons, selected and checked states, and the keyboard focus ring meet 3:1 (the focus ring is 6.7:1 or more).'),
 ('1.4.12 Text Spacing', 'AA', '__SPACING_LEVEL__', '__SPACING__'),
 ('1.4.13 Content on Hover or Focus', 'AA', P, 'The book&rsquo;s own content shows nothing on hover. The glossary pop-ups that LibreTexts adds to defined words' + PLAT + ' open on hover or tap and cannot be dismissed with the keyboard; the same definitions are on the Glossary page and in each Chapter Guide&rsquo;s Key Terms table.'),
 ('2.1.1 Keyboard', 'A', P, 'All book content, links, hint and answer disclosures, and Try It boxes work from the keyboard (Tab to a choice, Space to select, Enter to check). The glossary pop-ups' + PLAT + ' open with a mouse or touch only.'),
 ('2.1.2 No Keyboard Trap', 'A', S, 'Keyboard focus can move into and out of every practice box and embedded frame.'),
 ('2.1.4 Character Key Shortcuts', 'A', S, 'The book uses no single-character keyboard shortcuts.'),
 ('2.2.1 Timing Adjustable', 'A', S, 'Nothing in the book is timed. The optional study games have no required timed mode.'),
 ('2.2.2 Pause, Stop, Hide', 'A', S, 'Nothing moves, blinks, or updates on its own; videos play only when started.'),
 ('2.3.1 Three Flashes or Below Threshold', 'A', S, 'No content flashes.'),
 ('2.4.1 Bypass Blocks', 'A', S, 'Pages use headings for every section, and LibreTexts provides landmark regions and a table of contents' + PLAT + '.'),
 ('2.4.2 Page Titled', 'A', S, 'Every page has a numbered, descriptive title.'),
 ('2.4.3 Focus Order', 'A', S, 'Focus moves in reading order; after an answer is checked in a Try It box, focus moves to the next control in the box.'),
 ('2.4.4 Link Purpose (In Context)', 'A', S, 'Link text says where the link goes; there are no &ldquo;click here&rdquo; links.'),
 ('2.4.5 Multiple Ways', 'AA', S, 'Pages can be reached from the table of contents, search' + PLAT + ', the Index, the Glossary, and cross-references.'),
 ('2.4.6 Headings and Labels', 'AA', S, 'Headings describe their sections and never skip a level; box titles name the box (Example, Exercise, Professor Tip, Try It, and so on).'),
 ('2.4.7 Focus Visible', 'AA', S, 'The browser focus ring shows on all book links and controls; the Try It boxes add a high-contrast ring.'),
 ('2.5.1 Pointer Gestures', 'A', S, 'Everything works with a single tap or click; the interactive labs that use dragging also accept tap-to-place.'),
 ('2.5.2 Pointer Cancellation', 'A', S, 'Actions happen on release (standard buttons and links).'),
 ('2.5.3 Label in Name', 'A', S, 'Visible labels match the accessible names of controls.'),
 ('2.5.4 Motion Actuation', 'A', NA, 'Nothing responds to device motion.'),
 ('3.1.1 Language of Page', 'A', S, 'Pages and the PDF declare English.'),
 ('3.1.2 Language of Parts', 'AA', S, 'The text is in English; there are no passages in other languages.'),
 ('3.2.1 On Focus', 'A', S, 'Focusing a control never changes the page.'),
 ('3.2.2 On Input', 'A', S, 'Selecting an answer does not submit it; the student checks it with a separate button.'),
 ('3.2.3 Consistent Navigation', 'AA', S, 'Navigation is the same on every page' + PLAT + '.'),
 ('3.2.4 Consistent Identification', 'AA', S, 'Boxes, buttons, and links that do the same thing are named the same way throughout the book.'),
 ('3.3.1 Error Identification', 'A', S, 'A wrong answer in a Try It box is identified in text and announced to screen readers.'),
 ('3.3.2 Labels or Instructions', 'A', S, 'Every practice box and question has instructions.'),
 ('3.3.3 Error Suggestion', 'AA', S, 'Each wrong answer choice explains the likely mistake and how to fix it.'),
 ('3.3.4 Error Prevention (Legal, Financial, Data)', 'AA', NA, 'The book has no legal, financial, or data-submission transactions.'),
 ('4.1.1 Parsing', 'A', S, 'The page code is checked for unclosed and mis-nested elements.'),
 ('4.1.2 Name, Role, Value', 'A', P, 'All book controls have correct names and roles (automated scan: no failures in book content). The glossary pop-up markup that LibreTexts adds' + PLAT + ' uses an ARIA attribute that is not allowed on its element.'),
 ('4.1.3 Status Messages', 'AA', S, 'Try It feedback is announced through a polite live region without moving focus.'),
]
ISSUES = [
 'Captions (planned): the one video with only automatic captions, &ldquo;Properties of Intermolecular Forces (Part 4),&rdquo; is to get reviewed, uploaded captions.',
 'Glossary pop-ups' + PLAT + ': this is a LibreTexts issue the book cannot change; the definitions are available from the keyboard on the Glossary page and in each Chapter Guide&rsquo;s Key Terms table.',
 'A listening test with a screen reader (VoiceOver) on pages with math and practice boxes is planned; the automated checks confirm names, roles, and structure but not how a page sounds.',
]

def main(reflow, reflow_level, spacing, spacing_level, summary):
    s = open(T).read()
    rows = '\n'.join(f'<tr><td data-th="Criterion">{c}</td><td data-th="Level">{l}</td><td data-th="Conformance">{k}</td><td data-th="Remarks">{r}</td></tr>' for c, l, k, r in ROWS)
    rows = rows.replace('__REFLOW_LEVEL__', reflow_level).replace('__REFLOW__', reflow).replace('__SPACING_LEVEL__', spacing_level).replace('__SPACING__', spacing)
    for k, v in RESULTS.items(): s = s.replace(f'__{k}__', v)
    s = s.replace('__ROWS__', rows).replace('__ISSUES__', '\n'.join(f'<li>{i}</li>' for i in ISSUES)).replace('__SUMMARY__', summary)
    assert '__' not in s, re.findall(r'__\w+__', s)
    open(OUT, 'w').write(s)
    print('built', len(ROWS), 'criteria;', sum(r[2] == S for r in ROWS), 'supports')

if __name__ == '__main__':
    import json, sys
    main(**json.load(open(sys.argv[1])))
