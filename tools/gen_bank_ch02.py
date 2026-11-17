#!/usr/bin/env python3
"""Builds bank/ch02.json (Chapter 2 Try It items). Scratch generator; the JSON file is the deliverable."""
import json, sys
OUT = sys.argv[1]
M = '&minus;'
def iso(A, Z, s, ch=''):
    return f'<sup>{A}</sup><sub>{Z}</sub>{s}' + (f'<sup>{ch}</sup>' if ch else '')
B = []
def Q(t, q, c, y, h, w, d, k=0, f=None):
    it = {"id": "c2-%03d" % (len(B) + 1), "t": t, "q": q, "c": c, "y": y, "h": h, "w": w, "d": d, "k": k}
    if f: it["f"] = f
    B.append(it)

# particle-diagram key for subatomic particles (letters on every circle, so color is never the only cue)
PK = {"p": {"c": "#c0473b", "n": "proton", "q": "+"},
      "n": {"c": "#8a96a0", "n": "neutron", "q": "n"},
      "e": {"c": "#2f5fa8", "n": "electron", "q": "−", "r": 7}}
def atomfig(p, n, e, seed):
    return [{"type": "particles", "seed": seed, "key": PK,
             "boxes": [{"mols": [["p"]] * p + [["n"]] * n, "cap": "Nucleus"},
                       {"mols": [["e"]] * e, "cap": "Outside the nucleus"}]}]
PT_SHOW = {"H": [1, 1], "He": [1, 18]}

# ---------------- ch02-theory (10) ----------------
T = 'ch02-theory'
Q(T, "Which statement is part of <b>Dalton's atomic theory</b>?",
  ["Atoms of different elements combine in simple whole-number ratios to form compounds.",
   "Every atom has a tiny, dense, positively charged nucleus.",
   "Atoms contain negatively charged particles that can be pulled out by a high voltage.",
   "In a chemical reaction, atoms of one element can turn into atoms of another element."],
  ["Dalton proposed that compounds form when atoms join in fixed, whole-number ratios, which also explains why a compound always has the same composition.",
   "The nucleus came from Rutherford's gold foil experiment about a century after Dalton; Dalton pictured atoms as solid, uncuttable spheres.",
   "Charged particles inside atoms (electrons) were found by Thomson in 1897; Dalton's atoms had no smaller parts.",
   "Dalton said the opposite: in a reaction atoms are only rearranged; they are never changed into atoms of a different element."],
  "Dalton worked in the early 1800s, before anyone knew atoms had smaller parts.",
  "Dalton's theory (early 1800s) says elements are made of atoms, atoms of one element are alike, atoms are rearranged but not created or destroyed in reactions, and <b>atoms combine in simple whole-number ratios to form compounds</b>. Electrons (Thomson) and the nucleus (Rutherford) came later.", 1)

Q(T, "In a cathode-ray tube, the glowing beam bends <b>toward</b> a positively charged plate. What did Thomson conclude from this?",
  ["The beam is made of negatively charged particles.",
   "The beam is made of positively charged particles.",
   "The beam carries no charge.",
   "The atom has a small, dense nucleus."],
  ["Opposite charges attract, so a beam pulled toward a + plate must carry negative charge. These particles were electrons.",
   "Like charges repel, so a positive beam would bend <i>away</i> from the + plate, not toward it.",
   "A beam with no charge would not be pushed or pulled by a charged plate at all; it would go straight.",
   "The nucleus was discovered later, with alpha particles and gold foil, not with cathode rays."],
  "Use the charge rules from Chapter 1: opposite charges attract, like charges repel.",
  "Opposite charges attract. A beam that bends toward the positive plate is <b>negatively charged</b>. Thomson showed the particles were the same for every metal he used: he had found the electron.", 1)

Q(T, "In the gold foil experiment, <b>most</b> alpha particles passed straight through the foil. What does this observation show?",
  ["Most of the volume of an atom is empty space.",
   "The nucleus fills most of the atom's volume.",
   "Alpha particles have no charge.",
   "Gold atoms have almost no mass."],
  ["If most particles meet nothing on their way through a thousand layers of atoms, most of each atom must be open space.",
   "A nucleus that filled the atom would sit in the path of nearly every alpha particle and turn many of them aside.",
   "Alpha particles are positively charged; the result is about what they did or did not run into, not about their charge.",
   "Gold is a heavy element; a few alpha particles even bounced back, which needs a lot of mass packed in one place."],
  "Think about what an alpha particle would have to do to get through the foil without being turned.",
  "Passing straight through means the alpha particles met nothing. So <b>an atom is mostly empty space</b>. The few that bounced back revealed the tiny, dense, positive nucleus.", 2)

Q(T, "Which observation from Rutherford's gold foil experiment showed that an atom's positive charge and mass are packed into a tiny nucleus?",
  ["A small fraction of the alpha particles bounced off at large angles, some almost straight back.",
   "Most alpha particles passed straight through the foil.",
   "A beam of particles bent toward a positively charged plate.",
   "The gold foil gained mass during the experiment."],
  ["Only a small, very heavy, positive center could turn a fast positive alpha particle sharply or send it back; it happened rarely because that center is tiny.",
   "Passing straight through shows that atoms are mostly empty space; it does not show what is concentrated in the center.",
   "A beam bending toward a + plate is Thomson's cathode-ray result, which revealed the electron.",
   "No mass change was part of the result; the evidence came from where the alpha particles went."],
  "Which result needs something small, heavy and positive to explain it?",
  "A positive alpha particle is turned back only when it heads almost straight at something small, massive and positive. The rare <b>large-angle deflections and bounce-backs</b> showed the nucleus. Most particles passing through showed the empty space around it.", 2)

Q(T, "Which description matches Thomson's <b>plum pudding</b> model of the atom?",
  ["A sphere of spread-out positive charge with electrons scattered through it",
   "A tiny, dense, positive nucleus with electrons moving in mostly empty space around it",
   "A solid, uncuttable sphere with no smaller parts",
   "A nucleus of protons and neutrons with no electrons at all"],
  ["Thomson knew atoms were neutral and contained electrons, so he spread the balancing positive charge evenly through the whole atom.",
   "This is the nuclear model that Rutherford proposed after the gold foil experiment replaced the plum pudding model.",
   "This is Dalton's earlier picture; Thomson's model had to include the electrons he had discovered.",
   "Thomson's model was built around electrons; he had just discovered them."],
  "Thomson had found the electron but did not yet know about a nucleus.",
  "Thomson pictured <b>positive charge spread through a sphere with electrons scattered in it</b>, like plums in a pudding. Rutherford's gold foil results later replaced it with the nuclear model.", 1)

Q(T, "Calcium carbonate, the active ingredient in many chewable antacids, is always 40.0% calcium by mass, whatever its source. How many grams of calcium are in a 1.25 g sample of pure calcium carbonate?",
  ["0.500 g", "3.13 g", "50.0 g", "0.750 g"],
  ["40.0% means 0.400 g of calcium in every gram of compound: 0.400 &times; 1.25 g = 0.500 g (3 significant figures).",
   "This divides by 0.400 instead of multiplying. The calcium must be <i>less</i> than the 1.25 g of compound it is part of.",
   "This multiplies by 40.0 instead of 0.400. A percent must be divided by 100 before you use it.",
   "This is 60.0% of the sample: the mass of the carbon and oxygen, not the calcium."],
  "Change the percent to a decimal, then multiply by the mass of the sample.",
  "By the law of definite proportions, every sample of calcium carbonate is 40.0% calcium. 1.25 g &times; 0.400 = <b>0.500 g</b> of calcium. Check: the part (0.500 g) is smaller than the whole (1.25 g).", 2, 1)

