#!/usr/bin/env python3
"""Builds bank/ch02_adapt.json (Chapter 2 ADAPT homework-only items, text only). Scratch generator."""
import json, sys
OUT = sys.argv[1]
def iso(A, Z, s, ch=''):
    return f'<sup>{A}</sup><sub>{Z}</sub>{s}' + (f'<sup>{ch}</sup>' if ch else '')
B = []
def Q(t, q, c, y, h, w, d, k=0):
    y = ["Correct: " + y[0]] + y[1:]
    B.append({"id": "c2-h%02d" % (len(B) + 1), "t": t, "q": q, "c": c, "y": y, "h": h, "w": w, "d": d, "k": k})

# ---------------- ch02-theory (6) ----------------
T = 'ch02-theory'
Q(T, "Which idea came from Rutherford's gold foil experiment rather than from Dalton's atomic theory?",
  ["An atom has a tiny, dense, positively charged nucleus.",
   "Atoms combine in simple whole-number ratios to form compounds.",
   "Atoms are not created or destroyed in a chemical reaction.",
   "Atoms of one element differ from the atoms of every other element."],
  ["Rutherford's alpha particles bouncing back from gold foil revealed the nucleus, about a century after Dalton.",
   "This is one of Dalton's main points; it explains the law of definite proportions.",
   "This is one of Dalton's main points; it explains the conservation of mass.",
   "This is one of Dalton's main points about elements."],
  "Dalton never looked inside an atom; Rutherford did.",
  "Dalton's theory (early 1800s) is about atoms as the units of elements and compounds. The <b>nucleus</b> was Rutherford's conclusion from the gold foil experiment (around 1909).", 1)

Q(T, "Thomson found that cathode rays were made of the same particles no matter which metal the tube's electrodes were made of. What did this suggest?",
  ["Electrons are a part of the atoms of every element.",
   "Each metal has its own kind of electron.",
   "Cathode rays are made of whole metal atoms.",
   "Cathode rays are positively charged."],
  ["Identical particles from every metal mean that the same particle is inside all atoms.",
   "The particles were the same for every metal, which is the opposite of each metal having its own kind.",
   "The particles were far lighter than any atom, so they could not be whole atoms.",
   "The beam bent toward a positive plate, which shows a negative charge."],
  "If the particle is the same from every source, where must it come from?",
  "The same tiny negative particle came out of every metal, so <b>electrons are part of all atoms</b>. Atoms are not indivisible after all.", 2)

Q(T, "Sodium fluoride, used in some fluoride rinses, is always 45.2% fluorine by mass. How many grams of fluorine are in 2.50 g of pure sodium fluoride?",
  ["1.13 g", "5.53 g", "113 g", "1.37 g"],
  ["0.452 &times; 2.50 g = 1.13 g (3 significant figures).",
   "This divides by 0.452 instead of multiplying; the fluorine must be less than the 2.50 g of compound.",
   "This multiplies by 45.2 instead of 0.452; divide the percent by 100 first.",
   "This is the sodium part (54.8% of the sample), not the fluorine."],
  "Percent by mass tells you grams of the element per 100 g of compound.",
  "Every sample of NaF has the same composition (law of definite proportions): 2.50 g &times; 0.452 = <b>1.13 g</b> of fluorine.", 2, 1)

Q(T, "Anhydrous ammonia, NH<sub>3</sub>, is a nitrogen fertilizer used on Valley farms. A 10.00 g sample of ammonia contains 8.23 g of nitrogen and 1.77 g of hydrogen. A second sample contains 41.2 g of nitrogen. How many grams of hydrogen does it contain?",
  ["8.86 g", "1.77 g", "192 g", "7.29 g"],
  ["The nitrogen-to-hydrogen mass ratio is fixed: 41.2 g N &times; (1.77 g H &divide; 8.23 g N) = 8.86 g H.",
   "The ratio of the elements is fixed, not the mass of hydrogen; more nitrogen means more hydrogen.",
   "This flips the ratio (8.23 &divide; 1.77), giving more hydrogen than nitrogen, which ammonia never has by mass.",
   "This takes 17.7% of the nitrogen mass, but 17.7% is hydrogen's share of the whole compound, not of the nitrogen."],
  "Set up the ratio grams H per gram N from the first sample, then use it for the second.",
  "Ammonia always has the same composition. 41.2 g N &times; (1.77 g H / 8.23 g N) = <b>8.86 g H</b>. Check: 8.86 &divide; (41.2 + 8.86) = 17.7% hydrogen, the same as the first sample.", 3, 1)

