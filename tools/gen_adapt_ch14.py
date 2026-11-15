#!/usr/bin/env python3
"""Builds bank/ch14_adapt.json (Chapter 14 ADAPT homework-only items, text only; 42 items, none repeated from
bank/ch14.json).
usage: python3 tools/gen_adapt_ch14.py bank/ch14_adapt.json
Same conventions, helpers and markup as tools/gen_bank_ch14.py (imported from it): A and Z conserved; particle
symbols as in Section 14.2; whole numbers of half-lives (amount keeps the initial amount's s.f., time keeps the
half-life's); ages = n x 5730 years to 3 s.f.; 1 Ci = 3.7 x 10^10 Bq exact (1 mCi = 37 MBq); inverse-square law.
y[0] begins "Correct: ". Every item is rechecked by tools/check_bank_ch14.py."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bank_ch14 import *
import gen_bank_ch14 as G
G.CFG.update(prefix='c14-h%02d', adapt=True)


def build_hw():
    # ======================= ch14-radiation (6) =======================
    T = 'ch14-radiation'
    a = '6.40'; v = D(a) * D('3.7e7') / D('1e6')
    Q(T, "A gallium-67 dose has an activity of %s mCi. What is its activity in megabecquerels (MBq)? (1 Ci = 3.7 &times; 10<sup>10</sup> Bq, exact; 1 MBq = 10<sup>6</sup> Bq)" % a,
      [S(v, 3, 'MBq'), S(D(a) / 37, 3, 'MBq'), S(D(a) * D('3.7e7'), 3, 'MBq'), S(D(a) * D('3.7e10') / D('1e6'), 3, 'MBq')],
      ["%s mCi &times; 3.7 &times; 10<sup>7</sup> Bq/mCi = %s Bq = %s MBq (1 mCi = 37 MBq)." % (a, num(D(a) * D('3.7e7'), 3), num(v, 3)),
       "This divides by 37; each millicurie is 37 MBq, so multiply.",
       "This is the answer in becquerels; divide by 10<sup>6</sup> to get MBq.",
       "This treats mCi as Ci; divide by 1000 first."],
      "1 mCi = 3.7 &times; 10<sup>7</sup> Bq = 37 MBq.",
      "%s &times; 37 MBq = <b>%s</b>." % (a, S(v, 3, 'MBq')), 2, 1)

    Q(T, "Cesium-137 is a fission product released in the Chernobyl and Fukushima accidents. How many protons and neutrons are in one cesium-137 nucleus?",
      ["55 protons and 82 neutrons", "82 protons and 55 neutrons", "55 protons and 137 neutrons", "137 protons and 55 neutrons"],
      ["Cesium is element 55; neutrons = 137 &minus; 55 = 82.",
       "This swaps the counts; the atomic number, 55, is the number of protons.",
       "137 counts protons and neutrons together; subtract the 55 protons.",
       "137 is the mass number, not the number of protons."],
      "Z from the periodic table; neutrons = A &minus; Z.",
      "[[Cs-137]]: 55 protons, 137 &minus; 55 = <b>82 neutrons</b>.", 1)

    Q(T, "Marie Curie named one of the elements she discovered for her home country. Which element is it?",
      ["Polonium", "Radium", "Curium", "Francium"],
      ["Polonium is named for Poland, where Marie Curie (born Maria Sk&#322;odowska) grew up.",
       "Radium, her other discovery, is named for its strong radiation (Latin <i>radius</i>, ray).",
       "Curium was made in 1944 and named in honor of the Curies; it is not one of her discoveries.",
       "Francium is named for France and was discovered by Marguerite Perey in 1939."],
      "Her home country was Poland.",
      "<b>Polonium</b>, for Poland.", 1)

    Q(T, "What does a <b>sievert</b> (Sv) measure?",
      ["The equivalent (biological) dose: absorbed dose adjusted for how harmful the radiation is",
       "The number of decays per second in a source", "The energy given off by a source per second",
       "The time for half of a sample to decay"],
      ["Sieverts (and the older rem, 1 Sv = 100 rem) describe the dose to a person; doses are usually given in millisieverts.",
       "Decays per second is activity, in becquerels or curies.",
       "Sieverts describe what a person absorbs, not what a source emits.",
       "That is the half-life, a time."],
      "Which family of units describes the person?",
      "Sievert = <b>equivalent (biological) dose</b>.", 2)

    Q(T, "A nuclear medicine technologist finishes preparing doses and wants to check her gloves and the bench for spilled tracer. Which instrument should she use?",
      ["A survey meter, such as a Geiger counter", "Her dosimeter badge", "A gamma camera", "A film badge read at the end of the month"],
      ["A Geiger counter clicks right away when it is near contamination, so it can find a spill on the spot.",
       "A dosimeter records her total dose for a lab to read later; it cannot locate a spill now.",
       "A gamma camera images a patient; it is not a hand-held survey tool.",
       "A film badge also records total dose over time; it cannot find contamination right now."],
      "She needs an instant reading, not a monthly report.",
      "<b>A survey meter (Geiger counter)</b> gives an immediate reading.", 2)

    Q(T, "Which isotope must be radioactive, without looking anything up?",
      ["Thorium-232", "Carbon-12", "Potassium-39", "Oxygen-16"],
      ["Thorium is element 90; every isotope of every element beyond bismuth (atomic number 83) is radioactive.",
       "Carbon-12 is stable; carbon-14 is the radioactive isotope of carbon.",
       "Potassium-39 is stable; potassium-40 is the radioactive one.",
       "Oxygen-16 is stable; an element can have both stable and radioactive isotopes."],
      "Find the element beyond atomic number 83.",
      "Z = 90 &gt; 83: <b>thorium-232</b> must be radioactive.", 2)

    # ======================= ch14-decay (11) =======================
    T = 'ch14-decay'
    Q(T, "Plutonium-238 powers spacecraft such as the Mars rovers; it decays by alpha emission. What is the product? [[Pu-238]] -> ? + [[alpha]]",
      ["[[U-234]] (uranium-234)", "[[Np-234]] (neptunium-234)", "[[U-236]] (uranium-236)", "[[Pu-234]] (plutonium-234)"],
      ["A: 238 &minus; 4 = 234. Z: 94 &minus; 2 = 92, uranium.",
       "This lowers Z by only 1; an alpha particle carries 2 protons.",
       "This lowers A by only 2; an alpha particle has A = 4.",
       "This keeps Z = 94; the element must change."],
      "Subtract 4 from the top number and 2 from the bottom.",
      "<b>[[U-234]]</b>: 234 + 4 = 238 and 92 + 2 = 94.", 2)

    Q(T, "Samarium-153, used to relieve bone pain from cancer, is a beta emitter. What is the product? [[Sm-153]] -> ? + [[beta]]",
      ["[[Eu-153]] (europium-153)", "[[Pm-153]] (promethium-153)", "[[Eu-154]] (europium-154)", "[[Gd-153]] (gadolinium-153)"],
      ["A stays 153; Z = 62 + 1 = 63, europium.",
       "This lowers Z; a beta particle counts as &minus;1, so the new atomic number is one higher.",
       "A beta particle has A = 0, so the mass number stays 153.",
       "This raises Z by 2; beta decay raises it by 1."],
      "Beta decay: A the same, Z + 1.",
      "<b>[[Eu-153]]</b>: 153 = 153 + 0 and 62 = 63 &minus; 1.", 2)

    Q(T, "Rubidium-82, a positron emitter made in a generator at the hospital, is used in PET scans of heart blood flow. What is the product? [[Rb-82]] -> ? + [[positron]]",
      ["[[Kr-82]] (krypton-82)", "[[Sr-82]] (strontium-82)", "[[Rb-81]] (rubidium-81)", "[[Br-78]] (bromine-78)"],
      ["A stays 82; Z = 37 &minus; 1 = 36, krypton. Positron emission moves one place to the left.",
       "This raises Z, as beta decay would; a positron carries away +1, so Z drops.",
       "This lowers A and keeps the element; A stays 82 and Z drops by 1.",
       "This is alpha decay (A &minus; 4, Z &minus; 2); a positron has A = 0."],
      "A positron is [[positron]].",
      "<b>[[Kr-82]]</b>: 82 = 82 + 0 and 37 = 36 + 1.", 2)

    Q(T, "Gallium-67 decays by electron capture. What is the product? [[Ga-67]] + [[e]] -> ?",
      ["[[Zn-67]] (zinc-67)", "[[Ge-67]] (germanium-67)", "[[Zn-66]] (zinc-66)", "[[Ga-67]] (gallium-67, unchanged)"],
      ["The electron is a reactant: A = 67 + 0 = 67; Z = 31 &minus; 1 = 30, zinc.",
       "This raises Z, as if a beta particle were given off; a captured electron lowers Z.",
       "The electron's mass number is 0, so A stays 67.",
       "A proton becomes a neutron, so the element changes."],
      "Add the electron on the left.",
      "<b>[[Zn-67]]</b>.", 3)

    Q(T, "In 1932, James Chadwick discovered a new particle by hitting beryllium-9 with alpha particles. Identify the missing particle: [[Be-9]] + [[alpha]] -> [[C-12]] + ?",
      ["[[n]], a neutron", "[[p]], a proton", "[[gamma]], a gamma ray", "[[beta]], a beta particle"],
      ["Left: A = 13, Z = 6. Right so far: A = 12, Z = 6. Missing: A = 1, Z = 0, a neutron, the particle Chadwick discovered.",
       "A proton has Z = 1; the atomic numbers already balance (6 = 6), so the missing particle has Z = 0.",
       "A gamma ray has A = 0; one mass unit is still missing.",
       "A beta particle has A = 0 and Z = &minus;1; the totals would not match."],
      "Total each side, then subtract.",
      "Missing A = 13 &minus; 12 = 1, Z = 6 &minus; 6 = 0: <b>a neutron</b>.", 3)

    Q(T, "Copper-64 is used in some PET scans. What kind of decay is this? [[Cu-64]] -> [[Ni-64]] + [[positron]]",
      ["Positron emission", "Beta decay", "Electron capture", "Gamma emission"],
      ["A positron is a product; Z drops from 29 to 28 and A stays 64.",
       "Beta decay gives off [[beta]] and raises Z; here Z drops.",
       "Electron capture also lowers Z, but the electron is a reactant on the left; here a positron is a product.",
       "Gamma emission changes neither A nor Z; here Z changes."],
      "Which particle is a product?",
      "<b>Positron emission</b>.", 1)

    Q(T, "Thorium-232, found in many rocks, is an alpha emitter. Which equation is balanced?",
      ["[[Th-232]] -> [[Ra-228]] + [[alpha]]", "[[Th-232]] -> [[Ra-230]] + [[alpha]]", "[[Th-232]] -> [[Ac-228]] + [[alpha]]",
       "[[Th-232]] -> [[Rn-228]] + [[alpha]]"],
      ["Top: 228 + 4 = 232. Bottom: 88 + 2 = 90.",
       "Top: 230 + 4 = 234, not 232.",
       "Bottom: 89 + 2 = 91, not 90.",
       "Bottom: 86 + 2 = 88, not 90."],
      "Check the top total and the bottom total of each.",
      "<b>[[Th-232]] &rarr; [[Ra-228]] + [[alpha]]</b>.", 2)

    Q(T, "A nucleus gives off an alpha particle and becomes thorium-231. What was the starting nucleus? ? -> [[Th-231]] + [[alpha]]",
      ["[[U-235]] (uranium-235)", "[[Ra-227]] (radium-227)", "[[Pa-235]] (protactinium-235)", "[[Th-235]] (thorium-235)"],
      ["A = 231 + 4 = 235; Z = 90 + 2 = 92, uranium.",
       "This subtracts the alpha particle; the parent has the larger numbers.",
       "This adds only 1 to Z; add 2.",
       "This keeps Z = 90; the parent has 2 more protons."],
      "The parent's numbers equal the totals on the right.",
      "<b>[[U-235]]</b>.", 3)

    Q(T, "Which kind of radiation has the <b>lowest</b> ionizing power?",
      ["Gamma rays", "Alpha particles", "Beta particles", "Alpha and beta particles equally"],
      ["Gamma rays have no mass and no charge, so they pass most atoms without interacting: most penetrating, least ionizing.",
       "Alpha particles have the <i>highest</i> ionizing power.",
       "Beta particles are in the middle.",
       "Alpha particles ionize far more than beta particles."],
      "Ionizing power is the reverse of penetrating power.",
      "Ionizing power alpha &gt; beta &gt; gamma: <b>gamma rays</b>.", 2)

    Q(T, "A researcher works with a vial of a pure beta emitter, phosphorus-32. Which protection is appropriate for her hands and body?",
      ["A lab coat, gloves, and a plastic or aluminum shield", "Nothing; beta particles cannot get through skin",
       "Only a sheet of paper", "Thick lead or concrete, because beta is the most penetrating radiation"],
      ["Beta particles pass through paper but are stopped by aluminum, plastic, wood, or a lab coat and gloves.",
       "Beta particles penetrate a few millimeters into tissue; skin alone is not enough. (Alpha particles are the ones skin stops.)",
       "Paper stops alpha particles, not beta particles.",
       "Gamma rays are the most penetrating; beta needs only light shielding."],
      "Paper stops alpha; what stops beta?",
      "<b>Lab coat, gloves, and a plastic or aluminum shield</b>.", 2)

    Q(T, "Which radiation has a mass number of 0 and a charge of 0?",
      ["A gamma ray, [[gamma]]", "A neutron, [[n]]", "A positron, [[positron]]", "A beta particle, [[beta]]"],
      ["A gamma ray is pure energy (high-energy light), so it changes neither A nor Z.",
       "A neutron has no charge, but its mass number is 1.",
       "A positron has a mass number of 0 but a charge of +1.",
       "A beta particle has a mass number of 0 but a charge of &minus;1."],
      "Which one is light, not a particle with mass?",
      "<b>Gamma ray</b>: A = 0, charge 0.", 1)

    # ======================= ch14-halflife (10) =======================
    T = 'ch14-halflife'
    a, t, h = '6.80', '15.75', '5.25'; n = 3
    Q(T, "Xenon-133 (half-life %s days) is used in lung ventilation scans. A vial contains %s mCi of xenon-133. What activity remains after %s days?" % (h, a, t),
      [AM(a, n, 'mCi'), AM(a, n + 1, 'mCi'), S(D(a) / (2 * n), 3, 'mCi'), S(D(a) * n / 2, 3, 'mCi')],
      ["n = %s &divide; %s = 3; %s &divide; 8." % (t, h, a),
       "This halves four times; n = 3.",
       "This divides by 2 &times; 3 = 6 instead of 2<sup>3</sup> = 8.",
       "This multiplies by (1/2) &times; 3; the activity must drop."],
      "n = time &divide; half-life.",
      "%s = <b>%s</b>." % (steps(a, n, 'mCi'), AM(a, n, 'mCi')), 2, 1)

    a, t, h = '3.60', '55.4', '27.7'; n = 2
    Q(T, "Chromium-51 (half-life %s days) is used to measure red blood cell survival. A sample has an activity of %s &mu;Ci. What is its activity after %s days?" % (h, a, t),
      [AM(a, n, '&mu;Ci'), AM(a, n - 1, '&mu;Ci'), '0 &mu;Ci', AM(a, n + 1, '&mu;Ci')],
      ["n = %s &divide; %s = 2; %s &times; 1/4." % (t, h, a),
       "This halves once; %s days is two half-lives." % t,
       "This subtracts half of the <i>original</i> amount twice; each half-life halves what is left.",
       "This halves three times; n = 2."],
      "Halve once per half-life.",
      "%s = <b>%s</b>." % (steps(a, n, '&mu;Ci'), AM(a, n, '&mu;Ci')), 2, 1)

    a, t, h = '7.20', '26.6', '6.65'; n = 4
    Q(T, "Lutetium-177 (half-life %s days) treats some neuroendocrine tumors. A dose has an activity of %s GBq. What activity remains after %s days?" % (h, a, t),
      [AM(a, n, 'GBq'), AM(a, n - 1, 'GBq'), AM(a, n + 1, 'GBq'), S(D(a) * n / 2, 3, 'GBq')],
      ["n = %s &divide; %s = 4; %s &divide; 16." % (t, h, a),
       "This halves only three times; n = 4.",
       "This halves five times; count the half-lives, not the amounts.",
       "This multiplies by (1/2) &times; 4 = 2 instead of (1/2)<sup>4</sup> = 1/16."],
      "Find n first.",
      "%s = <b>%s</b>." % (steps(a, n, 'GBq'), AM(a, n, 'GBq')), 3, 1)

    a, b, h = '10.4', '2.60', '73.8'; n = 2
    Q(T, "Iridium-192 (half-life %s days) sources are used in brachytherapy. How long does it take a %s Ci source to decay to %s Ci?" % (h, a, b),
      [TM(h, n, 'days'), TM(h, n + 1, 'days'), S(D(h) / n, 3, 'days'), TM(h, 4, 'days')],
      ["%s &rarr; 5.20 &rarr; %s Ci is 2 half-lives; 2 &times; %s days." % (a, b, h),
       "This counts the three amounts; there are two halvings.",
       "This divides the half-life by 2; time = n &times; half-life.",
       "This multiplies by 4 (from the fraction 1/4); 1/4 is 2 half-lives."],
      "Halve %s until you reach %s." % (a, b),
      "2 &times; %s = <b>%s</b>." % (h, TM(h, n, 'days')), 2, 1)

    a, b, t = '6.40', '0.400', '34.8'; n = 4
    Q(T, "A %s g sample of a short-lived radioisotope decays to %s g in %s min. What is its half-life?" % (a, b, t),
      [S(D(t) / n, 3, 'min'), t + ' min', S(D(t) / (n + 1), 3, 'min'), S(D(t) / (n - 1), 3, 'min')],
      ["%s &rarr; 3.20 &rarr; 1.60 &rarr; 0.800 &rarr; %s g is 4 half-lives; %s &divide; 4." % (a, b, t),
       "This treats the whole time as one half-life.",
       "This divides by 5, the number of amounts in the chain.",
       "This divides by 3; there are 4 halvings."],
      "Count the halvings, then divide the time by n.",
      "%s &divide; 4 = <b>%s</b>." % (t, S(D(t) / n, 3, 'min')), 2, 1)

    a, t, h = '0.600', '8.40', '2.80'; n = 3
    Q(T, "Indium-111 (half-life %s days) labels white blood cells to find infections. %s days after a dose was made, %s mCi remains. What was the starting activity?" % (h, t, a),
      [S(D(a) * 2 ** n, 3, 'mCi'), S(D(a) / 2 ** n, 3, 'mCi'), S(D(a) * 2 ** (n - 1), 3, 'mCi'), S(D(a) * n, 3, 'mCi')],
      ["n = %s &divide; %s = 3; working backward, double 3 times: %s &times; 8." % (t, h, a),
       "This halves; going back to the start, the activity must get larger.",
       "This doubles only twice; n = 3.",
       "This multiplies by n = 3 instead of 2<sup>3</sup> = 8."],
      "Backward in time, double once per half-life.",
      "%s &times; 8 = <b>%s</b>." % (a, S(D(a) * 8, 3, 'mCi')), 3, 1)

    t = '19.0'; n = 5
    Q(T, "Radon-222 (half-life 3.8 days) from soil enters a sealed jar, and no more radon gets in. What percent of the radon-222 is left after %s days?" % t,
      [PC(n), PC(n - 1), PC(n - 2), '96.875%'],
      ["n = %s &divide; 3.8 = 5; (1/2)<sup>5</sup> = 1/32." % t,
       "This is 4 half-lives; n = 5.",
       "This is 3 half-lives; 19.0 days is five 3.8-day half-lives.",
       "This is the percent that has <i>decayed</i>, not the percent left."],
      "n = time &divide; half-life; then halve n times from 100%.",
      "n = 5: 100 &rarr; 50 &rarr; 25 &rarr; 12.5 &rarr; 6.25 &rarr; <b>3.125%</b>.", 2, 1)

    Q(T, "A sample of technetium-99m is cooled in a freezer. What happens to its half-life?",
      ["Nothing; it stays 6.0 h, because half-life does not depend on temperature",
       "It gets longer, because nuclei decay more slowly when cold", "It gets shorter, because cold makes the nucleus unstable",
       "It changes only if the technetium is in a different compound"],
      ["Nuclear decay is not affected by temperature, by the amount, or by what compound the atom is in.",
       "Cooling slows chemical reactions, but not nuclear decay.",
       "Temperature does not change nuclear stability.",
       "Chemical bonds involve electrons; the nucleus decays the same in any compound."],
      "Half-life is a property of the nucleus.",
      "<b>No change</b>: still 6.0 h.", 1)

    Q(T, "Iodine-123 (half-life 13 h; electron capture with gamma rays) and iodine-131 (half-life 8.0 days; beta and gamma) both collect in the thyroid. Which is better for <b>imaging</b> the thyroid, and why?",
      ["Iodine-123: its gamma rays make the image, it gives off no beta particles, and its half-life is shorter",
       "Iodine-131: its beta particles make a sharper image", "Iodine-131: its longer half-life lowers the patient's dose",
       "Either one; the half-life does not matter for imaging"],
      ["Imaging needs radiation that leaves the body (gamma) and a short half-life; iodine-131's beta particles add dose without helping the image, which is why it is used for treatment.",
       "Beta particles stay in the body; they do not reach the camera.",
       "A longer half-life keeps the patient radioactive longer, which raises the dose.",
       "A tracer's half-life should be long enough to image and short enough to be gone soon after."],
      "Imaging: gamma rays out of the body, short half-life.",
      "<b>Iodine-123</b> for imaging; iodine-131 for treatment.", 2)

    Q(T, "A student must find how much of 2.50 mg of sodium-24 (half-life 15.0 h) remains after 60.0 h. What is the correct first step?",
      ["Divide 60.0 h by 15.0 h to get n = 4 half-lives", "Raise 1/2 to the power 60.0",
       "Subtract 15.0 from 60.0 to get the time left", "Divide 2.50 mg by 60.0 h"],
      ["n = time &divide; half-life, with matching units; then 2.50 mg &times; (1/2)<sup>4</sup> = 0.156 mg.",
       "This uses the time as n; n is the number of half-lives, 60.0 &divide; 15.0 = 4.",
       "Subtracting times does not count half-lives.",
       "mg &divide; h is not an amount; the amount is halved once per half-life."],
      "Before you multiply anything, find n.",
      "First find <b>n = 60.0 h &divide; 15.0 h = 4</b>.", 1)

    # ======================= ch14-dating (6) =======================
    T = 'ch14-dating'
    lv, sm = '13.6', '1.70'; n = 3
    Q(T, "A wooden post from an ancient village gives %s decays per minute per gram of carbon. Fresh wood from a living tree gives %s. About how many years ago was the tree cut down? (carbon-14 half-life 5730 years)" % (sm, lv),
      [AGE(n), AGE(8), S(D(5730) / 8, 3, 'years'), AGE(n + 1)],
      ["%s &rarr; 6.80 &rarr; 3.40 &rarr; %s is 3 half-lives; 3 &times; 5730 years = 17,190 years, three significant figures." % (lv, sm),
       "This uses 8 (from the fraction 1/8) as n; 1/8 = (1/2)<sup>3</sup>.",
       "This multiplies the fraction 1/8 by 5730; multiply n instead.",
       "This counts the four activities; there are three halvings."],
      "Turn the two activities into a number of halvings.",
      "n = 3: <b>%s</b>." % AGE(n), 2, 1)

    n = 7
    Q(T, "Charcoal from a cave painting has 1/128 of the carbon-14 per gram of carbon found in living wood. Estimate its age. (carbon-14 half-life 5730 years)",
      [AGE(n), AGE(n + 1), S(D(5730) * 128, 3, 'years'), S(D(5730) / 128, 3, 'years')],
      ["1/128 = (1/2)<sup>7</sup>: 7 &times; 5730 = 40,110 years, three significant figures. This is near the method's limit of about 50,000 years.",
       "This counts 8 half-lives; 2<sup>7</sup> = 128.",
       "This multiplies 5730 by 128; multiply by n = 7.",
       "This multiplies the fraction by 5730."],
      "How many times must you halve 1 to reach 1/128?",
      "n = 7: <b>%s</b>." % AGE(n), 3, 1)

    Q(T, "An archaeologist finds a clay pot with charred food stuck to the inside. What can radiocarbon dating measure?",
      ["The age of the charred food, which came from once-living plants or animals",
       "The age of the clay, because clay contains carbon-14 from the ground",
       "Nothing, because cooking destroys all carbon-14", "The age of the clay and the food, which must be the same"],
      ["The food residue was once alive, so its carbon-14 clock started when it died; the clay is a mineral, not once-living.",
       "Clay was never alive; it has no carbon-14 clock.",
       "Cooking is a chemical change; it does not change nuclei, so the carbon-14 is still there.",
       "Only the once-living food can be dated; the pot's clay is far older and was never alive."],
      "Which part was once alive?",
      "<b>The charred food</b>.", 2)

    Q(T, "Why do radiocarbon labs calibrate their ages with tree rings?",
      ["The carbon-14 level in the air has varied over thousands of years, and tree rings record known years.",
       "Tree rings show how fast carbon-14 decays in wood.", "Carbon-14 decays faster in wood than in bone.",
       "Tree rings are the only material that contains carbon-14."],
      ["Each ring can be counted to a known year, so measuring its carbon-14 shows how the starting ratio has changed; fossil fuel burning and bomb tests also changed it.",
       "The half-life is the same in every material: 5730 years.",
       "Half-life does not depend on the material.",
       "All once-living material contains carbon-14."],
      "Was the starting ratio perfectly constant?",
      "<b>The air's carbon-14 level has varied</b>; counted tree rings correct for it.", 3)

    Q(T, "A meteorite is thought to be about as old as Earth, about 4.5 billion years. Which isotope is most useful for dating it?",
      ["Uranium-238 (half-life 4.5 &times; 10<sup>9</sup> years)", "Carbon-14 (half-life 5730 years)",
       "Hydrogen-3 (half-life 12.3 years)", "Cobalt-60 (half-life 5.27 years)"],
      ["Its half-life is about the same as the age being measured; it decays (through several steps) to lead-206.",
       "Carbon-14 works only to about 50,000 years and only for once-living things.",
       "Tritium would have decayed away within a few centuries.",
       "Cobalt-60 would be gone in less than a century."],
      "Match the half-life to the age.",
      "<b>Uranium-238</b>.", 2)

    Q(T, "Archaeologists want to know whether a bone is about 1500 years old or about 3000 years old. What would they expect for its carbon-14 compared with living bone?",
      ["Less than living bone, and less still if it is the older age", "More than living bone, because carbon-14 builds up after death",
       "The same as living bone, because the bone's carbon was fixed at death", "None at all, because carbon-14 is gone within a few centuries"],
      ["Both ages are less than one half-life (5730 years), so more than half the carbon-14 is left, and the older bone has less.",
       "Carbon-14 only decays after death; nothing adds more.",
       "At death the carbon stops being <i>replaced</i>, but the carbon-14 keeps decaying.",
       "After 5730 years half is still left; it takes many half-lives to become unmeasurable."],
      "After death, carbon-14 decays and is not replaced.",
      "<b>Less than living bone, and less for the older age</b>.", 2)

    # ======================= ch14-fission (4) =======================
    T = 'ch14-fission'
    Q(T, "Cesium-140 is one of many possible fragments when uranium-235 splits. What is the other fragment? [[n]] + [[U-235]] -> [[Cs-140]] + ? + 3 [[n]]",
      ["[[Rb-93]] (rubidium-93)", "[[Rb-95]] (rubidium-95)", "[[Rb-92]] (rubidium-92)", "[[Kr-93]] (krypton-93)"],
      ["Left: A = 236, Z = 92. Right so far: A = 140 + 3 = 143, Z = 55. Missing: A = 93, Z = 37, rubidium.",
       "This counts the 3 neutrons as 1; they add 3 to the mass numbers.",
       "This forgets the neutron on the left; the left total is 236, not 235.",
       "Z: 92 &minus; 55 = 37, rubidium, not 36."],
      "Left total 236; count all 3 neutrons.",
      "A: 236 &minus; 140 &minus; 3 = 93. Z: 37: <b>[[Rb-93]]</b>.", 3)

    Q(T, "In most nuclear reactors, water flows through the core. What two jobs does the water do?",
      ["It slows the neutrons so uranium-235 can capture them, and it carries the heat away.",
       "It absorbs all the neutrons to stop the chain reaction, and it shields the turbine.",
       "It is the fuel that splits, and it makes the steam.",
       "It cools the control rods so they can give off more neutrons."],
      ["The water is the moderator (slows neutrons) and the coolant (carries heat to the steam generator).",
       "Absorbing neutrons is the job of the control rods.",
       "Uranium-235 in the fuel rods is what splits.",
       "Control rods absorb neutrons; they do not give them off."],
      "Moderator and coolant.",
      "<b>Moderator and coolant</b>: slows neutrons, carries heat.", 2)

    Q(T, "Why can a nuclear power reactor not explode like an atomic bomb?",
      ["Its fuel is only a few percent uranium-235, too little for a runaway chain reaction.",
       "Its fuel is plutonium, which cannot undergo fission.", "Its control rods are made of uranium-235.",
       "Reactors use fusion, which cannot run away."],
      ["Bomb material is highly enriched and slammed into a supercritical mass; reactor fuel's low enrichment cannot do this. (Serious accidents, such as Chernobyl, are still possible, but not a nuclear explosion.)",
       "Plutonium-239 can undergo fission; it was used in a 1945 bomb.",
       "Control rods are neutron absorbers such as boron or cadmium.",
       "Power reactors use fission; practical fusion power does not exist yet."],
      "Think about how much uranium-235 is in the fuel.",
      "<b>Low-enrichment fuel (a few percent uranium-235)</b>.", 3)

    Q(T, "Which statement correctly compares fission and fusion?",
      ["Fission splits a heavy nucleus; fusion joins light nuclei. Both turn a little mass into energy.",
       "Fission joins light nuclei; fusion splits a heavy nucleus.",
       "Fission releases energy; fusion absorbs energy.", "Fusion is used in today's nuclear power plants; fission powers the Sun."],
      ["Fission: uranium-235 or plutonium-239 split by a neutron. Fusion: hydrogen isotopes joined at very high temperature, as in the Sun.",
       "This swaps the two; fission sounds like &ldquo;fissure,&rdquo; a crack.",
       "Both release energy; per gram of fuel, fusion releases even more.",
       "This swaps them: power plants use fission, and the Sun uses fusion."],
      "Fission = split; fusion = fuse.",
      "<b>Fission splits heavy nuclei; fusion joins light ones; both release energy</b>.", 1)

    # ======================= ch14-medicine (5) =======================
    T = 'ch14-medicine'
    r, d1, d2 = '64', '0.50', '2.0'; v = D(r) * (D(d1) / D(d2)) ** 2
    Q(T, "The dose rate 0.50 m from a sealed gamma source is %s &mu;Sv/h. What is the dose rate 2.0 m away?" % r,
      [S(v, 2, '&mu;Sv/h'), S(D(r) / 4, 2, '&mu;Sv/h'), S(D(r) / 2, 2, '&mu;Sv/h'), S(D(r) / 64, 2, '&mu;Sv/h')],
      ["2.0 m is 4 times as far; (1/4)<sup>2</sup> = 1/16: %s &divide; 16." % r,
       "This divides by 4; the dose rate falls with the square of the distance.",
       "This halves it; four times the distance cuts the dose rate to 1/16.",
       "This divides by 4<sup>3</sup> = 64; the law uses the square, 4<sup>2</sup> = 16."],
      "How many times farther is 2.0 m than 0.50 m? Square that.",
      "%s &times; (0.50/2.0)<sup>2</sup> = <b>%s</b>." % (r, S(v, 2, '&mu;Sv/h')), 2, 1)

    Q(T, "A nurse caring for a patient after radioactive iodine therapy cuts her time at the bedside from 20 minutes to 10 minutes, at the same distance. How does her dose change?",
      ["It is cut in half", "It is cut to one-fourth", "It does not change", "It doubles"],
      ["Dose = dose rate &times; time, so half the time gives half the dose. (Context only; care follows facility policy.)",
       "One-fourth comes from doubling the <i>distance</i> (inverse-square law), not halving the time.",
       "The dose depends on how long she is exposed.",
       "Less time means less dose."],
      "Dose = dose rate &times; time.",
      "Half the time: <b>half the dose</b>.", 2)

    Q(T, "Patients fast for several hours before an FDG PET scan. Why?",
      ["So that glucose in the blood does not compete with the FDG for uptake by cells",
       "So that the fluorine-18 decays faster", "So that the stomach does not block the gamma rays",
       "So that the FDG is not digested into fluoride"],
      ["FDG enters cells through the same glucose transporters as glucose; high blood glucose would crowd it out, weakening the image.",
       "Nothing the patient does changes the half-life (110 min).",
       "Gamma rays pass through the body; food does not block them.",
       "FDG is given by injection into a vein, not swallowed."],
      "FDG is a glucose look-alike.",
      "<b>Blood glucose would compete with FDG</b>.", 2)

    Q(T, "Some ground beef is treated with gamma rays to kill <i>E. coli</i> bacteria. How do the gamma rays kill the bacteria?",
      ["They break the bacteria's DNA, directly and through free radicals made from water.",
       "They make the bacteria radioactive, so the bacteria decay.", "They heat the meat until it is cooked.",
       "They change the carbon atoms in the bacteria into nitrogen."],
      ["A bacterium has one copy of its chromosome and limited repair, so enough DNA breaks stop it from dividing. The meat does not become radioactive.",
       "Gamma rays change no nuclei, so nothing becomes radioactive.",
       "The dose deposits far too little heat to cook food; the damage is to DNA.",
       "Gamma rays ionize molecules; they do not change one element into another."],
      "Radiation damages microbes the same way it damages human cells.",
      "<b>Broken DNA</b>, directly and through free radicals.", 2)

    Q(T, "In the 1920s, workers who painted glowing watch dials with radium paint often shaped their brushes with their lips. Why was this so harmful, even though radium's alpha particles cannot get through skin?",
      ["The swallowed radium settled in their bones, so its alpha particles hit living cells from the inside.",
       "Radium's alpha particles are the most penetrating radiation.", "The paint gave off X-rays from the radium nuclei.",
       "Radium is harmful only as a gas."],
      ["Inside the body, the highly ionizing alpha particles deliver all their energy to nearby living cells; radium is taken up in bone like calcium.",
       "Alpha particles are the least penetrating; the danger was being inside the body.",
       "X-rays come from machines, not nuclei; radium gives off alpha particles.",
       "Radium is a metal; it was harmful because it was swallowed."],
      "Alpha: highest ionizing power, lowest penetrating power.",
      "<b>Swallowed radium put alpha emitters inside the body</b>.", 2)


if __name__ == '__main__':
    build_hw()
    dump(sys.argv[1])