Q(T, "A 9.00 g sample of pure water contains 1.01 g of hydrogen and 7.99 g of oxygen. A nurse has a 36.0 g sample of sterile water. How many grams of oxygen does it contain?",
  ["32.0 g", "4.04 g", "7.99 g", "288 g"],
  ["The larger sample is 36.0 &divide; 9.00 = 4.00 times as big, so it has 4.00 times the oxygen: 4.00 &times; 7.99 g = 32.0 g.",
   "This scales up the hydrogen (4.00 &times; 1.01 g) instead of the oxygen.",
   "The <i>ratio</i> of elements is fixed, not the mass of each element; a bigger sample has more oxygen.",
   "This multiplies 36.0 by 7.99 without dividing by the 9.00 g sample size, so the oxygen comes out heavier than the whole sample."],
  "Water always has the same mass ratio of oxygen to the whole. How many times larger is the second sample?",
  "Pure water always has the same composition (law of definite proportions). 36.0 g &divide; 9.00 g = 4.00, so the oxygen is 4.00 &times; 7.99 g = <b>32.0 g</b>. Check: 32.0 &divide; 36.0 = 88.9% oxygen, the same (within rounding) as 7.99 &divide; 9.00 = 88.8%.", 2, 1)

Q(T, "Which part of Dalton's atomic theory was later shown to be <b>not quite right</b>, once isotopes were discovered?",
  ["All atoms of a given element have the same mass.",
   "Atoms are rearranged, not created or destroyed, in chemical reactions.",
   "Atoms combine in simple whole-number ratios to form compounds.",
   "Each element is made of tiny particles called atoms."],
  ["Isotopes are atoms of the same element with different numbers of neutrons, so atoms of one element can have different masses.",
   "This idea still holds; it is why mass is conserved in a chemical reaction.",
   "This idea still holds; it is why every compound has a fixed composition.",
   "This central idea still holds; it is the base of all of modern chemistry."],
  "Isotopes are atoms of the same element that differ in the number of neutrons. Which of Dalton's ideas does that contradict?",
  "Isotopes (Section 2.5) have the same number of protons but different numbers of neutrons, so <b>atoms of the same element do not all have the same mass</b>. Dalton's other main ideas have held up.", 2)

Q(T, "Rutherford's results caused the plum pudding model to be replaced. Which statement best explains why, in terms of the scientific method?",
  ["The model predicted that every alpha particle would pass through with little deflection, and the experiment showed some bouncing back.",
   "Thomson's earlier measurements were found to be made up.",
   "The plum pudding model had no electrons in it.",
   "A model is replaced whenever a more famous scientist proposes a new one."],
  ["A model makes predictions that can be tested. When a prediction fails, the model must change: here, the bounce-backs could not happen if positive charge were spread thin.",
   "Thomson's measurements were sound; his electron is still part of the modern model. The problem was his picture of where the positive charge sits.",
   "Electrons were the center of Thomson's model; he had discovered them.",
   "Models change because of evidence, not reputation. Rutherford's model won because it explained the data."],
  "What did the plum pudding model predict for the gold foil, and what actually happened?",
  "Spread-out positive charge could not turn an alpha particle sharply, so the model predicted that all alpha particles would get through. <b>Some bounced back</b>, the prediction failed, and the model was revised to include a nucleus. Testing predictions is the scientific method from Section 1.1.", 2)

Q(T, "A radiologic technology student reads that many X-ray photons pass through soft tissue without hitting anything. Which feature of the nuclear model helps explain this?",
  ["Each atom is mostly empty space, with a nucleus that is tiny compared with the whole atom.",
   "Atoms in soft tissue have no nuclei.",
   "The nucleus fills most of each atom's volume.",
   "Electrons are packed tightly together and fill each atom solidly."],
  ["The nucleus is roughly 1/100,000 of the atom's diameter, so most of the space a photon crosses is empty.",
   "Every atom has a nucleus; atoms in soft tissue are mostly light elements such as hydrogen, carbon and oxygen, but they still have nuclei.",
   "The nucleus holds almost all the mass but only a tiny fraction of the volume.",
   "Electrons move through a large, mostly empty region; they do not fill the atom solidly."],
  "Recall Rutherford's conclusion about how much of an atom is filled.",
  "In the nuclear model, <b>the atom is mostly empty space</b> around a tiny nucleus, so many photons travel through tissue without striking anything. Bone, with more and heavier atoms in the way, stops more of them, which is why it shows up brighter on an X-ray image.", 1)

# ---------------- ch02-particles (11) ----------------
T = 'ch02-particles'
Q(T, "Which subatomic particle has a <b>negative charge</b> and <b>almost no mass</b>?",
  ["Electron", "Proton", "Neutron", "Alpha particle"],
  ["An electron has a 1&minus; charge and a mass of about 0.00055 amu, so it adds almost nothing to an atom's mass.",
   "A proton has a 1+ charge and a mass of about 1 amu.",
   "A neutron has no charge and a mass of about 1 amu.",
   "An alpha particle is positive and has a mass of about 4 amu; it is not one of the three particles that build an atom."],
  "Two of the three particles have a mass of about 1 amu.",
  "The <b>electron</b> has a 1&minus; charge and a mass of about 0.00055 amu. Protons (1+) and neutrons (0) each have a mass of about 1 amu.", 1)

Q(T, "Where is nearly all of an atom's mass found?",
  ["In the nucleus", "Spread evenly through the whole atom", "In the electrons outside the nucleus", "Split about equally between the nucleus and the electrons"],
  ["Protons and neutrons, each about 1 amu, are in the nucleus; electrons are far lighter.",
   "Rutherford's experiment showed that the mass is concentrated, not spread out.",
   "Electrons are about 1800 times lighter than a proton, so they carry very little of the mass.",
   "An electron is so light that all of an atom's electrons together are a tiny fraction of its mass."],
  "Which particles have a mass of about 1 amu, and where are they?",
  "Protons and neutrons (about 1 amu each) make up the <b>nucleus</b>; electrons (about 0.00055 amu) add almost nothing. So nearly all the mass is in the nucleus, even though it takes up a tiny fraction of the volume.", 1)

Q(T, "The atomic number (Z) of an element is the number of",
  ["protons in each of its atoms", "neutrons in each of its atoms", "protons plus neutrons in each of its atoms", "electrons in every ion of the element"],
  ["The atomic number counts protons, and the proton count is what makes an atom that element.",
   "The number of neutrons can differ among atoms of the same element, so it cannot define the element.",
   "Protons plus neutrons is the mass number (A), which you will use in Section 2.5.",
   "Ions have gained or lost electrons, so their electron count differs from Z; only a neutral atom has Z electrons."],
  "Which particle count can never change without the atom becoming a different element?",
  "Z = <b>number of protons</b>. Every atom of an element has the same Z. A neutral atom also has Z electrons, but ions do not.", 1)

Q(T, "Zinc (Z = 30) is a trace element that many enzymes need. How many protons and electrons are in a neutral zinc atom?",
  ["30 protons and 30 electrons", "65 protons and 65 electrons", "30 protons and 35 electrons", "30 protons and 0 electrons"],
  ["Z = 30 gives 30 protons, and a neutral atom has as many electrons as protons.",
   "65 comes from rounding the average atomic mass (65.38); the atomic number is the whole number, 30.",
   "35 is 65 &minus; 30, which would be a neutron count, not an electron count.",
   "A neutral atom must have electrons to balance the positive charge of its protons."],
  "Use the whole number on the periodic table, and remember that a neutral atom has no overall charge.",
  "Z = 30, so <b>30 protons</b>. Neutral means the charges cancel, so <b>30 electrons</b>. The decimal number (65.38) is the average atomic mass, not a particle count.", 1)