Q(T, "Suppose atoms were solid balls of dense positive charge that filled their whole volume. What would the gold foil experiment most likely have shown?",
  ["Many alpha particles would have been turned aside or bounced back.",
   "Every alpha particle would have passed straight through.",
   "The alpha particles would have bent toward the foil.",
   "Nothing different; the results do not depend on how mass is arranged."],
  ["If dense positive matter filled every atom, almost every alpha particle would hit it and be pushed away.",
   "Passing straight through needs mostly empty space, which these solid atoms would not have.",
   "Alpha particles are positive, so positive atoms would repel them, not attract them.",
   "The pattern of deflections is exactly what reveals how the mass and charge are arranged."],
  "Alpha particles are positive. What happens when they run into something positive and heavy?",
  "Dense positive matter everywhere would repel nearly every positive alpha particle, so <b>many would be deflected or bounce back</b>. The real result (most passed through) showed that atoms are mostly empty space.", 3)

Q(T, "In 1932, James Chadwick discovered a particle that explained why nuclei have more mass than their protons alone. Which particle?",
  ["The neutron", "The electron", "The alpha particle", "The proton"],
  ["The neutron has about the mass of a proton but no charge, so it adds mass to the nucleus without adding charge.",
   "The electron (Thomson, 1897) is outside the nucleus and far too light to explain the extra mass.",
   "Alpha particles were the tool Rutherford used to probe atoms; they are not a building block of every nucleus.",
   "The extra mass was beyond what the protons could account for, so another particle had to be present."],
  "The missing mass came from a particle with no charge.",
  "Chadwick found the <b>neutron</b>: about 1 amu, no charge, in the nucleus. It accounts for the mass that the protons alone cannot.", 1)

# ---------------- ch02-particles (7) ----------------
T = 'ch02-particles'
Q(T, "Selenium (Z = 34) is a trace element that people need in small amounts. How many protons and electrons are in a neutral selenium atom?",
  ["34 protons and 34 electrons", "79 protons and 79 electrons", "34 protons and 45 electrons", "34 protons and 36 electrons"],
  ["Z = 34 gives 34 protons, and a neutral atom has the same number of electrons.",
   "79 is selenium's average atomic mass (78.97) rounded; the atomic number gives the protons.",
   "45 is 79 &minus; 34, which would be a neutron count, not electrons.",
   "36 electrons is the count for the Se<sup>2&minus;</sup> ion, not the neutral atom."],
  "Neutral atom: electrons = protons = Z.",
  "Selenium: Z = 34, so <b>34 protons and 34 electrons</b> in the neutral atom.", 1)

Q(T, "A neutral atom has 27 electrons. This element sits at the center of vitamin B<sub>12</sub>. Which element is it?",
  ["Cobalt", "Nickel", "Iron", "Aluminum"],
  ["A neutral atom has equal protons and electrons, so Z = 27, which is cobalt (Co).",
   "Nickel has Z = 28, one more proton than this atom.",
   "Iron has Z = 26, one fewer proton than this atom.",
   "Aluminum has Z = 13; 27 is the mass number of its common isotope, not its atomic number."],
  "Neutral means protons = electrons. Find that atomic number on the periodic table.",
  "27 electrons in a neutral atom means 27 protons: Z = 27 is <b>cobalt</b>, Co.", 1)

