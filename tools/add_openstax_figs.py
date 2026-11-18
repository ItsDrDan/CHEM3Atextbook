#!/usr/bin/env python3
"""Insert OpenStax Chemistry 2e figures (CC BY 4.0, LibreTexts copy) into Chapters 10, 11 and 14 (2026-11-18), then
renumber every figure caption on the touched pages in order. Idempotent: a figure whose image is already on the page is
skipped. Images are hosted in figures/openstax/ (downloaded from the LibreTexts copy, compressed)."""
import re, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BASE = 'https://itsdrdan.github.io/CHEM3Atextbook/figures/openstax/'
OS = 'https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/'

def credit(sec, path, extra=''):
    e = f'; {extra}' if extra else ''
    return (f'(From <a href="{OS}{path}" target="_blank" rel="noopener">OpenStax, <i>Chemistry 2e</i>, Section {sec}</a>, '
            f'CC BY 4.0{e}.)')

FIGS = [
 # (page, anchor text that ends the paragraph to insert after, image, lead-in sentence or '', alt, caption, credit)
 ('ch10/10.2_pressure.html', 'and 1 atm = 101,325 Pa are exact; 14.7 psi is rounded to 3 significant figures.</p>',
  'os_9-2_sphygmomanometer.jpg',
  '<p>Blood pressure is the most common pressure measurement in health care, and it is still reported in mmHg, the unit of the first mercury instruments.</p>',
  'Two photographs. (a) A medical technician in a white coat and stethoscope wraps an inflatable cuff around a seated patient&rsquo;s upper arm and holds the pressure gauge. (b) A sphygmomanometer laid out on a table: the fabric cuff, a rubber squeeze bulb with a valve, a round dial gauge, and a stethoscope.',
  'Measuring blood pressure. (a) A medical technician prepares to measure a patient&rsquo;s blood pressure. (b) A sphygmomanometer: a rubber bulb inflates the cuff, and the dial gauge reads the pressure in mmHg.',
  credit('9.1', '09%3A_Gases/9.02%3A_Gas_Pressure', 'photo a: modification of work by Master Sgt. Jeffrey Allen')),
 ('ch11/11.3_concentration.html', None, 'os_3-5_saline_glucometer.jpg', '',
  'Two photographs. (a) A hand holds a clear plastic IV bag whose printed label reads 0.9% Sodium Chloride Injection. (b) A blood glucose meter in one hand, with a test strip inserted, next to a patient-details form on a table; another hand holds a pricked fingertip to the strip.',
  'Mass/volume units in health care. (a) Normal saline is 0.9% (m/v) NaCl. (b) A glucose meter reports blood glucose in mg/dL; a typical fasting range is about 70&ndash;100 mg/dL.',
  credit('3.4', '03%3A_Composition_of_Substances_and_Solutions/3.05%3A_Other_Units_for_Solution_Concentrations',
         'photo a: modification of work by &ldquo;The National Guard&rdquo;/Flickr; photo b: modification of work by Biswarup Ganguly')),
 ('ch11/11.6_colligative.html', None, 'os_11-5_osmosis.jpg', '',
  'Two U-shaped tubes, each split at the bottom by a semipermeable membrane, with pure solvent (small particles only) in the left arm and a solution (small solvent particles plus larger solute particles) in the right arm. (a) At the start both liquid levels are equal; arrows show solvent crossing the membrane. (b) Later the liquid in the solution arm has risen above the pure-solvent arm; the difference in height is labeled osmotic pressure.',
  'Osmosis. (a) Pure solvent and a solution are separated by a semipermeable membrane; only solvent can cross. (b) Solvent moves into the solution until the extra height of the solution, a measure of its osmotic pressure, makes the flow equal in both directions.',
  credit('11.4', '11%3A_Solutions_and_Colloids/11.05%3A_Colligative_Properties')),
 ('ch14/14.6_radiation_health.html', None, 'os_21-7_exposure_sources.jpg', '',
  'Bar graph titled Radiation Doses and Regulatory Limits, in millirems, on a broken vertical axis. Green bars are limits: annual nuclear worker limit 5,000; annual public limit 100. Blue bars are doses: whole-body CT 1,000; average US annual dose 620; average natural background 310; from your own body 40; cosmic rays 30; chest X-ray 10; EPA safe drinking water limit 4; trans-Atlantic flight 2.5.',
  'Typical radiation doses and limits in the United States, in millirems (100 mrem = 1 mSv). The average total is about 620 mrem (6.2 mSv) a year; natural background, about 310 mrem (3.1 mSv), is about half of it, and most of the rest is medical imaging. A chest X-ray is about 10 mrem (0.1 mSv).',
  credit('21.6', '21%3A_Nuclear_Chemistry/21.07%3A_Biological_Effects_of_Radiation', 'data: U.S. Nuclear Regulatory Commission')),
 ('ch14/14.6_radiation_health.html', None, 'os_21-7_radon_house.png', '',
  'Cutaway drawing of a house over layers of soil, bedrock, fractured bedrock and groundwater, with the decay chain U-238 to radium-226 to radon-222 written at the bottom. Green arrows show radon rising from the soil and through cracks in the basement and foundation, through the drain, and from well water into the water heater and shower. An inset shows radon decay products being inhaled into the lungs, where an alpha particle damages DNA.',
  'How radon gets into a home. Uranium-238 in rock decays to radium-226 and then to radon-222, a gas that seeps through cracks and openings in foundations and can enter from well water. Breathed in, radon and its decay products give off alpha particles inside the lungs.',
  credit('21.6', '21%3A_Nuclear_Chemistry/21.07%3A_Biological_Effects_of_Radiation')),
 ('ch14/14.6_radiation_health.html', None, 'os_21-7_detectors.jpg',
  '<p>To know a dose, you have to measure it. A Geiger counter clicks or reads out when radiation passes through its probe; a scintillation detector, in which radiation makes a crystal give off flashes of light, is the heart of a gamma camera; and anyone who works with radiation wears a personal dosimeter that records their total dose.</p>',
  'Three photographs. (a) A Geiger counter: a box-shaped meter with a needle dial, connected by a cable to a round hand-held probe. (b) Several cylindrical scintillation detectors and a long rectangular crystal. (c) A hand holds a small digital dosimeter outdoors on a sidewalk; its display reads 0.532.',
  'Instruments that measure radiation: (a) a Geiger counter, (b) scintillation detectors, and (c) a personal dosimeter.',
  credit('21.6', '21%3A_Nuclear_Chemistry/21.07%3A_Biological_Effects_of_Radiation', 'photo c: modification of work by &ldquo;osaMu&rdquo;/Wikimedia Commons')),
 ('ch14/14.7_medicine.html', None, 'os_21-6_tc99m_generator.jpg', '',
  'Two images. (a) A black-and-white photograph of an early technetium generator: a hand pours liquid from a graduated cylinder into a glass column clamped above a collection vial. (b) A thyroid scan on a black background: scattered red and orange dots form two bright lobes near the top and a bright patch below, showing where the tracer collected in the neck.',
  'Technetium-99m in practice. (a) The first technetium generator (about 1958): molybdenum-99 stays on the column, and the technetium-99m it decays into is rinsed off and collected. (b) A thyroid scan made with technetium-99m; the bright areas show where an overactive thyroid (Graves&rsquo; disease) took up the tracer.',
  credit('21.5', '21%3A_Nuclear_Chemistry/21.06%3A_Uses_of_Radioisotopes',
         'image a: modification of work by the Department of Energy; image b: modification of work by &ldquo;MBq&rdquo;/Wikimedia Commons')),
 ('ch14/14.7_medicine.html', None, 'os_21-4_pet_scan.jpg', '',
  'Three images. (a) A PET scanner in a hospital room: a large ring-shaped machine with a padded patient table that slides through the opening. (b) A color PET image of a healthy brain seen from above, with large areas of red and yellow showing high glucose use. (c) A PET image of a brain with Alzheimer&rsquo;s disease, mostly blue and purple with only small spots of red and yellow.',
  'Positron emission tomography (PET). (a) A PET scanner. (b) A PET scan of a healthy brain: red and yellow mark regions using a lot of glucose (FDG). (c) A PET scan from a person with Alzheimer&rsquo;s disease shows much lower activity.',
  credit('21.3', '21%3A_Nuclear_Chemistry/21.04%3A_Radioactive_Decay', 'photo a: modification of work by Jens Maus')),
]
# anchors for figures whose anchor is None: insert after the first paragraph containing this text
AFTER = {
 'os_3-5_saline_glucometer.jpg': '</strong>, %(m/v), is grams of solute per 100 mL of solution',
 'os_11-5_osmosis.jpg': 'Build the idea in two steps.',
 'os_21-7_exposure_sources.jpg': 'Everyone is exposed to <strong>background radiation</strong>',
 'os_21-7_radon_house.png': '<p class="boxtitle">Valley Connection: Radon in Tulare County Homes</p>',
 'os_21-7_detectors.jpg': 'Time, Distance, and Shielding</h2>',
 'os_21-6_tc99m_generator.jpg': '(half-life 6.0 h) is used in most nuclear medicine scans',
 'os_21-4_pet_scan.jpg': '</strong>, the tracer is usually <strong>fluorine-18',
}