Q(T, "A neutral atom has 53 electrons. The thyroid gland needs this element to make its hormones. Which element is it?",
  ["Iodine", "Xenon", "Tellurium", "It cannot be identified without the mass number."],
  ["A neutral atom has equal numbers of protons and electrons, so it has 53 protons, and Z = 53 is iodine.",
   "Xenon has Z = 54, one more proton than this atom has.",
   "Tellurium has Z = 52, one fewer proton than this atom has.",
   "The identity depends only on the number of protons, and for a neutral atom that equals the number of electrons."],
  "In a neutral atom, electrons = protons, and protons give the atomic number.",
  "Neutral, so protons = electrons = 53. Z = 53 is <b>iodine</b>, I. The mass number tells you which isotope, but not which element.", 1)

Q(T, "Which two subatomic particles have charges that are <b>equal in size but opposite in sign</b>?",
  ["A proton and an electron", "A proton and a neutron", "A neutron and an electron", "Two protons"],
  ["A proton is 1+ and an electron is 1&minus;, so one proton and one electron cancel exactly.",
   "A neutron has no charge, so it cannot cancel a proton's 1+ charge.",
   "A neutron has no charge, so it cannot cancel an electron's 1&minus; charge.",
   "Two protons have the same sign (both 1+), so their charges add instead of cancel."],
  "Opposite in sign means one is positive and one is negative.",
  "A <b>proton (1+) and an electron (1&minus;)</b> have equal and opposite charges. That is why a neutral atom has equal numbers of the two.", 1)

Q(T, "The diagram shows every particle in one atom. Which element is it, and is it neutral?",
  ["Fluorine, neutral", "Potassium, neutral", "Neon, neutral", "Fluorine, as the fluoride ion"],
  ["There are 9 protons (Z = 9 is fluorine) and 9 electrons, so the charges cancel.",
   "19 is the total of protons and neutrons in the nucleus; the element is set by the protons alone.",
   "10 is the number of neutrons; the element is set by the protons, not the neutrons.",
   "An ion has unequal numbers of protons and electrons; count the two boxes again."],
  "Count only the + particles to find the element. Then compare protons with electrons.",
  "Nucleus: 9 protons and 10 neutrons. Outside: 9 electrons. Z = 9 is <b>fluorine</b>, and 9 protons with 9 electrons make it <b>neutral</b>. The fluoride ion in toothpaste would have one extra electron.", 2, 0,
  atomfig(9, 10, 9, 5))

Q(T, "The atomic mass unit (amu) is defined as",
  ["one-twelfth of the mass of a carbon-12 atom", "the mass of one electron", "the mass of one hydrogen molecule", "exactly 1 gram"],
  ["One amu is defined from carbon-12: 1/12 of the mass of one carbon-12 atom, about 1.6605 &times; 10<sup>&minus;24</sup> g.",
   "An electron is about 0.00055 amu, far smaller than the unit.",
   "A hydrogen molecule (H<sub>2</sub>) has a mass of about 2 amu, not 1.",
   "A gram is enormous on the atomic scale: 1 amu is only about 1.6605 &times; 10<sup>&minus;24</sup> g."],
  "The unit is tied to one particular isotope of carbon.",
  "1 amu = <b>1/12 of the mass of a carbon-12 atom</b> = 1.6605 &times; 10<sup>&minus;24</sup> g. On this scale protons and neutrons are each about 1 amu.", 2)

Q(T, "About how many electrons would it take to equal the mass of one proton?",
  ["About 1800", "1", "12", "About 100,000"],
  ["A proton is about 1.0073 amu and an electron about 0.00055 amu; 1.0073 &divide; 0.00055 is roughly 1800.",
   "The charges are equal in size, but the masses are very different.",
   "12 comes from the definition of the amu (carbon-12), not from comparing these two particles.",
   "100,000 compares the size of an atom with the size of its nucleus, not the masses of two particles."],
  "Compare 1.0073 amu with 0.00055 amu.",
  "1.0073 amu &divide; 0.00055 amu &asymp; <b>1800</b>. An electron is so light that chemists treat its mass as about 0 amu when they add up the mass of an atom.", 2)

Q(T, "Which statement about neutrons is correct?",
  ["They add mass to the nucleus but do not change the atom's charge.",
   "They carry a negative charge that balances the protons.",
   "Their number decides which element an atom is.",
   "They move outside the nucleus, along with the electrons."],
  ["A neutron has no charge and a mass of about 1 amu, so it adds mass only.",
   "Electrons, not neutrons, balance the protons' charge; neutrons are neutral.",
   "The element is set by the number of protons; atoms of one element can have different numbers of neutrons.",
   "Neutrons are in the nucleus with the protons."],
  "Neutron sounds like neutral.",
  "Neutrons are neutral particles of about 1 amu in the nucleus. They <b>add mass but no charge</b>, and their number can vary within an element (isotopes, Section 2.5).", 1)

Q(T, "An atom has 12 protons, 12 neutrons and 12 electrons. Which change would turn it into an atom of a <b>different element</b>?",
  ["Adding one proton", "Adding one neutron", "Removing one electron", "Adding two electrons"],
  ["The number of protons is the atomic number; 13 protons would make it aluminum instead of magnesium.",
   "A different number of neutrons gives a different isotope of the same element.",
   "Losing an electron makes an ion of the same element; the protons are unchanged.",
   "Gaining electrons makes an ion of the same element; the protons are unchanged."],
  "Which particle count defines the element?",
  "Only the number of protons decides the element. 12 protons is magnesium; <b>adding a proton</b> (13) makes aluminum. Changing neutrons gives an isotope; changing electrons gives an ion.", 2)

# ---------------- ch02-table (11) ----------------
T = 'ch02-table'
Q(T, "A lab report flags <b>hypernatremia</b>, a high level of an element in the blood. The word comes from the element's Latin name, <i>natrium</i>. What is the element's symbol?",
  ["Na", "N", "Ne", "Nt"],
  ["Sodium's symbol comes from its Latin name, natrium.",
   "N is nitrogen, a gas that is not the ion measured here.",
   "Ne is neon, a noble gas that does not form ions in the body.",
   "Nt is not the symbol of any element; symbols must be learned, not built from the first letters."],
  "-natremia refers to the element sodium.",
  "<i>Natrium</i> is the Latin name for sodium, so the symbol is <b>Na</b>. Hyper- means high and -emia means in the blood: hypernatremia is high blood sodium.", 1)

Q(T, "A respiratory therapy chart lists inhaled &ldquo;NO&rdquo; as a gas used for some newborns. What does NO stand for?",
  ["A compound made of nitrogen and oxygen", "The element nobelium", "The element sodium", "The element neon"],
  ["Two capital letters mean two different elements: N (nitrogen) and O (oxygen) together make the compound nitric oxide.",
   "Nobelium's symbol is No, with a lowercase o; NO with two capitals is two elements.",
   "Sodium's symbol is Na, from the Latin natrium.",
   "Neon's symbol is Ne."],
  "A second letter in an element symbol is always lowercase.",
  "A symbol has one capital letter, so <b>NO</b> is two symbols, N and O: the compound nitric oxide. Compare No (nobelium) and CO (carbon monoxide) with Co (cobalt).", 2)