Q(T, "Using the masses 1.0073 amu (proton), 1.0087 amu (neutron) and 0.00055 amu (electron), which particle has the <b>greatest</b> mass?",
  ["Neutron", "Proton", "Electron", "All three have the same mass."],
  ["1.0087 amu is slightly larger than 1.0073 amu, so the neutron is the heaviest, by a tiny amount.",
   "The proton is very close, but 1.0073 is a little smaller than 1.0087.",
   "The electron is about 1800 times lighter than the other two.",
   "Two of the particles are close to 1 amu, but the electron is far lighter, so the masses are not all equal."],
  "Compare the numbers digit by digit.",
  "The <b>neutron</b> (1.0087 amu) is very slightly heavier than the proton (1.0073 amu); both are about 1800 times heavier than the electron.", 2)

Q(T, "Copper (Z = 29) is a trace element needed by several enzymes. How many protons and electrons are in a neutral copper atom?",
  ["29 protons and 29 electrons", "64 protons and 64 electrons", "29 protons and 35 electrons", "29 protons and 0 electrons"],
  ["Z = 29 gives 29 protons, and a neutral atom has as many electrons as protons.",
   "64 comes from rounding the average atomic mass (63.55); the atomic number is 29.",
   "35 is 64 &minus; 29, which would be a neutron count, not electrons.",
   "A neutral atom needs electrons to balance its 29 protons."],
  "Use the whole number on the periodic table.",
  "Cu: Z = 29, so <b>29 protons and 29 electrons</b>.", 1)

Q(T, "Which statement about the electron is correct?",
  ["It is found outside the nucleus and has about 1/1800 the mass of a proton.",
   "It has a charge of 1+ and is found in the nucleus.",
   "It has a mass of about 1 amu.",
   "It has no charge."],
  ["Electrons move in the mostly empty space around the nucleus, and each is about 0.00055 amu.",
   "The electron is negative (1&minus;) and is outside the nucleus; the 1+ particle in the nucleus is the proton.",
   "About 1 amu describes protons and neutrons; the electron is about 0.00055 amu.",
   "The particle with no charge is the neutron; the electron is 1&minus;."],
  "Recall the charge, mass and location of each particle.",
  "The electron is <b>1&minus;, about 0.00055 amu (about 1/1800 of a proton), and outside the nucleus</b>.", 1)

Q(T, "Atom 1 has 15 protons and 16 neutrons. Atom 2 has 15 protons and 17 neutrons. Which statement is correct?",
  ["Both are phosphorus, because both have 15 protons.",
   "They are different elements, because they have different numbers of neutrons.",
   "They are different elements, because they have different masses.",
   "Their identity cannot be known without the number of electrons."],
  ["The atomic number (protons) alone decides the element, and Z = 15 is phosphorus.",
   "The neutron count can change without changing the element; the protons decide.",
   "Atoms of one element can have different masses (they are isotopes).",
   "The number of protons is enough; electrons can change when ions form."],
  "Which particle count defines the element?",
  "Both have <b>15 protons, so both are phosphorus</b>. They differ only in neutrons, so they are isotopes (phosphorus-31 and phosphorus-32).", 2)

Q(T, "The nucleus is about 1/100,000 of the diameter of the whole atom. If an atom were enlarged to the length of a 100 m football field, about how wide would its nucleus be?",
  ["About 1 mm", "About 1 cm", "About 1 m", "About 10,000 km"],
  ["100 m &divide; 100,000 = 0.001 m, which is 1 mm, about the size of a grain of sand.",
   "1 cm would be 1/10,000 of 100 m; one zero was dropped.",
   "1 m would be only 1/100 of the atom's width.",
   "This multiplies by 100,000 instead of dividing; the nucleus is much smaller than the atom."],
  "Divide the atom's size by 100,000.",
  "100 m &divide; 100,000 = 0.001 m = <b>about 1 mm</b>. The nucleus is tiny, yet it holds almost all the atom's mass.", 2, 1)

# ---------------- ch02-table (7) ----------------
T = 'ch02-table'
Q(T, "Mercury is one of the metals in dental amalgam. What is the symbol for mercury?",
  ["Hg", "Me", "Mr", "Mg"],
  ["Mercury's symbol comes from its Latin name, hydrargyrum.",
   "Me is not the symbol of any element.",
   "Mr is not the symbol of any element.",
   "Mg is magnesium, an alkaline earth metal."],
  "Mercury's symbol comes from a Latin name.",
  "Mercury is <b>Hg</b>, from <i>hydrargyrum</i> (&ldquo;liquid silver&rdquo;). Mg is magnesium.", 1)

