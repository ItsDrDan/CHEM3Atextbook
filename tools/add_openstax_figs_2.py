#!/usr/bin/env python3
"""Second OpenStax figure batch (2026-11-18): Chapters 1, 2 and 12. Same pattern as add_openstax_figs.py: images from the
LibreTexts copy of OpenStax Chemistry 2e (CC BY 4.0) in figures/openstax/, our own alt text and captions, credit with a
source link, attribution sentence, captions renumbered. Idempotent."""
import re, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BASE = 'https://itsdrdan.github.io/CHEM3Atextbook/figures/openstax/'
OS = 'https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/'
ATTR = (' Figures marked &ldquo;From OpenStax&rdquo; are from <a href="https://chem.libretexts.org/Bookshelves/General_Chemistry/'
        'Chemistry_2e_(OpenStax)" target="_blank" rel="noopener">OpenStax, <i>Chemistry 2e</i></a> (CC BY 4.0), with the credits given in each caption.')

def credit(sec, path, extra=''):
    e = f'; {extra}' if extra else ''
    return f'(From <a href="{OS}{path}" target="_blank" rel="noopener">OpenStax, <i>Chemistry 2e</i>, Section {sec}</a>, CC BY 4.0{e}.)'

P13 = '01%3A_Essential_Ideas/1.04%3A_Physical_and_Chemical_Properties'
P22 = '02%3A_Atoms_Molecules_and_Ions/2.03%3A_Evolution_of_Atomic_Theory'
P23 = '02%3A_Atoms_Molecules_and_Ions/2.04%3A_Atomic_Structure_and_Symbolism'
# (page, unique anchor in the raw HTML, where: 'after' = after the paragraph/list it is in, 'afterbox' = after the box it is in,
#  image, lead-in paragraph or '', alt, caption, credit)
FIGS = [
 ('ch01/1.3.3_reading_tools.html', 'Water and most water solutions curve upward where they touch glass', 'after', 'os_1-5_meniscus.jpg', '',
  'A 25 mL graduated cylinder marked every 1 mL and labeled every 5 mL, filled with blue liquid to just above the 20 mL mark. Two enlargements zoom in on the surface: the liquid curves down in the middle, and an arrow labeled &ldquo;Make reading here&rdquo; points to the bottom of the curve, between dashed lines marking the 21 and 22 mL graduations.',
  'Reading a meniscus. Zoom in on the curved surface and read the bottom of the curve at eye level, estimating tenths of a milliliter between the 21 and 22 mL marks.',
  credit('1.5', '01%3A_Essential_Ideas/1.06%3A_Measurement_Uncertainty_Accuracy_and_Precision')),
 ('ch01/1.8_properties_and_changes.html', 'describes how a substance <em>changes into a diff', 'after', 'os_1-3_rust_chromium.jpg', '',
  'Two photographs. (a) Old iron machinery, its bars and bolts covered in flaky orange-brown rust. (b) The bright, mirror-like chrome parts of a motorcycle engine, reflecting the street around it.',
  'Chemical properties compared. (a) Iron rusts: it reacts with oxygen and water to form a new substance. (b) Chromium does not, which is why it is plated onto metal as a shiny, protective coating.',
  credit('1.3', P13, 'photo a: modification of work by Tony Hisgett; photo b: modification of work by &ldquo;Atoma&rdquo;/Wikimedia Commons')),
 ('ch01/1.8_properties_and_changes.html', 'os_1-3_rust_chromium.jpg', 'afterfig', 'os_1-3_nfpa_diamond.png',
  '<p>Chemical properties are also what hazard labels warn about. The <strong>NFPA 704 hazard diamond</strong>, posted on chemical containers and on the doors of labs, storage rooms and hospital pharmacies, rates three hazards from 0 (none) to 4 (severe): health in the blue square, flammability in the red square, and reactivity in the yellow square. The white square shows special hazards, such as OX for an oxidizer or a crossed-out W for &ldquo;do not use water.&rdquo;</p>',
  'An NFPA hazard diamond divided into four colored squares: blue (health hazard) showing 3, red (fire hazard) showing 4, yellow (reactivity) showing 2, and white (specific hazard) showing a W with a line through it. Keys explain each scale. Health: 4 deadly, 3 extreme danger, 2 hazardous, 1 slightly hazardous, 0 normal material. Fire, by flash point: 4 below 73 &deg;F, 3 below 100 &deg;F, 2 above 100 &deg;F but not above 200 &deg;F, 1 above 200 &deg;F, 0 will not burn. Reactivity: 4 may detonate, 3 shock and heat may detonate, 2 violent chemical change, 1 unstable if heated, 0 stable. Specific hazards: OX oxidizer, ACID acid, ALK alkali, COR corrosive, crossed-out W use no water, and the radiation symbol for radioactive.',
  'The NFPA 704 hazard diamond used by the National Fire Protection Association. Each colored square rates one hazard from 0 to 4; the white square lists special hazards.',
  credit('1.3', P13)),
 ('ch01/1.8_properties_and_changes.html', '(a <strong>chemical reaction</strong>) turns one or more substances into', 'after', 'os_1-3_chemical_changes.jpg', '',
  'Four photographs. (a) A flask with blue-green liquid at the bottom and orange-brown gas above it, with a few strands of copper wire inside. (b) A lit match with a bright yellow flame against a dark background. (c) Chunks of red meat browning in a pan. (d) Two bananas with yellow skins covered in brown and black spots.',
  'Everyday chemical changes. (a) Copper reacts with nitric acid to form blue copper nitrate and brown nitrogen dioxide gas. (b) A burning match: cellulose and oxygen form carbon dioxide and water vapor. (c) Cooking turns red meat brown as the iron in myoglobin is oxidized. (d) A banana browns as new substances form.',
  credit('1.3', P13, 'photo b: modification of work by Jeff Turner; photo c: modification of work by Gloria Cabada-Leman; photo d: modification of work by Roberto Verzo')),
 ('ch02/2.1_atomic_theory.html', 'In 1897 J. J. Thomson studied <strong>cathode rays</strong>', 'after', 'os_2-2_cathode_ray.jpg', '',
  'Three images. (a) A black-and-white portrait of J. J. Thomson writing at a desk. (b) An early glass cathode ray tube on a wooden stand. (c) A labeled diagram of a cathode ray tube: a cathode (negative) and anode (positive) connected to a high-voltage source at one end; a beam, the cathode ray, travels down the tube between charged plates and magnets, and bends toward the positive plate before striking a scale at the far end.',
  'Thomson&rsquo;s cathode ray experiments. (a) J. J. Thomson. (b) An early cathode ray tube (1897). (c) The beam bends toward the positive plate and in a magnetic field, which showed it was made of negatively charged particles, electrons.',
  credit('2.2', P22, 'image a: modification of work by the Nobel Foundation; image b: modification of work by Eugen Nesper; image c: modification of work by &ldquo;Kurzon&rdquo;/Wikimedia Commons')),
 ('ch02/2.1_atomic_theory.html', 'os_2-2_cathode_ray.jpg', 'afterfig', 'os_2-2_millikan.jpg',
  '<p>A few years later, in 1909, Robert Millikan measured the electron&rsquo;s charge. He sprayed tiny oil drops between two charged metal plates, gave them an electric charge, and adjusted the voltage until a drop hung still. Every drop carried a whole-number multiple of the same small charge, 1.6 &times; 10<sup>&minus;19</sup> C: the charge of one electron.</p>',
  'Left, a cutaway drawing of Millikan&rsquo;s apparatus: an atomizer sprays fine oil droplets through a pinhole into a chamber between two horizontal brass plates, the upper one positive and the lower one negative; X-rays give the droplets a charge, and a telescope eyepiece views one charged droplet. Right, a table of example charges on five oil drops: A 4.8 &times; 10<sup>&minus;19</sup> C, B 3.2 &times; 10<sup>&minus;19</sup> C, C 6.4 &times; 10<sup>&minus;19</sup> C, D 1.6 &times; 10<sup>&minus;19</sup> C, E 4.8 &times; 10<sup>&minus;19</sup> C.',
  'Millikan&rsquo;s oil-drop experiment. Every charge in the table is a whole-number multiple of 1.6 &times; 10<sup>&minus;19</sup> C (drop D), so that is the charge of a single electron.',
  credit('2.2', P22)),
 ('ch02/2.2_subatomic_particles.html', 'The table above shows two patterns worth remembering', 'after', 'os_2-3_stadium_blueberry.jpg', '',
  'Three images in a row. Left, a drawing of an atom as a large pale sphere about 10<sup>&minus;10</sup> m across with a tiny dot at the center labeled nucleus, about 10<sup>&minus;15</sup> m across. Middle, a photograph of an empty football stadium. Right, a hand holding a handful of blueberries.',
  'How small the nucleus is. If an atom were the size of a football stadium, its nucleus would be about the size of a blueberry, yet the nucleus holds almost all of the atom&rsquo;s mass.',
  credit('2.3', P23, 'photo middle: modification of work by &ldquo;babyknight&rdquo;/Wikimedia Commons; photo right: modification of work by Paxson Woelber')),
 ('ch02/2.4_ions.html', 'The metal formed a cation and kept its name; the nonmetals formed anions ending in -ide.', 'afterbox', 'os_2-3_goiter_salt.jpg',
  '<p>Iodide, I<sup>&minus;</sup>, is an anion your body depends on. The thyroid gland, in the neck, takes up iodide to make its hormones, which control metabolism. When the diet has too little iodine, the thyroid can enlarge into a swelling called a <strong>goiter</strong>. Adding a small amount of an iodine compound, such as potassium iodide, to table salt (&ldquo;iodized salt&rdquo;) has made goiters rare in the United States.</p>',
  'Two photographs. (a) A person&rsquo;s neck with a large, rounded swelling at the front below the chin: an enlarged thyroid gland. (b) A round container of table salt labeled Iodized Salt, with the line &ldquo;This salt supplies iodide, a necessary nutrient.&rdquo;',
  'Iodide and the thyroid. (a) Too little iodine in the diet can cause a goiter, an enlarged thyroid gland. (b) Iodized salt supplies iodide and helps prevent goiters.',
  credit('2.3', P23, 'photo a: modification of work by &ldquo;Almazi&rdquo;/Wikimedia Commons; photo b: modification of work by Mike Mozart')),
 ('ch02/2.6_atomic_mass.html', 'Instruments that sort particles by mass, called <strong>mass spectrometers</strong>', 'afterbox', 'os_2-3_mass_spectrum.jpg', '',
  'Left, a diagram of a mass spectrometer: a sample enters a tube, a heater vaporizes it, an electron beam turns it into ions, the ions are accelerated through plates, and a magnet bends their path, deflecting the lightest ions most, before they reach a detector. Right, a bar graph of the mass spectrum of zirconium, relative abundance in percent versus mass-to-charge ratio: Zr-90 about 51%, Zr-91 about 11%, Zr-92 about 17%, Zr-94 about 17%, and Zr-96 about 3%.',
  'A mass spectrometer separates ions by mass; the lightest are bent the most by the magnet. The mass spectrum of zirconium shows one peak for each isotope, and the peak heights give the percent abundances used to calculate an average atomic mass.',
  credit('2.3', P23)),
 ('ch12/12.6_buffers.html', 'As a thought experiment (the CHEM 3A lab uses red cabbage indicator', 'after', 'os_14-6_buffer_beakers.jpg', '',
  'Two photographs of the same pair of beakers. (a) Both beakers hold yellow liquid; the left one is labeled Unbuffered and the right one pH = 8.0 Buffer. (b) After a small amount of acid is added to each, the unbuffered beaker has turned red while the buffered beaker is still yellow.',
  'A buffer in action, shown with the indicator methyl orange (yellow in basic solution, red below about pH 4). (a) An unbuffered solution and a pH 8.0 buffer start out the same color. (b) After 1 mL of 0.01 M HCl is added to each, the unbuffered solution has turned acidic (red) while the buffer has barely changed.',
  credit('14.6', '14%3A_Acid-Base_Equilibria/14.07%3A_Buffers', 'photos: modification of work by Mark Ott')),
]