Q(T, "Radiologic technologists wear aprons made with lead to shield their bodies. What is the symbol for lead?",
  ["Pb", "Pd", "P", "Ld"],
  ["Lead's symbol comes from its Latin name, plumbum (the root of the word plumbing).",
   "Pd is palladium, a different metal.",
   "P is phosphorus, a nonmetal.",
   "Ld is not the symbol of any element; lead is one of the elements whose symbol comes from Latin."],
  "This is one of the symbols that come from a Latin name.",
  "Lead is <b>Pb</b>, from the Latin <i>plumbum</i>. Pd is palladium and P is phosphorus.", 1)

Q(T, "Which highlighted element (A&ndash;D) on the periodic table outline is a <b>halogen</b>?",
  ["B", "A", "C", "D"],
  ["B is in group 17, the next-to-last column: the halogen family (F, Cl, Br, I).",
   "A is in group 18, the last column: a noble gas, not a halogen.",
   "C is in group 2: an alkaline earth metal.",
   "D is in group 16, one column left of the halogens: the oxygen family (chalcogens)."],
  "Halogens are in group 17, one column left of the last column.",
  "The halogens are group 17, the next-to-last column. Only <b>B</b> is there (it is chlorine, period 3). A is a noble gas (group 18), C an alkaline earth metal (group 2), and D a chalcogen (group 16).", 2, 0,
  [{"type": "ptgrid", "periods": 5, "show": PT_SHOW, "cells": {"A": [4, 18], "B": [3, 17], "C": [4, 2], "D": [2, 16]}}])

Q(T, "Calcium in bones and teeth is in group 2, period 4. The element marked X sits in the same <b>group</b> but one <b>period</b> higher. Which element is X?",
  ["Magnesium", "Strontium", "Potassium", "Calcium"],
  ["One row up from calcium in group 2 is period 3: magnesium (Z = 12).",
   "Strontium is one period lower (period 5), not higher.",
   "Potassium is in the same period as calcium but in group 1, one column to the left.",
   "X is in a different row, so it cannot be calcium itself."],
  "Groups are columns; periods are rows numbered from the top.",
  "Same group (column 2), one period higher (row 3): X is <b>magnesium</b>, Mg, another alkaline earth metal. Moving up or down a column keeps the group; moving across a row keeps the period.", 2, 0,
  [{"type": "ptgrid", "periods": 4, "show": dict(PT_SHOW, Ca=[4, 2]), "cells": {"X": [3, 2]}}])

Q(T, "Arsenic, found naturally in some San Joaquin Valley groundwater, is a <b>metalloid</b>. Which highlighted element (A&ndash;D) is also a metalloid?",
  ["C", "A", "B", "D"],
  ["C is group 15, period 4, right on the staircase between metals and nonmetals; that is arsenic.",
   "A is group 13, period 3: aluminum, a metal to the left of the staircase.",
   "B is group 15, period 3: phosphorus, a nonmetal above the staircase.",
   "D is group 16, period 4: selenium, a nonmetal to the right of the staircase."],
  "The staircase starts at boron and steps down to the right. Metalloids touch it: B, Si, Ge, As, Sb, Te.",
  "The metalloids sit along the staircase: B, Si, Ge, As, Sb, Te. <b>C</b> (group 15, period 4) is arsenic. A is aluminum (a metal), B is phosphorus and D is selenium (both nonmetals).", 2, 0,
  [{"type": "ptgrid", "periods": 4, "show": PT_SHOW, "cells": {"A": [3, 13], "B": [3, 15], "C": [4, 15], "D": [4, 16]}}])

Q(T, "Elements in the same <b>group</b> of the periodic table",
  ["have similar chemical properties", "are all in the same horizontal row", "all have the same atomic mass", "have the same number of protons"],
  ["A group is a column, and the elements in a column behave alike; that is why groups such as the halogens have family names.",
   "A horizontal row is a period, not a group.",
   "Atomic mass increases going down a group.",
   "Each element has its own number of protons; no two elements share an atomic number."],
  "Groups are the columns. What do the members of a family have in common?",
  "A group (family) is a vertical column, and its members have <b>similar chemical properties</b>; Chapter 3 explains why. A period is a row.", 1)

Q(T, "Dental amalgam fillings contain silver, tin, copper and mercury. Which list gives the correct symbols, in that order?",
  ["Ag, Sn, Cu, Hg", "Ag, Ti, Cu, Hg", "Si, Sn, Cu, Hg", "Ag, Sn, Co, Hg"],
  ["All four come from Latin names: argentum (silver), stannum (tin), cuprum (copper), hydrargyrum (mercury).",
   "Ti is titanium, not tin; tin's symbol comes from the Latin stannum.",
   "Si is silicon, a metalloid; silver's symbol comes from the Latin argentum.",
   "Co is cobalt; copper's symbol comes from the Latin cuprum."],
  "All four of these elements have symbols from Latin names.",
  "Silver <b>Ag</b> (argentum), tin <b>Sn</b> (stannum), copper <b>Cu</b> (cuprum), mercury <b>Hg</b> (hydrargyrum). Ti is titanium, Si silicon and Co cobalt.", 2)

Q(T, "Which element is a <b>nonmetal</b> that is a <b>liquid</b> at room temperature?",
  ["Bromine", "Mercury", "Chlorine", "Iodine"],
  ["Bromine (group 17) is the only nonmetal that is a liquid at room temperature.",
   "Mercury is a liquid, but it is a metal; it is the only metal that is not a solid at room temperature.",
   "Chlorine is a nonmetal, but it is a gas at room temperature.",
   "Iodine is a nonmetal, but it is a solid at room temperature."],
  "Two elements are liquids at room temperature: one metal and one nonmetal.",
  "<b>Bromine</b> is the one liquid nonmetal; mercury is the one liquid metal. Chlorine is a gas and iodine a solid, though all three halogens are nonmetals.", 2)

Q(T, "Barium sulfate is a contrast medium that makes the digestive tract show up on X-ray images. Barium (Ba) is in group 2. Which family does it belong to?",
  ["Alkaline earth metals", "Alkali metals", "Halogens", "Transition metals"],
  ["Group 2 is the alkaline earth metal family, with Be, Mg, Ca, Sr and Ba.",
   "Alkali metals are group 1 (Li, Na, K, Rb, Cs).",
   "Halogens are group 17 nonmetals (F, Cl, Br, I).",
   "Transition metals fill groups 3&ndash;12 in the middle of the table."],
  "Match the group number with the family name.",
  "Group 2 is the <b>alkaline earth metals</b>: Be, Mg, Ca, Sr, Ba. Barium is a heavy atom, so it blocks X-rays well; calcium in the same family is in your bones.", 1)

Q(T, "Which of these elements is a <b>transition metal</b>?",
  ["Iron (Fe)", "Calcium (Ca)", "Aluminum (Al)", "Selenium (Se)"],
  ["Iron is in group 8, inside the block of groups 3&ndash;12 in the middle of the table.",
   "Calcium is in group 2, a main-group metal (an alkaline earth metal).",
   "Aluminum is in group 13, a main-group metal just left of the staircase.",
   "Selenium is in group 16, a main-group nonmetal."],
  "Transition metals are in groups 3&ndash;12.",
  "Transition metals fill groups 3&ndash;12. <b>Iron</b> (group 8, period 4) is one; it is the metal at the center of heme in hemoglobin. Ca (2), Al (13) and Se (16) are main-group elements.", 1)