Q(T, "Which element is in period 4, group 1?",
  ["Potassium", "Sodium", "Calcium", "Rubidium"],
  ["Group 1 in the fourth row is potassium (K), an element Valley growers add to soil.",
   "Sodium is in group 1 but in period 3.",
   "Calcium is in period 4 but in group 2.",
   "Rubidium is in group 1 but in period 5."],
  "Period = row, group = column.",
  "Row 4, column 1 is <b>potassium</b>, K, an alkali metal.", 1)

Q(T, "Iodine is the element that makes iodinated contrast media show up on X-ray and CT images. How is iodine classified?",
  ["A halogen (a group 17 nonmetal)", "A noble gas", "An alkali metal", "A transition metal"],
  ["Iodine is in group 17 with F, Cl and Br: the halogens, all nonmetals.",
   "Noble gases are in group 18; iodine is one column to the left.",
   "Alkali metals are in group 1, on the far left.",
   "Transition metals are in groups 3&ndash;12; iodine is a main-group element."],
  "Find iodine's group.",
  "Iodine (Z = 53) is in group 17: a <b>halogen</b> and a nonmetal. Its heavy atoms block X-rays, which is why it works in contrast media.", 1)

Q(T, "Boron is a micronutrient that almond trees need. Which of these elements is a <b>metalloid</b>?",
  ["Boron", "Aluminum", "Carbon", "Beryllium"],
  ["Boron is where the staircase line begins, and it has properties between those of metals and nonmetals.",
   "Aluminum is just left of the staircase: a metal.",
   "Carbon is right of the staircase: a nonmetal.",
   "Beryllium is in group 2: an alkaline earth metal."],
  "Metalloids lie along the staircase: B, Si, Ge, As, Sb, Te.",
  "<b>Boron</b> is a metalloid. Aluminum and beryllium are metals; carbon is a nonmetal.", 2)

Q(T, "Cobalt-60 has long been used as a radiation source in cancer therapy. Cobalt is in period 4, group 9. How is cobalt classified?",
  ["A transition metal", "A main-group metal", "A metalloid", "An alkaline earth metal"],
  ["Groups 3&ndash;12 are the transition metals, and group 9 is inside that block.",
   "Main-group elements are in groups 1, 2 and 13&ndash;18.",
   "Metalloids sit along the staircase on the right side of the table.",
   "Alkaline earth metals are in group 2."],
  "Which groups hold the transition metals?",
  "Group 9 is inside groups 3&ndash;12, so cobalt is a <b>transition metal</b>.", 1)

Q(T, "Hydrogen sits at the top of group 1. How is it classified?",
  ["A nonmetal", "An alkali metal", "A noble gas", "A metalloid"],
  ["Hydrogen is a colorless gas that does not conduct like a metal; it is a nonmetal even though it sits in group 1.",
   "The alkali metals are the metals below hydrogen (Li to Cs); hydrogen is not one of them.",
   "Noble gases are in group 18 and are very unreactive; hydrogen is reactive.",
   "Metalloids lie along the staircase; hydrogen is far from it."],
  "Hydrogen is a gas made of H<sub>2</sub> molecules.",
  "Hydrogen is a <b>nonmetal</b>. It sits above group 1, but it is not an alkali metal.", 1)

Q(T, "Ferrous sulfate is a common iron supplement. Which element does &ldquo;ferrous&rdquo; refer to, and what is its symbol?",
  ["Iron, Fe", "Fluorine, F", "Iridium, Ir", "Francium, Fr"],
  ["Ferrous comes from ferrum, the Latin name for iron, which gives the symbol Fe.",
   "F is fluorine, a halogen, not a metal used for iron supplements.",
   "Ir is iridium; iron's symbol does not come from its English name.",
   "Fr is francium, a rare radioactive alkali metal."],
  "Think of the Latin name for iron.",
  "Ferrous comes from <i>ferrum</i>, Latin for iron, so the element is <b>iron, Fe</b>.", 1)