def block(img, alt, cap, cred):
    return (f'<figure class="figure"><img src="{BASE}{img}" alt="{alt}" style="max-width:100%;height:auto;" />\n'
            f'<figcaption>Figure \\(\\PageIndex{{0}}\\): {cap} {cred}</figcaption></figure>\n')

touched = set()
for page, key, where, img, lead, alt, cap, cred in FIGS:
    p = os.path.join(R, 'drafts', page); s = open(p).read()
    if BASE + img in s: continue
    assert s.count(key) == 1, (page, key, s.count(key)); i = s.find(key)
    if where == 'after':
        cands = [(s.find(t, i), t) for t in ('</p>', '</ul>') if s.find(t, i) >= 0]; k, t = min(cands); ins = k + len(t) + 1
    elif where == 'afterbox':
        k = s.find('</div>', i); ins = s.find('\n', k) + 1
    elif where == 'afterfig':
        k = s.find('</figure>', i); ins = s.find('\n', k) + 1
    s = s[:ins] + lead + ('\n' if lead else '') + block(img, alt, cap, cred) + s[ins:]
    if ATTR.strip() not in s:
        a = s.find('<p class="boxtitle">Attribution</p>'); j = s.find('</p>', a + 40); s = s[:j] + ATTR + s[j:]
    open(p, 'w').write(s); touched.add(p); print('added', img, 'to', page)

for p in sorted({os.path.join(R, 'drafts', f[0]) for f in FIGS}):
    s = open(p).read(); n = [0]
    def num(m):
        n[0] += 1; return f'<figcaption>Figure \\(\\PageIndex{{{n[0]}}}\\):'
    s = re.sub(r'<figcaption>Figure \\\(\\PageIndex\{\d+\}\\\):', num, s); open(p, 'w').write(s)
    print(os.path.basename(p), n[0], 'figures')