# ---------------- ch02-ions (11) ----------------
T = 'ch02-ions'
Q(T, "A <b>cation</b> forms when a neutral atom",
  ["loses one or more electrons", "gains one or more electrons", "gains one or more protons", "loses one or more neutrons"],
  ["Losing negative electrons leaves more protons than electrons, so the particle becomes positive.",
   "Gaining electrons makes the particle negative: that forms an anion.",
   "Ions form by changing electrons only; changing the protons would make a different element.",
   "Neutrons have no charge, so losing them cannot make an ion."],
  "Charge = protons &minus; electrons. What change makes that positive?",
  "A cation is positive, so protons must outnumber electrons. That happens when the atom <b>loses electrons</b>. Metals usually form cations.", 1)

Q(T, "Toothpaste and fluoride varnish deliver the <b>fluoride ion</b>, F<sup>&minus;</sup>. How many protons and electrons does one fluoride ion have?",
  ["9 protons and 10 electrons", "9 protons and 8 electrons", "10 protons and 10 electrons", "9 protons and 9 electrons"],
  ["Fluorine has Z = 9. A 1&minus; charge means one extra electron: 9 + 1 = 10.",
   "This removes an electron, which would give a 1+ ion; a negative ion has gained an electron.",
   "The proton count never changes when an ion forms; it stays at Z.",
   "Equal protons and electrons is the neutral fluorine atom, not the ion."],
  "Protons come from Z. For an anion, electrons = protons + size of the charge.",
  "F: Z = 9, so <b>9 protons</b>. The 1&minus; charge means it gained one electron: <b>10 electrons</b>. Check: 9 &minus; 10 = &minus;1.", 1)

Q(T, "Many enzymes in the body hold a zinc ion, Zn<sup>2+</sup>. How many protons and electrons does Zn<sup>2+</sup> have?",
  ["30 protons and 28 electrons", "30 protons and 32 electrons", "28 protons and 28 electrons", "30 protons and 30 electrons"],
  ["Zinc has Z = 30. A 2+ charge means two electrons were lost: 30 &minus; 2 = 28.",
   "Adding electrons makes an ion more negative; a 2+ ion has fewer electrons than protons.",
   "Ions form by losing electrons only; 28 protons would be nickel, not zinc.",
   "30 electrons is the neutral atom; the 2+ charge means some were lost."],
  "Electrons = protons &minus; charge.",
  "Zn: Z = 30, so <b>30 protons</b>. 2+ means two electrons lost: 30 &minus; 2 = <b>28 electrons</b>. Check: 30 &minus; 28 = +2.", 2, 1)

Q(T, "Selenium in western San Joaquin Valley soils dissolves in irrigation water. A monatomic ion has 34 protons and 36 electrons. Which ion is it?",
  ["Se<sup>2&minus;</sup>, selenide", "Se<sup>2+</sup>", "Kr, a krypton atom", "Br<sup>&minus;</sup>, bromide"],
  ["Z = 34 is selenium, and 34 &minus; 36 = &minus;2, so it is Se<sup>2&minus;</sup>; a monatomic anion is named with -ide.",
   "More electrons than protons means a negative charge, not a positive one.",
   "Krypton has 36 protons; this ion has 36 electrons, and the element is set by the protons.",
   "Bromine has 35 protons; this ion has 34."],
  "Use the protons to name the element, then charge = protons &minus; electrons.",
  "34 protons is <b>selenium</b>. Charge = 34 &minus; 36 = 2&minus;, so the ion is <b>Se<sup>2&minus;</sup>, selenide</b>. (In soil water most selenium is actually in larger ions containing oxygen; the monatomic ion is shown here for counting practice.)", 2, 1)

Q(T, "Which highlighted element (A&ndash;D) is most likely to form an ion with a <b>2&minus;</b> charge?",
  ["D", "A", "B", "C"],
  ["D is in group 16; main-group elements in group 16 usually gain two electrons to form 2&minus; ions.",
   "A is in group 2, which usually forms 2+ ions, not 2&minus; ions.",
   "B is in group 15, which usually forms 3&minus; ions.",
   "C is in group 18; noble gases rarely form ions at all."],
  "Main-group charges follow the group: 1+, 2+, 3+ on the left; 3&minus;, 2&minus;, 1&minus; on the right.",
  "Group 16 elements gain two electrons: 2&minus;. <b>D</b> (group 16, period 3) is sulfur, which forms S<sup>2&minus;</sup>. A (group 2) forms 2+, B (group 15) forms 3&minus;, and C (group 18) rarely forms ions.", 2, 0,
  [{"type": "ptgrid", "periods": 4, "show": PT_SHOW, "cells": {"A": [4, 2], "B": [2, 15], "C": [3, 18], "D": [3, 16]}}])

Q(T, "The diagram shows all the protons, neutrons and electrons of one particle (an atom or an ion). Which particle is it?",
  ["O<sup>2&minus;</sup>, an oxide ion", "A neon atom", "O<sup>2+</sup>", "A sulfur atom"],
  ["8 protons is oxygen, and 8 &minus; 10 = &minus;2, so this is the oxide ion.",
   "Neon has 10 protons; 10 is the electron count here, and electrons do not decide the element.",
   "There are more electrons than protons, so the charge is negative, not positive.",
   "16 is the total of protons and neutrons; the element is set by the 8 protons alone."],
  "Count the + particles for the element, then subtract the electrons to get the charge.",
  "Nucleus: 8 protons and 8 neutrons. Outside: 10 electrons. Z = 8 is oxygen, and 8 &minus; 10 = 2&minus;: <b>O<sup>2&minus;</sup>, the oxide ion</b>.", 2, 0,
  atomfig(8, 8, 10, 13))

Q(T, "Iodized salt contains iodine as the I<sup>&minus;</sup> ion. What is the name of I<sup>&minus;</sup>?",
  ["Iodide", "Iodine", "Iodate", "Iodine ion"],
  ["A monatomic anion takes the root of the element name plus -ide.",
   "Iodine is the element (I<sub>2</sub> as a solid); the anion has a different name.",
   "The -ate ending is for polyatomic ions that contain oxygen, not for a single iodine atom with a charge.",
   "Keeping the element name is the rule for monatomic cations; anions change the ending."],
  "Monatomic anions end in -ide: Cl<sup>&minus;</sup> is chloride.",
  "Anion names use the root plus -ide, so I<sup>&minus;</sup> is <b>iodide</b>. Cations keep the element name (Na<sup>+</sup> is the sodium ion).", 1)

Q(T, "A patient's potassium result is 6.2 mmol/L. The lab's reference range is 3.5&ndash;5.0 mmol/L. How would this result be described?",
  ["Hyperkalemia", "Hypokalemia", "Hypernatremia", "Hypercalcemia"],
  ["The value is above the range (hyper-), and -kalemia refers to potassium (Latin kalium, symbol K).",
   "Hypo- means below the range; 6.2 is above 5.0.",
   "-natremia refers to sodium (natrium), not potassium.",
   "-calcemia refers to calcium, not potassium."],
  "Hyper- means above, hypo- means below. Potassium's Latin name is kalium.",
  "6.2 mmol/L is above 5.0, so it is <b>hyperkalemia</b>: high blood potassium (K<sup>+</sup>). Reading the label is the chemistry skill here; decisions about care follow the provider's orders and facility policy.", 1)