# ---------------- ch02-ions (7) ----------------
T = 'ch02-ions'
Q(T, "Barium in X-ray contrast is present as the Ba<sup>2+</sup> ion. Barium has Z = 56. How many protons and electrons are in Ba<sup>2+</sup>?",
  ["56 protons and 54 electrons", "56 protons and 58 electrons", "54 protons and 54 electrons", "56 protons and 56 electrons"],
  ["Z = 56; a 2+ charge means two electrons lost: 56 &minus; 2 = 54.",
   "Adding electrons gives a negative ion; a 2+ ion has fewer electrons than protons.",
   "The protons never change when an ion forms; 54 protons would be xenon.",
   "56 electrons is the neutral atom; the 2+ charge means two were lost."],
  "Electrons = protons &minus; charge.",
  "Ba: Z = 56, so <b>56 protons</b>; 56 &minus; 2 = <b>54 electrons</b>.", 1, 1)

Q(T, "An ion has 26 protons and 23 electrons. Which ion is it?",
  ["Fe<sup>3+</sup>", "Fe<sup>3&minus;</sup>", "V, a vanadium atom", "Fe<sup>2+</sup>"],
  ["26 protons is iron, and 26 &minus; 23 = +3.",
   "Fewer electrons than protons means a positive charge, not a negative one.",
   "Vanadium has 23 protons; 23 is the electron count, and the element is set by the protons.",
   "Fe<sup>2+</sup> would have 24 electrons."],
  "Protons name the element; charge = protons &minus; electrons.",
  "Z = 26 is iron; 26 &minus; 23 = 3+, so the ion is <b>Fe<sup>3+</sup></b>.", 2, 1)

Q(T, "Predict the usual ion formed by selenium (group 16) and name it.",
  ["Se<sup>2&minus;</sup>, selenide", "Se<sup>2+</sup>, selenium ion", "Se<sup>6+</sup>, selenium ion", "Se<sup>&minus;</sup>, selenide"],
  ["Group 16 nonmetals gain two electrons to form 2&minus; ions, and monatomic anions end in -ide.",
   "Nonmetals in group 16 gain electrons, so the charge is negative.",
   "The group number 16 does not give a 6+ charge; group 16 elements gain two electrons.",
   "The -ide name is right, but group 16 gains two electrons, not one; 1&minus; is the group 17 charge."],
  "Group 16 is two columns left of the noble gases.",
  "Group 16 forms 2&minus; ions: <b>Se<sup>2&minus;</sup>, selenide</b>, like O<sup>2&minus;</sup> (oxide) and S<sup>2&minus;</sup> (sulfide).", 2)

Q(T, "A lab report shows <b>hypocalcemia</b>. What does this term mean?",
  ["Low blood calcium", "High blood calcium", "Low blood potassium", "Low blood sodium"],
  ["Hypo- means below the normal range, and -calcemia refers to calcium in the blood.",
   "High would be hyper-; hypo- means low.",
   "Low potassium is hypokalemia, from potassium's Latin name kalium.",
   "Low sodium is hyponatremia, from sodium's Latin name natrium."],
  "Split the word: hypo- + calc + -emia.",
  "Hypo- (low) + calc (calcium) + -emia (in the blood): <b>low blood calcium</b>. Ca<sup>2+</sup> ions are needed for muscle contraction, including the heart.", 1)

Q(T, "How many protons and electrons are in the phosphide ion, P<sup>3&minus;</sup>?",
  ["15 protons and 18 electrons", "15 protons and 12 electrons", "18 protons and 18 electrons", "15 protons and 15 electrons"],
  ["Phosphorus has Z = 15; a 3&minus; charge means three extra electrons: 15 + 3 = 18.",
   "This subtracts the charge; a negative ion has more electrons than protons.",
   "The protons stay at Z = 15; 18 protons would be argon.",
   "Equal protons and electrons is the neutral phosphorus atom."],
  "For an anion, electrons = protons + size of the charge.",
  "P: Z = 15, so <b>15 protons</b>; 3&minus; means <b>18 electrons</b>. Check: 15 &minus; 18 = &minus;3.", 1, 1)