def block(img, alt, cap, cred):
    return (f'<figure class="figure"><img src="{BASE}{img}" alt="{alt}" style="max-width:100%;height:auto;" />\n'
            f'<figcaption>Figure \\(\\PageIndex{{0}}\\): {cap} {cred}</figcaption></figure>\n')

touched = set()
for page, anchor, img, lead, alt, cap, cred in FIGS:
    p = os.path.join(R, 'drafts', page); s = open(p).read()
    if BASE + img in s: continue
    if anchor is None:
        key = AFTER[img]; i = s.find(key); assert i >= 0 and s.count(key) == 1, (page, key)
        if key.startswith('<p class="boxtitle">'):            # put the figure just after the box
            j = s.find('</div>', i); ins = s.find('\n', j) + 1
        elif key.endswith('</h2>'):                           # put it after the section's last list/figure block
            j = s.find('</figure>', i); ins = s.find('\n', j) + 1
        else:
            cands = [(s.find(t, i), t) for t in ('</p>', '</ul>') if s.find(t, i) >= 0]
            k, t = min(cands); ins = k + len(t) + 1
    else:
        assert s.count(anchor) == 1, (page, anchor); ins = s.find(anchor) + len(anchor) + 1
    s = s[:ins] + lead + ('\n' if lead else '') + block(img, alt, cap, cred) + s[ins:]
    open(p, 'w').write(s); touched.add(p); print('added', img, 'to', page)

for p in touched:   # renumber captions in page order
    s = open(p).read(); n = [0]
    def num(m):
        n[0] += 1; return f'<figcaption>Figure \\(\\PageIndex{{{n[0]}}}\\):'
    s = re.sub(r'<figcaption>Figure \\\(\\PageIndex\{\d+\}\\\):', num, s); open(p, 'w').write(s)
    print(os.path.basename(p), n[0], 'figures')