Q(T, "Predict the usual ion formed by phosphorus, and name it.",
  ["P<sup>3&minus;</sup>, phosphide", "P<sup>3+</sup>, phosphorus ion", "P<sup>5+</sup>, phosphorus ion", "P<sup>3&minus;</sup>, phosphorus ion"],
  ["Phosphorus is in group 15, which gains three electrons to form 3&minus; ions; the anion name ends in -ide.",
   "A nonmetal in group 15 gains electrons, so the charge is negative, not positive.",
   "Group 15 does not form 5+ ions; it gains three electrons.",
   "The charge is right, but anions are not named with the element name; they take -ide."],
  "Find phosphorus's group. Nonmetals gain electrons, and their anions end in -ide.",
  "Group 15 forms 3&minus; ions, so phosphorus forms <b>P<sup>3&minus;</sup></b>, named <b>phosphide</b>.", 2)

Q(T, "Iron supplements and hemoglobin involve the ions Fe<sup>2+</sup> and Fe<sup>3+</sup>. How do these two ions differ?",
  ["Fe<sup>3+</sup> has one fewer electron than Fe<sup>2+</sup>; both have 26 protons.",
   "Fe<sup>3+</sup> has one more proton than Fe<sup>2+</sup>.",
   "Fe<sup>3+</sup> has one more electron than Fe<sup>2+</sup>.",
   "Fe<sup>3+</sup> has one more neutron than Fe<sup>2+</sup>."],
  ["Both are iron (26 protons). Fe<sup>2+</sup> has 24 electrons and Fe<sup>3+</sup> has 23, so the 3+ ion lost one more.",
   "An extra proton would make a different element (cobalt); both ions are iron.",
   "Gaining an electron would make the ion less positive, not more.",
   "Neutrons have no charge, so they cannot change the ion's charge."],
  "Charge = protons &minus; electrons, and the protons are fixed for iron.",
  "Both ions have <b>26 protons</b>. Fe<sup>2+</sup> has 26 &minus; 2 = 24 electrons; Fe<sup>3+</sup> has 26 &minus; 3 = 23. The more positive ion has <b>one fewer electron</b>.", 2)

Q(T, "Stannous fluoride toothpaste contains tin as the Sn<sup>2+</sup> ion. A dental hygiene student counts its particles. How many protons and electrons does Sn<sup>2+</sup> have?",
  ["50 protons and 48 electrons", "50 protons and 52 electrons", "48 protons and 48 electrons", "119 protons and 117 electrons"],
  ["Tin has Z = 50; a 2+ charge means two electrons lost: 50 &minus; 2 = 48.",
   "Adding two electrons would give a 2&minus; ion; a 2+ ion has fewer electrons than protons.",
   "The protons stay at Z = 50 when an ion forms; 48 protons would be cadmium.",
   "119 comes from tin's average atomic mass (118.71); the atomic number is 50."],
  "Use the atomic number for protons, not the atomic mass.",
  "Sn: Z = 50, so <b>50 protons</b>; 2+ means <b>48 electrons</b>. &ldquo;Stannous&rdquo; comes from <i>stannum</i>, the Latin name for tin.", 2, 1)

# ---------------- ch02-isotopes (11) ----------------
T = 'ch02-isotopes'
Q(T, "Isotopes of the same element have the same number of ______ but different numbers of ______.",
  ["protons; neutrons", "neutrons; protons", "electrons; protons", "protons; electrons"],
  ["Same protons means same element; a different neutron count gives a different mass number.",
   "A different number of protons would make them different elements, not isotopes.",
   "A different number of protons would make them different elements.",
   "Atoms with the same protons but different electrons are ions of one element, not isotopes."],
  "What must stay the same for two atoms to be the same element?",
  "Isotopes are atoms of one element: <b>same protons (same Z), different neutrons</b> (different A).", 1)

Q(T, "The mass number (A) of an atom is the number of",
  ["protons plus neutrons in its nucleus", "protons in its nucleus", "neutrons in its nucleus", "protons, neutrons and electrons in the atom"],
  ["Protons and neutrons each have a mass of about 1 amu, so their total is close to the atom's mass in amu.",
   "The number of protons alone is the atomic number, Z.",
   "Neutrons alone are A &minus; Z, not A.",
   "Electrons are left out because they are so light."],
  "A counts the heavy particles.",
  "A = <b>protons + neutrons</b>. Neutrons = A &minus; Z.", 1)

Q(T, "Technetium-99m is the most widely used isotope in nuclear medicine imaging. Technetium has Z = 43. How many neutrons are in a technetium-99m nucleus? (The &ldquo;m&rdquo; means the nucleus is in a higher-energy state; it does not change the particle count.)",
  ["56", "99", "43", "142"],
  ["Neutrons = A &minus; Z = 99 &minus; 43 = 56.",
   "99 is the mass number, which counts protons and neutrons together.",
   "43 is the atomic number, the number of protons.",
   "This adds A and Z instead of subtracting."],
  "Neutrons = mass number &minus; atomic number.",
  "Neutrons = A &minus; Z = 99 &minus; 43 = <b>56</b>.", 1, 1)

Q(T, "Iodine-123 and iodine-131 are both used in thyroid studies. How many more neutrons does an iodine-131 atom have than an iodine-123 atom?",
  ["8", "0", "78", "70"],
  ["Both have 53 protons, so the difference in mass number (131 &minus; 123) is all neutrons: 8.",
   "They are the same element, so they have the same protons, but their mass numbers differ, so their neutrons differ.",
   "78 is the number of neutrons in iodine-131 alone, not the difference.",
   "70 is the number of neutrons in iodine-123 alone, not the difference."],
  "Same element means same protons. Where does the difference in mass number come from?",
  "Iodine-123 has 123 &minus; 53 = 70 neutrons; iodine-131 has 131 &minus; 53 = 78. The difference is <b>8 neutrons</b>, the same as 131 &minus; 123.", 2, 1)

Q(T, "Carbon-14 is used to date old bones and wood. Compared with an ordinary carbon-12 atom, a neutral carbon-14 atom has the same",
  ["number of protons and electrons", "number of neutrons", "mass number", "mass"],
  ["Both are carbon (6 protons) and, when neutral, both have 6 electrons; that is why they behave the same chemically.",
   "Carbon-12 has 6 neutrons and carbon-14 has 8.",
   "The mass numbers are 12 and 14; the numbers in the names are the mass numbers.",
   "Carbon-14 has two more neutrons, so it is about 2 amu heavier."],
  "The number after the name is the mass number. What stays the same for every carbon atom?",
  "Both isotopes have <b>6 protons and, as neutral atoms, 6 electrons</b>. Carbon-14 has 8 neutrons and carbon-12 has 6, so their mass numbers and masses differ.", 1)

Q(T, "Fluorine-18 is used in PET (positron emission tomography) scans. A fluorine-18 atom has 9 protons and 9 neutrons. Which isotope symbol is correct?",
  [iso(18, 9, 'F'), iso(9, 18, 'F'), iso(9, 9, 'F'), iso(18, 18, 'Ar')],
  ["The mass number (9 + 9 = 18) goes on top and the atomic number (9) on the bottom.",
   "This swaps the two numbers; the mass number is the top (superscript) number.",
   "The top number must be protons plus neutrons, not just the neutrons.",
   "18 is the mass number, not the atomic number; an atom with 18 protons would be argon, not fluorine."],
  "Top: mass number A = protons + neutrons. Bottom: atomic number Z = protons.",
  "A = 9 + 9 = 18 and Z = 9: <b>" + iso(18, 9, 'F') + "</b>, also written fluorine-18 or F-18.", 2)