Q(T, "Which ion has the same number of electrons as a neutral neon atom (10 electrons)?",
  ["Na<sup>+</sup>", "K<sup>+</sup>", "Cl<sup>&minus;</sup>", "Ca<sup>2+</sup>"],
  ["Sodium has 11 protons; losing one electron leaves 10, the same as neon.",
   "Potassium has 19 protons, so K<sup>+</sup> has 18 electrons.",
   "Chlorine has 17 protons, so Cl<sup>&minus;</sup> has 18 electrons.",
   "Calcium has 20 protons, so Ca<sup>2+</sup> has 18 electrons."],
  "Find each ion's electrons: protons &minus; charge.",
  "Na<sup>+</sup>: 11 &minus; 1 = <b>10 electrons</b>, like neon. K<sup>+</sup>, Cl<sup>&minus;</sup> and Ca<sup>2+</sup> each have 18, like argon. Chapter 3 explains why ions often match a noble gas.", 2, 1)

Q(T, "An ion has 53 protons and 54 electrons. What is its charge?",
  ["1&minus;", "1+", "0", "54&minus;"],
  ["Charge = protons &minus; electrons = 53 &minus; 54 = &minus;1.",
   "More electrons than protons gives a negative charge.",
   "The numbers of protons and electrons are not equal, so the particle is charged.",
   "The charge is the difference between protons and electrons, not the electron count."],
  "Charge = protons &minus; electrons.",
  "53 &minus; 54 = <b>1&minus;</b>. Z = 53 is iodine, so this is the iodide ion, I<sup>&minus;</sup>.", 1, 1)

# ---------------- ch02-isotopes (7) ----------------
T = 'ch02-isotopes'
Q(T, "Iodine-123 is used for thyroid imaging. Iodine has Z = 53. How many protons, neutrons and electrons are in a neutral iodine-123 atom?",
  ["53 protons, 70 neutrons, 53 electrons", "53 protons, 123 neutrons, 53 electrons", "70 protons, 53 neutrons, 70 electrons", "53 protons, 70 neutrons, 70 electrons"],
  ["Protons = Z = 53; neutrons = 123 &minus; 53 = 70; neutral, so 53 electrons.",
   "123 is the mass number, which counts protons and neutrons together.",
   "This swaps protons and neutrons; the protons always equal Z.",
   "A neutral atom has as many electrons as protons, not as many as neutrons."],
  "Protons = Z; neutrons = A &minus; Z; neutral electrons = protons.",
  "<b>53 protons</b>, <b>70 neutrons</b> (123 &minus; 53) and <b>53 electrons</b>.", 1, 1)

Q(T, "Cobalt-60 is a radiation source. Cobalt has Z = 27. How many neutrons are in a cobalt-60 nucleus?",
  ["33", "60", "27", "87"],
  ["Neutrons = A &minus; Z = 60 &minus; 27 = 33.",
   "60 is the mass number (protons plus neutrons).",
   "27 is the number of protons.",
   "This adds A and Z instead of subtracting."],
  "Neutrons = mass number &minus; atomic number.",
  "60 &minus; 27 = <b>33 neutrons</b>.", 1, 1)

Q(T, "Rubidium-82 is used in some heart PET scans. An atom of it has 37 protons and 45 neutrons. Which name is correct?",
  ["Rubidium-82", "Rubidium-45", "Rubidium-85", "Rhodium-82"],
  ["37 protons is rubidium, and 37 + 45 = 82 is the mass number.",
   "45 is the neutron count; the number in the name is protons plus neutrons.",
   "85 comes from rubidium's average atomic mass (85.47), not from this atom's particles.",
   "Rhodium has Z = 45; 45 is this atom's neutron count, and the element is set by its 37 protons."],
  "Element from the protons; mass number = protons + neutrons.",
  "Z = 37 is rubidium; A = 37 + 45 = 82: <b>rubidium-82</b>.", 2, 1)

Q(T, "Carbon-14 and nitrogen-14 have the same mass number. Which statement is true?",
  ["Carbon-14 has one more neutron than nitrogen-14.",
   "They have the same number of neutrons.",
   "Nitrogen-14 has one more neutron than carbon-14.",
   "They are isotopes of each other."],
  ["Carbon-14 has 14 &minus; 6 = 8 neutrons; nitrogen-14 has 14 &minus; 7 = 7.",
   "Same mass number with different protons means different neutron counts.",
   "Nitrogen has one more proton, so it needs one fewer neutron to reach 14.",
   "Isotopes must be the same element; these have 6 and 7 protons."],
  "Neutrons = A &minus; Z for each atom.",
  "C-14: 14 &minus; 6 = 8 neutrons. N-14: 14 &minus; 7 = 7 neutrons. <b>Carbon-14 has one more neutron</b>. Same A does not make atoms isotopes.", 2, 1)

Q(T, "Iodide in iodized salt is mostly the stable isotope iodine-127. How many protons, neutrons and electrons are in one " + iso(127, 53, 'I', '&minus;') + " ion?",
  ["53 protons, 74 neutrons, 54 electrons", "53 protons, 74 neutrons, 52 electrons", "53 protons, 127 neutrons, 54 electrons", "53 protons, 73 neutrons, 54 electrons"],
  ["Protons = 53; neutrons = 127 &minus; 53 = 74; a 1&minus; charge adds one electron: 54.",
   "This removes an electron, which would give a 1+ ion.",
   "127 is the mass number; neutrons are A &minus; Z.",
   "The charge changes electrons only, never neutrons."],
  "Z = protons; neutrons = A &minus; Z; electrons = protons &minus; charge.",
  "<b>53 protons</b>, <b>74 neutrons</b> (127 &minus; 53), <b>54 electrons</b> (53 + 1).", 2, 1)

Q(T, "Potassium-40 is a naturally radioactive isotope found in small amounts in the body and in foods such as bananas and almonds. Potassium has Z = 19. How many neutrons does potassium-40 have?",
  ["21", "40", "19", "20"],
  ["Neutrons = 40 &minus; 19 = 21.",
   "40 is the mass number.",
   "19 is the number of protons.",
   "20 is the neutron count of potassium-39, the common isotope, not potassium-40."],
  "Neutrons = A &minus; Z.",
  "40 &minus; 19 = <b>21 neutrons</b>.", 1, 1)

Q(T, "Which atom is <b>not</b> an isotope of oxygen?",
  [iso(18, 9, 'F'), iso(16, 8, 'O'), iso(17, 8, 'O'), iso(18, 8, 'O')],
  ["Its atomic number is 9, so it is fluorine, even though its mass number (18) matches one oxygen isotope.",
   "Z = 8 is oxygen; this is oxygen-16.",
   "Z = 8 is oxygen; this is oxygen-17.",
   "Z = 8 is oxygen; this is oxygen-18."],
  "Isotopes of oxygen all have Z = 8.",
  "Every oxygen isotope has 8 protons. " + iso(18, 9, 'F') + " has 9 protons, so it is <b>fluorine-18</b>, not oxygen.", 1)

# ---------------- ch02-mass (6) ----------------
T = 'ch02-mass'
Q(T, "Copper is 69.15% copper-63 (62.930 amu) and 30.85% copper-65 (64.928 amu). Calculate copper's average atomic mass.",
  ["63.55 amu", "63.93 amu", "64.31 amu", "6355 amu"],
  ["(0.6915)(62.930) + (0.3085)(64.928) = 43.52 + 20.03 = 63.55 amu.",
   "This is the simple average; it ignores that copper-63 is more than twice as common.",
   "This swaps the abundances, giving the larger share to copper-65.",
   "This uses the percents directly instead of dividing by 100."],
  "Fraction &times; mass for each isotope, then add.",
  "(0.6915)(62.930) + (0.3085)(64.928) = 43.52 + 20.03 = <b>63.55 amu</b>, closer to 63 as expected.", 2, 1)