Q(T, "Thallium-201, given as the Tl<sup>+</sup> ion, has been used for heart imaging. Thallium has Z = 81. How many protons, neutrons and electrons are in one " + iso(201, 81, 'Tl', '+') + " ion?",
  ["81 protons, 120 neutrons, 80 electrons",
   "81 protons, 120 neutrons, 82 electrons",
   "81 protons, 201 neutrons, 80 electrons",
   "81 protons, 119 neutrons, 80 electrons"],
  ["Protons = Z = 81; neutrons = 201 &minus; 81 = 120; a 1+ charge means one electron lost: 81 &minus; 1 = 80.",
   "Adding an electron gives a negative ion; a 1+ ion has one fewer electron than protons.",
   "201 is the mass number (protons plus neutrons), not the neutron count.",
   "The charge changes only the electrons; neutrons are always A &minus; Z."],
  "Z = protons. Neutrons = A &minus; Z. Electrons = protons &minus; charge.",
  "<b>81 protons</b> (Z); <b>120 neutrons</b> (201 &minus; 81); <b>80 electrons</b> (81 &minus; 1). Check: 81 &minus; 80 = +1.", 3, 1)

Q(T, "The diagram shows the particles in one atom used in the urea breath test for <i>Helicobacter pylori</i>, a stomach bacterium. Which isotope is it?",
  ["Carbon-13", "Nitrogen-13", "Carbon-7", "Aluminum-13"],
  ["6 protons is carbon, and 6 + 7 = 13 protons and neutrons gives mass number 13.",
   "7 is the neutron count; the element is set by the 6 protons.",
   "The mass number counts protons and neutrons together, not neutrons alone.",
   "13 is the mass number; Z = 13 would need 13 protons, and the nucleus has 6."],
  "Count the protons for the element. Add protons and neutrons for the mass number.",
  "Nucleus: 6 protons and 7 neutrons, with 6 electrons outside. Z = 6 is carbon and A = 6 + 7 = 13: <b>carbon-13</b>, a stable isotope. Bacterial urease releases it as CO<sub>2</sub> that the patient breathes out.", 2, 0,
  atomfig(6, 7, 6, 21))

Q(T, "Researchers trace nitrogen fertilizer through Valley crops using a rare nitrogen isotope. Which pair of atoms are <b>isotopes</b> of each other?",
  [iso(14, 7, 'N') + " and " + iso(15, 7, 'N'),
   iso(14, 6, 'C') + " and " + iso(14, 7, 'N'),
   iso(14, 7, 'N') + " and " + iso(14, 7, 'N', '3&minus;'),
   iso(15, 7, 'N') + " and " + iso(16, 8, 'O')],
  ["Both have Z = 7 (nitrogen) but different mass numbers, so they differ in neutrons (7 and 8).",
   "The same mass number does not make atoms isotopes; these have 6 and 7 protons, so they are different elements.",
   "These have the same protons and the same neutrons; they differ only in electrons, which makes an ion, not an isotope.",
   "These have the same number of neutrons (8), but different protons, so they are different elements."],
  "Isotopes share Z and differ in A.",
  "Isotopes have the <b>same Z and different A</b>. " + iso(14, 7, 'N') + " (7 neutrons) and " + iso(15, 7, 'N') + " (8 neutrons) are both nitrogen. Fertilizer made with extra nitrogen-15 lets scientists follow where that nitrogen goes.", 2)

Q(T, "The thyroid absorbs radioactive iodine-131 just as it absorbs stable iodine-127. Why can't the gland tell them apart?",
  ["Both have the same number of protons and electrons, so they behave the same way chemically.",
   "Both have the same mass.",
   "Both have the same number of neutrons.",
   "Radioactive atoms are attracted to the thyroid by their radiation."],
  ["Chemical behavior depends on electrons, and isotopes of one element have the same electron count as neutral atoms.",
   "Iodine-131 is about 4 amu heavier than iodine-127; the difference is in mass, not chemistry.",
   "They have different numbers of neutrons (78 and 74); that is what makes them different isotopes.",
   "Radiation does not attract the gland; the gland takes up iodine of any isotope because they react the same way."],
  "What do isotopes of one element have in common, and which particles control chemical behavior?",
  "Chemistry depends on electrons, and isotopes of iodine all have <b>53 protons and 53 electrons</b>. So the thyroid takes up iodine-131 like iodine-127, which is what makes radioactive iodine useful in thyroid imaging and therapy.", 2)

Q(T, "Xenon-133 gas is breathed in during some lung ventilation scans. Xenon has Z = 54. How many <b>electrons</b> are in a neutral xenon-133 atom?",
  ["54", "133", "79", "187"],
  ["A neutral atom has as many electrons as protons, and Z = 54.",
   "133 is the mass number, which counts protons and neutrons, not electrons.",
   "79 is the number of neutrons (133 &minus; 54), not electrons.",
   "This adds the mass number and the atomic number; no particle count is found that way."],
  "The mass number does not affect the electron count of a neutral atom.",
  "Neutral, so electrons = protons = Z = <b>54</b>. (Xenon-133 has 133 &minus; 54 = 79 neutrons.)", 1, 1)

# ---------------- ch02-mass (10) ----------------
T = 'ch02-mass'
Q(T, "Why is the atomic mass of most elements on the periodic table <b>not</b> a whole number?",
  ["It is a weighted average of the masses of the element's natural isotopes.",
   "Some atoms have part of a proton.",
   "Atoms constantly gain and lose neutrons.",
   "It is the mass number rounded to two decimal places."],
  ["Natural samples are mixtures of isotopes with different masses, and the table lists their abundance-weighted average.",
   "Protons are whole particles; every atom of an element has a whole number of them.",
   "The neutron count of a stable atom does not keep changing; the average reflects a mixture of different isotopes.",
   "A mass number is a whole-number count of particles; rounding it could never give a decimal."],
  "Natural chlorine, for example, is a mixture of chlorine-35 and chlorine-37.",
  "The atomic mass is a <b>weighted average</b> over the element's natural isotopes, each counted by its percent abundance. No single atom has the average mass.", 1)

Q(T, "Thallium has two natural isotopes, thallium-203 and thallium-205. Its average atomic mass is 204.38 amu. Which isotope is more abundant?",
  ["Thallium-205", "Thallium-203", "They are equally abundant.", "It cannot be told without a calculation."],
  ["204.38 is above the halfway point (about 204), so the average is pulled toward the heavier isotope.",
   "If thallium-203 were more common, the average would be below 204, closer to 203.",
   "Equal amounts would put the average at about 204.0, halfway between.",
   "The position of the average between the two masses is enough to decide."],
  "The average lies closest to the most abundant isotope.",
  "Halfway between 203 and 205 is about 204. The average, 204.38, is closer to 205, so <b>thallium-205</b> is more abundant (about 70% of natural thallium).", 2)

Q(T, "Boron is a micronutrient that almond trees need. Natural boron is 19.9% boron-10 (10.0129 amu) and 80.1% boron-11 (11.0093 amu). What is boron's average atomic mass?",
  ["10.81 amu", "10.51 amu", "1081 amu", "10.21 amu"],
  ["(0.199)(10.0129) + (0.801)(11.0093) = 1.99 + 8.82 = 10.81 amu, closer to 11 because boron-11 is more common.",
   "This is the simple average of the two masses, which ignores that boron-11 is four times as common.",
   "This multiplies by the percents (19.9 and 80.1) instead of the fractions, so the answer is 100 times too large.",
   "This pairs each abundance with the wrong isotope, putting 80.1% on boron-10."],
  "Change each percent to a fraction, multiply by that isotope's mass, then add.",
  "(0.199)(10.0129 amu) + (0.801)(11.0093 amu) = 1.99 + 8.82 = <b>10.81 amu</b>. Check: it lies between the two masses, closer to boron-11, the more abundant isotope.", 2, 1)