Q(T, "Rubidium is 72.17% rubidium-85 (84.912 amu) and 27.83% rubidium-87 (86.909 amu). Calculate rubidium's average atomic mass.",
  ["85.47 amu", "85.91 amu", "86.35 amu", "8547 amu"],
  ["(0.7217)(84.912) + (0.2783)(86.909) = 61.28 + 24.19 = 85.47 amu.",
   "This is the simple average, which treats both isotopes as equally common.",
   "This swaps the abundances.",
   "This uses percents instead of fractions."],
  "The answer should be closer to the more abundant isotope.",
  "(0.7217)(84.912) + (0.2783)(86.909) = 61.28 + 24.19 = <b>85.47 amu</b>.", 2, 1)

Q(T, "Carbon is 98.93% carbon-12 (12.000 amu) and 1.07% carbon-13 (13.003 amu). Calculate carbon's average atomic mass.",
  ["12.01 amu", "12.50 amu", "12.99 amu", "1201 amu"],
  ["(0.9893)(12.000) + (0.0107)(13.003) = 11.87 + 0.139 = 12.01 amu.",
   "This is the simple average; carbon-13 is far too rare to pull the average halfway.",
   "This gives the 98.93% to carbon-13.",
   "This uses the percents directly; divide each by 100 first."],
  "Almost all carbon is carbon-12, so the answer is just above 12.",
  "(0.9893)(12.000) + (0.0107)(13.003) = 11.87 + 0.139 = <b>12.01 amu</b>. The small amount of carbon-13 in breath is why the urea breath test must look for <i>extra</i> carbon-13.", 2, 1)

Q(T, "Oxygen has three natural isotopes: oxygen-16 (15.995 amu, 99.757%), oxygen-17 (16.999 amu, 0.038%) and oxygen-18 (17.999 amu, 0.205%). Calculate oxygen's average atomic mass.",
  ["15.999 amu", "15.993 amu", "16.998 amu", "1599.9 amu"],
  ["(0.99757)(15.995) + (0.00038)(16.999) + (0.00205)(17.999) = 15.956 + 0.0065 + 0.0369 = 15.999 amu.",
   "This leaves out oxygen-17; every isotope must be included, even a rare one.",
   "This is the simple average of the three masses, which ignores that oxygen-16 is over 99% of oxygen.",
   "This uses the percents directly instead of the fractions."],
  "Three isotopes means three products to add.",
  "15.956 + 0.0065 + 0.0369 = <b>15.999 amu</b>, the value on the periodic table.", 3, 1)

Q(T, "Iridium has two natural isotopes, iridium-191 and iridium-193. Its average atomic mass is 192.22 amu. Which isotope is more abundant?",
  ["Iridium-193", "Iridium-191", "They are equally abundant.", "It cannot be told from the average."],
  ["192.22 is above the halfway point (about 192), so the heavier isotope must be more common.",
   "If iridium-191 were more common, the average would be below 192.",
   "Equal amounts would put the average at about 192.0.",
   "Where the average falls between the isotope masses is enough to decide."],
  "Compare the average with the halfway point between 191 and 193.",
  "Halfway is about 192; 192.22 is closer to 193, so <b>iridium-193</b> is more abundant (about 63%).", 2)

Q(T, "Element X has two isotopes. X-50 makes up 25.0% of the atoms and X-52 makes up 75.0%. Treating each isotope's mass as equal to its mass number, estimate X's average atomic mass.",
  ["51.5 amu", "51.0 amu", "50.5 amu", "5150 amu"],
  ["(0.250)(50) + (0.750)(52) = 12.5 + 39.0 = 51.5 amu, closer to 52 because X-52 is three times as common.",
   "This is the simple average of 50 and 52, which ignores the abundances.",
   "This swaps the abundances, giving 75% to X-50.",
   "This uses 25.0 and 75.0 instead of 0.250 and 0.750."],
  "Three of every four atoms are X-52.",
  "(0.250)(50) + (0.750)(52) = 12.5 + 39.0 = <b>51.5 amu</b>.", 2, 1)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
import collections
print(len(B), collections.Counter(q['t'] for q in B))