Q(T, "Potassium is a key nutrient in Central Valley soils and almond hulls. Natural potassium is almost all potassium-39 (38.964 amu, 93.26%) and potassium-41 (40.962 amu, 6.73%). Using these two isotopes, what is potassium's average atomic mass?",
  ["39.09 amu", "39.96 amu", "3909 amu", "40.82 amu"],
  ["(0.9326)(38.964) + (0.0673)(40.962) = 36.3378 + 2.7567 = 39.09 amu, rounded once at the end.",
   "This is the simple average, which treats the two isotopes as equally common.",
   "This uses 93.26 and 6.73 instead of 0.9326 and 0.0673, so the answer is 100 times too big.",
   "This puts the 93.26% on potassium-41; the heavier isotope is the rare one."],
  "Fractional abundance = percent &divide; 100.",
  "(0.9326)(38.964) + (0.0673)(40.962) = 36.3378 + 2.7567 = <b>39.09 amu</b>, close to 39 because potassium-39 dominates. The abundances add to 99.99% because a tiny amount of potassium-40 (about 0.01%) is left out; including it brings the value to the periodic table's 39.098 amu.", 2, 1)

Q(T, "Silver, used in some dental alloys, is 51.84% silver-107 (106.905 amu) and 48.16% silver-109 (108.905 amu). What is the average atomic mass of silver?",
  ["107.87 amu", "107.91 amu", "107.94 amu", "10787 amu"],
  ["(0.5184)(106.905) + (0.4816)(108.905) = 55.42 + 52.45 = 107.87 amu, just below halfway because silver-107 is slightly more common.",
   "This is the simple average; with nearly equal abundances it comes close, but it ignores that silver-107 is a bit more common.",
   "This swaps the abundances, giving the heavier isotope the larger share.",
   "This uses the percents directly instead of dividing them by 100."],
  "With nearly equal abundances, the average is near halfway. Which side of halfway?",
  "(0.5184)(106.905 amu) + (0.4816)(108.905 amu) = 55.42 + 52.45 = <b>107.87 amu</b>. Silver-107 is slightly more abundant, so the answer sits just below the halfway value of 107.905.", 3, 1)

Q(T, "Neon has three natural isotopes. Use the data to calculate neon's average atomic mass.",
  ["20.18 amu", "20.12 amu", "20.99 amu", "2018 amu"],
  ["(0.9048)(19.992) + (0.0027)(20.994) + (0.0925)(21.991) = 18.09 + 0.057 + 2.03 = 20.18 amu.",
   "This leaves out neon-21. Even a small abundance must be included.",
   "This is the simple average of the three masses, which ignores that neon-20 makes up about 90% of neon.",
   "This multiplies by the percents instead of the fractions, so the answer is 100 times too big."],
  "Every isotope contributes (fraction &times; mass), even a rare one.",
  "(0.9048)(19.992) + (0.0027)(20.994) + (0.0925)(21.991) = 18.09 + 0.057 + 2.03 = <b>20.18 amu</b>. Rounded once at the end to the hundredths place.", 3, 1,
  [{"type": "table", "cap": "Natural isotopes of neon", "head": ["Isotope", "Mass (amu)", "Abundance (%)"],
    "rows": [["Neon-20", "19.992", "90.48"], ["Neon-21", "20.994", "0.27"], ["Neon-22", "21.991", "9.25"]]}])

Q(T, "A student calculates the average atomic mass of copper from its two isotopes (62.93 amu and 64.93 amu) and gets 6355 amu. What is the most likely mistake?",
  ["Multiplying by the percent abundances instead of the fractional abundances",
   "Taking a simple average instead of a weighted average",
   "Swapping the abundances of the two isotopes",
   "Rounding each product too early"],
  ["6355 is 100 times the expected 63.55; using 69.15 instead of 0.6915 makes every product 100 times too large.",
   "A simple average would give 63.93 amu, which is still between the two masses.",
   "Swapping abundances would give an answer near 64.3 amu, still between the two masses.",
   "Early rounding changes the last digit or two, not the size of the answer by a factor of 100."],
  "The average must fall between 62.93 and 64.93 amu. How far off is 6355?",
  "Any average must lie between the isotope masses. 6355 is <b>100 times too big</b>, the sign of using percents (69.15, 30.85) instead of fractions (0.6915, 0.3085). The correct answer is 63.55 amu.", 2)

Q(T, "An element has two isotopes with masses 20.0 amu and 22.0 amu. Which value <b>could</b> be its average atomic mass?",
  ["20.2 amu", "19.8 amu", "22.4 amu", "42.0 amu"],
  ["A weighted average must lie between the lightest and heaviest isotope masses; 20.2 does.",
   "An average cannot be smaller than the lightest isotope.",
   "An average cannot be larger than the heaviest isotope.",
   "This adds the two masses; an average lies between them."],
  "Where must a weighted average fall?",
  "Any weighted average lies between 20.0 and 22.0 amu, so only <b>20.2 amu</b> is possible. It would mean the lighter isotope is far more abundant.", 1)

Q(T, "Nitrogen is a major fertilizer element. Use the isotope data in the table to calculate nitrogen's average atomic mass.",
  ["14.01 amu", "14.50 amu", "15.00 amu", "1401 amu"],
  ["(0.9964)(14.003) + (0.0036)(15.000) = 13.953 + 0.054 = 14.01 amu.",
   "This is the simple average; nitrogen-15 is far too rare to pull the average halfway.",
   "This gives the 99.64% to nitrogen-15; the rare isotope is the heavier one.",
   "This uses percents directly; divide each by 100 first."],
  "Which isotope is far more abundant? The answer should be very close to its mass.",
  "(0.9964)(14.003) + (0.0036)(15.000) = 13.953 + 0.054 = <b>14.01 amu</b>, very close to 14 because nitrogen-14 is 99.64% of natural nitrogen.", 2, 1,
  [{"type": "table", "cap": "Natural isotopes of nitrogen", "head": ["Isotope", "Mass (amu)", "Abundance (%)"],
    "rows": [["Nitrogen-14", "14.003", "99.64"], ["Nitrogen-15", "15.000", "0.36"]]}])

Q(T, "Carbon's average atomic mass is 12.011 amu. Which statement about a <b>single</b> carbon atom in a breath sample is true?",
  ["Its mass is close to 12.000 amu or to 13.003 amu, depending on which isotope it is.",
   "Its mass is exactly 12.011 amu, like every carbon atom.",
   "It has 6.011 neutrons.",
   "It is most likely carbon-13, since 12.011 is more than 12."],
  ["A single atom is one isotope or another; no atom has the average mass, which describes the mixture.",
   "The average describes the mixture of isotopes; individual atoms have the mass of their own isotope.",
   "Every atom has a whole number of neutrons (6 for carbon-12, 7 for carbon-13).",
   "12.011 is only a little above 12, which shows that carbon-12 is by far the more common isotope (about 99%)."],
  "Is the average a property of one atom or of a large mixture of atoms?",
  "The 12.011 amu value is an average over a mixture that is about 99% carbon-12 and 1% carbon-13. <b>Any one atom has the mass of its own isotope</b>: about 12.000 or 13.003 amu.", 2)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
import collections
print(len(B), collections.Counter(q['t'] for q in B), 'figs', sum(1 for q in B if q.get('f')))
