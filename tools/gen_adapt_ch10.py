#!/usr/bin/env python3
"""Builds bank/ch10_adapt.json (Chapter 10 ADAPT homework-only items, text only; 42 items, none repeated from
bank/ch10.json).
usage: python3 tools/gen_adapt_ch10.py bank/ch10_adapt.json
Same conventions, helpers and markup as tools/gen_bank_ch10.py (imported from it): K = C + 273.15; 1 atm = 760 mmHg =
760 torr = 101.325 kPa = 14.7 psi; R = 0.082058 or 62.36; 22.4 L/mol only at STP; water vapor pressures given in the
stem; yellow-sheet molar masses. y[0] begins "Correct: ". Every item is rechecked by tools/check_bank_ch10.py."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bank_ch10 import *
import gen_bank_ch10 as G
G.CFG.update(prefix='c10-h%02d', adapt=True)


def build_hw():
    # ======================= ch10-kmt (5) =======================
    T = 'ch10-kmt'
    Q(T, "Which statement <b>contradicts</b> the kinetic molecular theory of an ideal gas?",
      ["Gas particles slow down a little every time they hit a wall, because the collisions lose energy.",
       "Gas particles move constantly and randomly in straight lines.",
       "The particles are tiny compared with the distances between them.",
       "The average kinetic energy of the particles is proportional to the Kelvin temperature."],
      ["KMT says collisions are elastic: no kinetic energy is lost overall, so a gas at constant temperature never 'runs down'.",
       "This is part of KMT: constant, random, straight-line motion between collisions.",
       "This is part of KMT: a gas is mostly empty space.",
       "This is part of KMT, and it is why kelvins are used in every gas law."],
      "Look for the statement about energy being lost.",
      "KMT collisions are elastic, so <b>particles losing energy at each wall collision</b> contradicts it.", 2)

    Q(T, "At the same temperature, which gas has the <b>lowest</b> average molecular speed?",
      ["{SO2} (64.06 g/mol)", "He (4.003 g/mol)", "{N2} (28.014 g/mol)", "{O2} (31.998 g/mol)"],
      ["All four have the same average kinetic energy, so the heaviest molecules move slowest.",
       "Helium is the lightest, so its atoms are the fastest.",
       "{N2} is lighter than {SO2}, so it moves faster.",
       "{O2} is lighter than {SO2}, so it moves faster."],
      "Same kinetic energy: the heaviest particles must move slowest.",
      "Heaviest is slowest: <b>{SO2}</b>.", 2)

    Q(T, "A nurse opens an alcohol swab, and a few seconds later the smell reaches a patient across the room. Which idea of kinetic molecular theory explains this?",
      ["Gas particles are in constant, random motion, so they spread out by diffusion.",
       "Gas particles attract the molecules in the air and are pulled along.",
       "Gas particles are larger than the spaces between them.",
       "Gas particles stop moving once they leave the swab."],
      ["The vapor molecules move constantly and randomly, so they mix through the air on their own.",
       "KMT treats gas particles as having no attractions.",
       "Gas particles are tiny compared with the spaces between them.",
       "Gas particles never stop moving; that motion is what carries the smell."],
      "How do gases mix without anyone stirring them?",
      "<b>Constant random motion</b> spreads the vapor by diffusion.", 1)

    Q(T, "Why does a real gas squeezed to a very high pressure take up more volume than the ideal gas law predicts?",
      ["The particles are crowded, so their own volume is no longer small compared with the space between them.",
       "The particles move faster at high pressure.",
       "The particles attract each other more strongly at high pressure, pushing them apart.",
       "The collisions become elastic only at high pressure."],
      ["The ideal model treats particles as taking up no room; crowded particles fill a real share of the container.",
       "At constant temperature the average speed does not change with pressure.",
       "Attractions pull particles together, which would make the volume smaller, not larger.",
       "KMT assumes elastic collisions at all pressures; that is not the reason for the difference."],
      "Which KMT assumption fails when the particles are packed closely?",
      "At high pressure <b>the particles' own volume matters</b>, so the real volume is larger than ideal.", 3)

    Q(T, "In the lungs, oxygen moves from the air in the alveoli into the blood without any pump. What moves it?",
      ["Diffusion: random molecular motion carries {O2} from where it is more concentrated to where it is less",
       "Gravity pulls the heavier {O2} molecules down into the blood",
       "The blood attracts {O2} molecules across the wall by suction",
       "{O2} molecules are pushed in only when the person exhales"],
      ["The alveolar air has a higher {O2} partial pressure than the blood, and random motion carries {O2} across the thin wall.",
       "Gravity is not the cause; diffusion works in every direction.",
       "There is no suction; the net movement comes from random motion and a difference in concentration.",
       "Diffusion happens continuously, during both breathing in and breathing out."],
      "Gases spread from high concentration to low concentration on their own.",
      "<b>Diffusion</b>, driven by random molecular motion.", 1)

    # ======================= ch10-pressure (6) =======================
    T = 'ch10-pressure'
    P = '2.85'; v = D(P) * ATM_MM
    Q(T, "A hyperbaric chamber for wound treatment runs at %s atm. What is this pressure in mmHg?" % P,
      [S(v, 3, 'mmHg'), S(D(P) / ATM_MM, 3, 'mmHg'), S(D(P) * KPA, 3, 'mmHg'), S(D(P) * PSI, 3, 'mmHg')],
      ["%s atm &times; (760 mmHg / 1 atm)." % P,
       "This divides by 760; going from atm to mmHg, multiply.",
       "This multiplies by 101.325, which gives kPa, not mmHg.",
       "This multiplies by 14.7, which gives psi, not mmHg."],
      "1 atm = 760 mmHg.",
      "%s &times; 760 = <b>%s</b>." % (P, S(v, 3, 'mmHg')), 2, 1)

    P = '34.5'; v = D(P) / PSI * KPA
    Q(T, "A car tire is inflated to %s psi. What is this pressure in kilopascals?" % P,
      [S(v, 3, 'kPa'), S(D(P) * PSI * KPA, 3, 'kPa'), S(D(P) / KPA * PSI, 3, 'kPa'), S(D(P) * KPA, 3, 'kPa')],
      ["Through atm: %s psi &times; (1 atm / 14.7 psi) &times; (101.325 kPa / 1 atm)." % P,
       "This multiplies by 14.7; the psi factor is flipped.",
       "This flips both factors.",
       "This multiplies psi by 101.325 as if the pressure were in atm."],
      "14.7 psi = 1 atm = 101.325 kPa.",
      "%s &times; 101.325 &divide; 14.7 = <b>%s</b>." % (P, S(v, 3, 'kPa')), 2, 1)

    P = '95.5'; v = D(P) / ATM_MM
    Q(T, "A patient's arterial oxygen pressure (PO<sub>2</sub>) is %s mmHg. What is this in atmospheres?" % P,
      [S(v, 3, 'atm'), S(D(P) * ATM_MM, 3, 'atm'), S(D(P) / KPA, 3, 'atm'), S(D(P) / PSI, 3, 'atm')],
      ["%s mmHg &times; (1 atm / 760 mmHg)." % P,
       "This multiplies by 760; the factor is flipped.",
       "This divides by 101.325 (kPa per atm); the pressure is in mmHg.",
       "This divides by 14.7 (psi per atm); the pressure is in mmHg."],
      "Divide mmHg by 760 to get atm.",
      "%s &divide; 760 = <b>%s</b>." % (P, S(v, 3, 'atm')), 2, 1)

    P = '78.5'; v = D(P) / KPA
    Q(T, "An airliner's cabin is pressurized to %s kPa during flight. What is this in atmospheres?" % P,
      [S(v, 3, 'atm'), S(D(P) * KPA, 3, 'atm'), S(D(P) / ATM_MM, 3, 'atm'), S(D(P) / 101325, 3, 'atm')],
      ["%s kPa &times; (1 atm / 101.325 kPa); a little over three-quarters of sea-level pressure." % P,
       "This multiplies by 101.325; the factor is flipped.",
       "This divides by 760, the number of mmHg in 1 atm.",
       "This divides by 101,325, the number of pascals (not kPa) in 1 atm."],
      "1 atm = 101.325 kPa.",
      "%s &divide; 101.325 = <b>%s</b>." % (P, S(v, 3, 'atm')), 2, 1)

    Q(T, "Which place has the <b>lowest</b> average air pressure?",
      ["Summit of Mount Whitney (14,505 ft)", "Huntington Lake (about 7,000 ft)", "Fresno (about 300 ft)", "Badwater Basin, Death Valley (282 ft below sea level)"],
      ["The highest place has the least air above it, so the lowest pressure.",
       "Huntington Lake is high, but Mount Whitney is about twice as high.",
       "Fresno is near sea level, with a pressure just under 1 atm.",
       "Below sea level there is more air overhead, so the pressure is slightly above 1 atm."],
      "Pressure comes from the weight of the air above you.",
      "Most altitude, least air above: <b>Mount Whitney</b>.", 1)

    Q(T, "A mercury barometer is carried from Fresno up to Huntington Lake. What happens to the height of the mercury column?",
      ["It gets shorter, because the air pressure pushing on the dish is lower.",
       "It gets taller, because there is less air pushing down on the column.",
       "It stays at 760 mm, because the mercury does not change.",
       "It gets taller, because the air is colder at altitude."],
      ["Lower air pressure supports a shorter column of mercury (about 590 mm at Huntington Lake).",
       "The column is pushed up by air pressure on the dish; less pressure gives a shorter column.",
       "760 mm is the sea-level height; the height follows the air pressure.",
       "The column height measures air pressure, which is lower at altitude."],
      "The column is held up by the air pushing on the dish.",
      "Lower pressure at altitude, <b>shorter column</b>.", 1)

    # ======================= ch10-laws (9) =======================
    T = 'ch10-laws'
    V1, P1, P2 = '1.35', '745', '1.12'; P1a = D(P1) / ATM_MM; v = D(V1) * P1a / D(P2); n = ns(V1, P1, P2)
    Q(T, "A gas occupies %s L at %s mmHg. What volume does it occupy at %s atm and the same temperature?" % (V1, P1, P2),
      [S(v, n, 'L'), S(D(V1) * D(P1) / D(P2), n, 'L'), S(D(V1) * D(P2) / P1a, n, 'L'), S(D(V1) * P1a, n, 'L')],
      ["Convert first: %s mmHg = %s atm; then V<sub>2</sub> = P<sub>1</sub>V<sub>1</sub>/P<sub>2</sub>." % (P1, num(P1a, 4)),
       "This mixes mmHg and atm in Boyle's law; both pressures must be in the same unit.",
       "This uses Boyle's law as a ratio; the pressure rose a little, so the volume must fall a little.",
       "This is P<sub>1</sub>V<sub>1</sub> (in atm&middot;L), not yet divided by P<sub>2</sub>."],
      "Same pressure units on both sides, then P<sub>1</sub>V<sub>1</sub> = P<sub>2</sub>V<sub>2</sub>.",
      "%s mmHg &divide; 760 = %s atm; V<sub>2</sub> = (%s)(%s) / %s = <b>%s</b>." % (P1, num(P1a, 4), num(P1a, 4), V1, P2, S(v, n, 'L')), 3, 1)

    V1, C1, C2 = '3.85', '20.5', '46.5'; v = D(V1) * TK(C2) / TK(C1); n = ns(V1, sfT(C1), sfT(C2))
    Q(T, "A %s L balloon at %s °C is left in the sun and warms to %s °C at constant pressure. What is its new volume?" % (V1, C1, C2),
      [S(v, n, 'L'), S(D(V1) * D(C2) / D(C1), n, 'L'), S(D(V1) * TK(C1) / TK(C2), n, 'L'), S(D(V1) * D(C2) / TK(C1), n, 'L')],
      ["Charles's law with kelvins: V<sub>2</sub> = V<sub>1</sub>T<sub>2</sub>/T<sub>1</sub>.",
       "This uses Celsius temperatures and more than doubles the volume. Use kelvins.",
       "This inverts the temperature ratio, so the balloon shrinks as it warms.",
       "This converts only T<sub>1</sub>; both temperatures must be in kelvins."],
      "Both temperatures to kelvins, then V<sub>1</sub>/T<sub>1</sub> = V<sub>2</sub>/T<sub>2</sub>.",
      "%s; %s. V<sub>2</sub> = %s &times; %s / %s = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), kt(C2, 'T<sub>2</sub>'), V1, TKs(C2), TKs(C1), S(v, n, 'L')), 2, 1)

    P1, C1, C2 = '138', '19.5', '41.5'; v = D(P1) * TK(C2) / TK(C1); n = ns(P1, sfT(C1), sfT(C2))
    Q(T, "A full oxygen cylinder is at %s atm at %s °C. It is left in a closed ambulance that warms to %s °C. What is the new pressure in the cylinder?" % (P1, C1, C2),
      [S(v, n, 'atm'), S(D(P1) * D(C2) / D(C1), n, 'atm'), S(D(P1) * TK(C1) / TK(C2), n, 'atm'), S(D(P1) * TK(C2) / D(C1), n, 'atm')],
      ["Gay-Lussac's law: P<sub>2</sub> = P<sub>1</sub>T<sub>2</sub>/T<sub>1</sub>, with kelvins.",
       "This uses Celsius temperatures, which more than doubles the pressure.",
       "This inverts the temperature ratio, so the pressure falls as the cylinder warms.",
       "This converts only T<sub>2</sub>; both temperatures must be in kelvins."],
      "Rigid cylinder: P and T (K) directly related.",
      "%s; %s. P<sub>2</sub> = %s &times; %s / %s = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), kt(C2, 'T<sub>2</sub>'), P1, TKs(C2), TKs(C1), S(v, n, 'atm')), 2, 1)

    P1, C1, P2 = '1.55', '22.5', '2.05'; v = TK(C1) * D(P2) / D(P1); n = ns(P1, P2, sfT(C1))
    Q(T, "A rigid tank of gas is at %s atm and %s °C. To what temperature, in kelvins, must it be heated for the pressure to reach %s atm?" % (P1, C1, P2),
      [S(v, n, 'K'), S(D(C1) * D(P2) / D(P1), n, 'K'), S(TK(C1) * D(P1) / D(P2), n, 'K'), S(v, n, '°C')],
      ["T<sub>2</sub> = T<sub>1</sub>P<sub>2</sub>/P<sub>1</sub>, with T<sub>1</sub> in kelvins.",
       "This uses the Celsius temperature in Gay-Lussac's law.",
       "This inverts the pressure ratio, so the temperature drops as the pressure rises.",
       "The calculation gives kelvins, not degrees Celsius."],
      "Convert %s °C to kelvins first." % C1,
      "%s. T<sub>2</sub> = %s &times; %s / %s = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), TKs(C1), P2, P1, S(v, n, 'K')), 2, 1)

    V1, n1, V2 = '4.65', '0.190', '6.20'; v = D(n1) * D(V2) / D(V1); n = ns(V1, n1, V2)
    Q(T, "A balloon holds %s mol of air at %s L. More air is blown in, at the same temperature and pressure, until the volume is %s L. How many moles of air does it hold now?" % (n1, V1, V2),
      [S(v, n, 'mol'), S(D(n1) * D(V1) / D(V2), n, 'mol'), S(D(n1) * D(V2) / D(V1) - D(n1), n, 'mol'), S(D(V2) / VM, n, 'mol')],
      ["Avogadro's law: n<sub>2</sub> = n<sub>1</sub>V<sub>2</sub>/V<sub>1</sub>.",
       "This inverts the volume ratio; a larger balloon holds more moles, not fewer.",
       "This is only the moles that were added; the question asks for the total now in the balloon.",
       "This uses 22.4 L/mol, which applies only at STP; the balloon's conditions are not given as STP."],
      "V and n are directly related at constant T and P.",
      "n<sub>2</sub> = %s mol &times; %s L / %s L = <b>%s</b>." % (n1, V2, V1, S(v, n, 'mol')), 2, 1)

    V1, P1, C1 = '186', '741', '25.5'; v = D(V1) * D(P1) / ATM_MM * D(273) / TK(C1); n = ns(V1, P1, sfT(C1), '273')
    Q(T, "A student collects %s mL of dry gas at %s mmHg and %s °C. What volume would it occupy at STP (273 K and 1 atm)?" % (V1, P1, C1),
      [S(v, n, 'mL'), S(D(V1) * D(P1) * D(273) / TK(C1), n, 'mL'), S(D(V1) * D(P1) / ATM_MM * TK(C1) / D(273), n, 'mL'), S(D(V1) * ATM_MM / D(P1) * D(273) / TK(C1), n, 'mL')],
      ["V<sub>2</sub> = V<sub>1</sub> &times; (P<sub>1</sub>/P<sub>2</sub>) &times; (T<sub>2</sub>/T<sub>1</sub>) with P<sub>2</sub> = 760 mmHg and T<sub>2</sub> = 273 K.",
       "This divides %s mmHg by 1 atm, mixing units; write the STP pressure as 760 mmHg." % P1,
       "This inverts the temperature ratio; cooling to 273 K shrinks the gas.",
       "This inverts the pressure ratio; raising the pressure to 760 mmHg shrinks the gas."],
      "STP pressure in mmHg is 760 mmHg; temperatures in kelvins.",
      "%s. V<sub>2</sub> = %s mL &times; (%s / 760) &times; (273 / %s) = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), V1, P1, TKs(C1), S(v, n, 'mL')), 3, 1)

    V1, P1, C1, V2, P2 = '2.20', '1.05', '17.5', '1.85', '1.42'
    v = TK(C1) * D(P2) * D(V2) / (D(P1) * D(V1)); n = ns(V1, P1, V2, P2, sfT(C1))
    Q(T, "A gas sample occupies %s L at %s atm and %s °C. It is changed to %s L at %s atm. What is its new temperature in kelvins?" % (V1, P1, C1, V2, P2),
      [S(v, n, 'K'), S(D(C1) * D(P2) * D(V2) / (D(P1) * D(V1)), n, 'K'), S(TK(C1) * D(P1) * D(V1) / (D(P2) * D(V2)), n, 'K'), S(TK(C1) * D(P2) / D(P1), n, 'K')],
      ["T<sub>2</sub> = T<sub>1</sub> &times; (P<sub>2</sub>V<sub>2</sub>)/(P<sub>1</sub>V<sub>1</sub>), with T<sub>1</sub> in kelvins.",
       "This uses the Celsius temperature in the combined gas law.",
       "This inverts the ratio; P<sub>2</sub>V<sub>2</sub> belongs on top when solving for T<sub>2</sub>.",
       "This ignores the volume change and uses only the pressures."],
      "Solve P<sub>1</sub>V<sub>1</sub>/T<sub>1</sub> = P<sub>2</sub>V<sub>2</sub>/T<sub>2</sub> for T<sub>2</sub>.",
      "%s. T<sub>2</sub> = %s K &times; (%s &times; %s) / (%s &times; %s) = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), TKs(C1), P2, V2, P1, V1, S(v, n, 'K')), 3, 1)

    Q(T, "The pressure on a gas is tripled at constant temperature and amount. What happens to its volume?",
      ["It becomes one-third as large.", "It becomes three times as large.", "It stays the same.", "It becomes nine times smaller."],
      ["Boyle's law: P and V are inverse, so tripling P divides V by 3.",
       "That would be a direct relationship; P and V are inverse.",
       "The volume must change when the pressure changes at constant temperature.",
       "Boyle's law is a simple inverse relationship (P<sub>1</sub>V<sub>1</sub> = P<sub>2</sub>V<sub>2</sub>), not an inverse square."],
      "P<sub>1</sub>V<sub>1</sub> = P<sub>2</sub>V<sub>2</sub>.",
      "Inverse: <b>one-third the volume</b>.", 1)

    Q(T, "A flight nurse notices that the air-filled cuff of a patient's breathing tube swells as the helicopter climbs, while the cabin temperature stays the same. Which gas law explains this?",
      ["Boyle's law: the outside pressure falls, so the trapped air's volume rises",
       "Charles's law: the air in the cuff warms and expands",
       "Gay-Lussac's law: the cuff's pressure rises with temperature",
       "Avogadro's law: more air molecules enter the cuff"],
      ["At constant temperature and amount, lower pressure means larger volume.",
       "The temperature is constant here, so Charles's law does not explain the change.",
       "Gay-Lussac's law needs a constant volume and a temperature change; here the volume changes at constant temperature.",
       "The cuff is sealed, so the amount of air does not change."],
      "Which variable changes as the helicopter climbs, and which stays constant?",
      "<b>Boyle's law</b>: lower pressure, larger volume. (Context only; crews follow their protocols.)", 2)

    # ======================= ch10-ideal (8) =======================
    T = 'ch10-ideal'
    nn, V, C = '0.645', '12.5', '24.5'; v = D(nn) * R * TK(C) / D(V); n = ns(nn, V, sfT(C))
    Q(T, "A %s L tank holds %s mol of oxygen at %s °C. What is the pressure in the tank?" % (V, nn, C),
      [S(v, n, 'atm'), S(D(nn) * R * D(C) / D(V), n, 'atm'), S(D(nn) * VM / D(V), n, 'atm'), S(D(nn) * R * TK(C), n, 'atm')],
      ["P = nRT/V, with T in kelvins.",
       "This uses the Celsius temperature.",
       "This uses 22.4 L/mol, which is for STP only.",
       "This is nRT, not yet divided by the volume."],
      "Solve PV = nRT for P.",
      "%s. P = (%s)(0.082058)(%s) / %s = <b>%s</b>." % (kt(C), nn, TKs(C), V, S(v, n, 'atm')), 2, 1)

    nn, C, P = '2.15e-3', '37.0', '0.985'; nv = D(nn); v = nv * R * TK(C) / D(P) * 1000; n = ns('2.15', P, sfT(C))
    Q(T, "A sample of exhaled air contains 2.15 &times; 10<sup>&minus;3</sup> mol of {CO2} at %s °C and %s atm. What volume, in mL, does the {CO2} alone occupy at these conditions?" % (C, P),
      [S(v, n, 'mL'), S(nv * R * D(C) / D(P) * 1000, n, 'mL'), S(v / 1000, n, 'mL'), S(nv * VM * 1000, n, 'mL')],
      ["V = nRT/P gives liters; &times; 1000 mL/L.",
       "This uses the Celsius temperature.",
       "This is the volume in liters labeled as mL; multiply by 1000.",
       "This uses 22.4 L/mol, but 37.0 °C is not STP."],
      "V = nRT/P in liters, then convert to mL.",
      "%s. V = (2.15 &times; 10<sup>&minus;3</sup>)(0.082058)(%s) / %s = %s L = <b>%s</b>." % (kt(C), TKs(C), P, num(v / 1000, 4), S(v, n, 'mL')), 2, 1)

    V, P, C = '2.75', '632', '26.5'; v = D(P) * D(V) / (R2 * TK(C)); n = ns(V, P, sfT(C), '62.36')
    Q(T, "A %s L flask contains neon at %s torr and %s °C. Using R = 62.36 L&middot;torr/(mol&middot;K), how many moles of neon are present?" % (V, P, C),
      [S(v, n, 'mol'), S(D(P) * D(V) / (R * TK(C)), n, 'mol'), S(D(P) * D(V) / (R2 * D(C)), n, 'mol'), S(D(P) / ATM_MM * D(V) / (R2 * TK(C)), n, 'mol')],
      ["n = PV/RT; with R = 62.36 the pressure stays in torr.",
       "This uses R = 0.082058 with the pressure in torr; that R needs atm.",
       "This uses the Celsius temperature.",
       "This converts torr to atm but then uses R = 62.36, which needs torr."],
      "Match the pressure unit to the R you use.",
      "%s. n = (%s)(%s) / [(62.36)(%s)] = <b>%s</b>." % (kt(C), P, V, TKs(C), S(v, n, 'mol')), 2, 1)

    V, nn, P = '6.50', '0.312', '1.27'; v = D(P) * D(V) / (D(nn) * R); n = ns(V, nn, P)
    Q(T, "A %s L steel tank holds %s mol of nitrogen at %s atm. What is the temperature in kelvins?" % (V, nn, P),
      [S(v, n, 'K'), S(D(nn) * R / (D(P) * D(V)), n, 'K'), S(D(P) * D(V) / (D(nn) * R2), n, 'K'), S(v, n, '°C')],
      ["T = PV/(nR).",
       "This is nR/(PV), the reciprocal.",
       "This uses R = 62.36, which needs torr; the pressure is in atm.",
       "PV/(nR) gives kelvins, not degrees Celsius."],
      "Solve PV = nRT for T.",
      "T = (%s)(%s) / [(%s)(0.082058)] = <b>%s</b>." % (P, V, nn, S(v, n, 'K')), 2, 1)

    V = '8.65'; v = D(V) / VM
    Q(T, "How many moles of nitrogen are in %s L of {N2} at STP?" % V,
      [S(v, 3, 'mol'), S(D(V) * VM, 3, 'mol'), S(VM / D(V), 3, 'mol'), S(D(V) / (R * D('298.15')), 3, 'mol')],
      ["At STP, 22.4 L = 1 mol: %s L &times; (1 mol / 22.4 L)." % V,
       "This multiplies by 22.4; set it up so liters cancel.",
       "This divides 22.4 by the volume; the factor is upside down.",
       "This uses 25 °C as standard temperature; STP is 0 °C (273 K)."],
      "At STP, 1 mol = 22.4 L.",
      "%s &divide; 22.4 = <b>%s</b>." % (V, S(v, 3, 'mol')), 1, 1)

    m, V, P, C = '0.635', '345', '0.968', '23.5'; nm = D(P) * D(V) / 1000 / (R * TK(C)); v = D(m) / nm; n = ns(m, V, P, sfT(C))
    Q(T, "A %s g sample of a gas occupies %s mL at %s atm and %s °C. What is its molar mass?" % (m, V, P, C),
      [S(v, n, 'g/mol'), S(D(m) / (D(P) * D(V) / (R * TK(C))), n, 'g/mol'), S(D(m) / (D(P) * D(V) / 1000 / (R * D(C))), n, 'g/mol'), S(nm / D(m), n, 'g/mol')],
      ["n = PV/RT with V = 0.%s L; M = m/n." % V,
       "This uses %s mL as liters, so n is 1000 times too large and M 1000 times too small." % V,
       "This uses the Celsius temperature.",
       "This divides moles by grams; molar mass is grams per mole."],
      "Get n from PV = nRT (liters, atm, K), then M = m/n.",
      "%s. n = (%s)(0.%s) / [(0.082058)(%s)] = %s mol; M = %s &divide; %s = <b>%s</b>." % (kt(C), P, V, TKs(C), num(nm, 4), m, num(nm, 4), S(v, n, 'g/mol')), 3, 1)

    Q(T, "At the same temperature and pressure, which gas has the greatest density?",
      ["{CO2} (44.009 g/mol)", "{N2} (28.014 g/mol)", "He (4.003 g/mol)", "{H2} (2.016 g/mol)"],
      ["At the same T and P, a liter of any gas holds the same number of moles, so the gas with the largest molar mass has the most grams per liter.",
       "{N2} is lighter per mole than {CO2}, so a liter of it has less mass.",
       "Helium is very light; that is why helium balloons float.",
       "{H2} has the smallest molar mass, so it is the least dense."],
      "Same T and P: same moles per liter. Then compare grams per mole.",
      "Same moles per liter, so the largest molar mass is densest: <b>{CO2}</b>.", 2)

    Q(T, "A student finds the moles of a gas with n = PV/RT, using R = 0.082058 L&middot;atm/(mol&middot;K) but leaving the pressure in mmHg. How does the answer compare with the correct one?",
      ["It is 760 times too large.", "It is 760 times too small.", "It is correct, because R works with any pressure unit.", "It is 101.325 times too large."],
      ["A pressure in mmHg is a number 760 times bigger than the same pressure in atm, and n is proportional to P.",
       "The mmHg number is larger than the atm number, so the answer comes out too large, not too small.",
       "The units of P must match the units in R.",
       "101.325 relates atm and kPa, not atm and mmHg."],
      "How many mmHg are in 1 atm?",
      "n &prop; P, and the mmHg number is 760 times the atm number: <b>760 times too large</b>.", 3)

    # ======================= ch10-stoich (7) =======================
    T = 'ch10-stoich'
    L = '2.65'; v = D(L) * 2
    Q(T, "In a hot engine, [[N2(g) + O2(g) -> 2 NO(g)]]. What volume of NO forms from %s L of {N2}, all gases at the same temperature and pressure?" % L,
      [S(v, 3, 'L'), S(D(L) / 2, 3, 'L'), L + ' L', S(D(L) / VM * 2, 3, 'L')],
      ["Same T and P, so volumes follow coefficients: %s L {N2} &times; (2 L NO / 1 L {N2})." % L,
       "This flips the ratio.",
       "This assumes 1 : 1; one {N2} makes two NO.",
       "This finds the moles of NO (2.65 × 2 ÷ 22.4) and stops; that number is moles, not liters. With all gases at the same T and P, the volume ratio gives liters directly."],
      "Coefficients are volume ratios for gases at the same T and P.",
      "%s &times; 2 = <b>%s</b>." % (L, S(v, 3, 'L')), 1, 1)

    g = '4.15'; Mx = D(MS['Na']); nn = D(g) / Mx; v = nn / 2 * VM
    Q(T, "Sodium reacts with chlorine: [[2 Na(s) + Cl2(g) -> 2 NaCl(s)]]. What volume of {Cl2} at STP reacts with %s g of Na (%s g/mol)?" % (g, Mx),
      [S(v, 3, 'L'), S(nn * VM, 3, 'L'), S(nn * 2 * VM, 3, 'L'), S(D(g) / 2 * VM, 3, 'L')],
      ["g Na &rarr; mol &rarr; &times; (1 mol {Cl2} / 2 mol Na) &rarr; &times; 22.4 L/mol.",
       "This skips the mole ratio.",
       "This flips the mole ratio.",
       "This uses grams of Na as moles."],
      "g &rarr; mol &rarr; mole ratio &rarr; L at STP.",
      "%s &divide; %s = %s mol Na; &divide; 2 = %s mol {Cl2}; &times; 22.4 = <b>%s</b>." % (g, Mx, num(nn, 4), num(nn / 2, 4), S(v, 3, 'L')), 2, 1)

    g, P, C = '25.5', '0.995', '32.5'; Mx = mm('C6H12O6'); ng = D(g) / Mx; nc = ng * 2; v = nc * R * TK(C) / D(P); n = ns(g, P, sfT(C))
    Q(T, "In bread dough, yeast ferments glucose: [[C6H12O6(aq) -> 2 C2H5OH(aq) + 2 CO2(g)]]. What volume of {CO2} at %s atm and %s °C comes from %s g of glucose (%s g/mol)?" % (P, C, g, Mx),
      [S(v, n, 'L'), S(nc * VM, n, 'L'), S(ng * R * TK(C) / D(P), n, 'L'), S(nc * R * D(C) / D(P), n, 'L')],
      ["g &rarr; mol &rarr; &times; 2 &rarr; V = nRT/P.",
       "This uses 22.4 L/mol, but the gas is not at STP.",
       "This skips the 1 : 2 mole ratio.",
       "This uses the Celsius temperature."],
      "Mole ratio, then V = nRT/P.",
      "%s &divide; %s = %s mol; &times; 2 = %s mol {CO2}. %s. V = <b>%s</b>." % (g, Mx, num(ng, 4), num(nc, 4), kt(C), S(v, n, 'L')), 3, 1)

    L, P, C = '1.45', '0.978', '24.5'; Mx = mm('H2O2'); no = D(P) * D(L) / (R * TK(C)); v = no * 2 * Mx; n = ns(L, P, sfT(C))
    Q(T, "Hydrogen peroxide decomposes on a wound: [[2 H2O2(aq) -> 2 H2O(l) + O2(g)]]. What mass of {H2O2} (%s g/mol) must decompose to give %s L of {O2} at %s atm and %s °C?" % (Mx, L, P, C),
      [S(v, n, 'g'), S(no * Mx, n, 'g'), S(no / 2 * Mx, n, 'g'), S(D(L) / VM * 2 * Mx, n, 'g')],
      ["n {O2} = PV/RT; &times; 2 mol {H2O2} per mol {O2}; &times; %s g/mol." % Mx,
       "This skips the mole ratio.",
       "This flips the mole ratio.",
       "This uses 22.4 L/mol off STP."],
      "L &rarr; mol (PV = nRT) &rarr; mole ratio &rarr; g.",
      "%s. n {O2} = %s mol; &times; 2 = %s mol {H2O2}; &times; %s = <b>%s</b>." % (kt(C), num(no, 4), num(no * 2, 4), Mx, S(v, n, 'g')), 3, 1)

    L, P, C = '2.85', '1.05', '21.5'; nmeth = D(L) / VM; no = nmeth * 2; v = no * R * TK(C) / D(P); n = ns(L, P, sfT(C))
    Q(T, "Methane burns: [[CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(g)]]. A %s L sample of {CH4}, measured at STP, burns completely. What volume of {O2}, measured at %s atm and %s °C, is used?" % (L, P, C),
      [S(v, n, 'L'), S(D(L) * 2, n, 'L'), S(nmeth * R * TK(C) / D(P), n, 'L'), S(no * R * D(C) / D(P), n, 'L')],
      ["L {CH4} &divide; 22.4 (STP) &rarr; &times; 2 &rarr; V = nRT/P at the new conditions.",
       "This uses the 1 : 2 volume ratio, but the two gases are measured at different conditions, so convert through moles.",
       "This skips the mole ratio.",
       "This uses the Celsius temperature."],
      "Different conditions for the two gases: go through moles.",
      "%s &divide; 22.4 = %s mol {CH4}; &times; 2 = %s mol {O2}. %s. V = <b>%s</b>." % (L, num(nmeth, 4), num(no, 4), kt(C), S(v, n, 'L')), 3, 1)

    Q(T, "For [[2 H2(g) + O2(g) -> 2 H2O(g)]] with all substances as gases at the same temperature and pressure, which statement is true?",
      ["2 L of {H2} react with 1 L of {O2} to make 2 L of water vapor.",
       "2 g of {H2} react with 1 g of {O2}.",
       "3 L of gas react to make 3 L of gas.",
       "1 L of {H2} reacts with 2 L of {O2}."],
      ["At the same T and P, coefficients are volume ratios, so 3 L of reactant gases make 2 L of product gas.",
       "Coefficients are mole (and, for gases, volume) ratios, not mass ratios.",
       "The total volume is not conserved: 2 + 1 = 3 L of reactants make only 2 L of water vapor.",
       "This reverses the coefficients of {H2} and {O2}."],
      "Read the coefficients as liters.",
      "<b>2 L {H2} + 1 L {O2} &rarr; 2 L {H2O}(g)</b>.", 2)

    g = '14.2'; Mx = mm('KO2'); nk = D(g) / Mx; v = nk * 3 / 4 * VM
    Q(T, "A rebreather uses potassium superoxide to make oxygen: [[4 KO2(s) + 2 CO2(g) -> 2 K2CO3(s) + 3 O2(g)]]. What volume of {O2} at STP forms from %s g of {KO2} (%s g/mol)?" % (g, Mx),
      [S(v, 3, 'L'), S(nk * VM, 3, 'L'), S(nk * 4 / 3 * VM, 3, 'L'), S(D(g) * 3 / 4 * VM, 3, 'L')],
      ["g &rarr; mol {KO2} &rarr; &times; 3/4 &rarr; &times; 22.4 L/mol.",
       "This skips the mole ratio.",
       "This flips the mole ratio (4/3 instead of 3/4).",
       "This uses grams of {KO2} as moles."],
      "g &rarr; mol &rarr; mole ratio &rarr; L at STP.",
      "%s &divide; %s = %s mol; &times; 3/4 = %s mol {O2}; &times; 22.4 = <b>%s</b>." % (g, Mx, num(nk, 4), num(nk * 3 / 4, 4), S(v, 3, 'L')), 2, 1)

    # ======================= ch10-dalton (7) =======================
    T = 'ch10-dalton'
    a, b, c, w = '569', '116', '28.5', '47.1'; v = addp(a, b, c, w)
    Q(T, "Exhaled air contains {N2} at %s mmHg, {O2} at %s mmHg, {CO2} at %s mmHg, and water vapor at %s mmHg. What is the total pressure?" % (a, b, c, w),
      [v + ' mmHg', addp(a, b, c) + ' mmHg', num((D(a) + D(b) + D(c) + D(w)) / 4, 3) + ' mmHg', format(D(a) + D(b) + D(c) + D(w), 'f') + ' mmHg'],
      ["Dalton's law: add all four partial pressures, rounded to the ones place like %s and %s." % (a, b),
       "This leaves out the water vapor; it is one of the gases in the mixture.",
       "This averages the partial pressures; the total is their sum.",
       "This is the sum, but it keeps a decimal place that %s mmHg and %s mmHg do not have." % (a, b)],
      "Add every partial pressure.",
      "%s + %s + %s + %s = <b>%s mmHg</b>." % (a, b, c, w, v), 1, 1)

    pc, Pt = '32.0', '2.45'; v = D(pc) / 100 * D(Pt); n = ns(pc, Pt)
    Q(T, "A diver's nitrox mixture is %s%% {O2} by moles. At a depth where the total pressure is %s atm, what is the partial pressure of {O2}?" % (pc, Pt),
      [S(v, n, 'atm'), S(D(pc) * D(Pt), n, 'atm'), S(D(Pt) / (D(pc) / 100), n, 'atm'), S((1 - D(pc) / 100) * D(Pt), n, 'atm')],
      ["X = 0.320; P<sub>O2</sub> = 0.320 &times; %s atm." % Pt,
       "This uses the percent without dividing by 100.",
       "This divides by the mole fraction.",
       "This is the partial pressure of the nitrogen (1 &minus; 0.320 = 0.680)."],
      "Percent &divide; 100 = mole fraction; P<sub>i</sub> = X<sub>i</sub>P<sub>total</sub>.",
      "0.320 &times; %s = <b>%s</b>." % (Pt, S(v, n, 'atm')), 2, 1)

    ar, ne, Pt = '0.275', '0.0850', '1.45'; tot = addp(ar, ne); v = D(ne) / D(tot) * D(Pt); n = ns(ne, tot, Pt)
    Q(T, "A lighting tube contains %s mol of argon and %s mol of neon at a total pressure of %s atm. What is the partial pressure of neon?" % (ar, ne, Pt),
      [S(v, n, 'atm'), S(D(ne) / D(ar) * D(Pt), n, 'atm'), S(D(ar) / D(tot) * D(Pt), n, 'atm'), S(D(ne) * D(Pt), n, 'atm')],
      ["X<sub>Ne</sub> = %s / %s; P<sub>Ne</sub> = X<sub>Ne</sub> &times; %s atm." % (ne, tot, Pt),
       "This divides by the moles of argon only; use the total moles.",
       "This is the partial pressure of argon.",
       "This multiplies the moles by the pressure; use the mole fraction."],
      "Total moles first.",
      "n<sub>total</sub> = %s; X<sub>Ne</sub> = %s; P<sub>Ne</sub> = <b>%s</b>." % (tot, num(D(ne) / D(tot), 4), S(v, n, 'atm')), 2, 1)

    Pa = '744'; v = addp(Pa, '-' + VP['37.0'])
    Q(T, "Water's vapor pressure is %s mmHg at 30.0 °C and %s mmHg at 37.0 °C. A gas is collected over water at 37.0 °C when the barometer reads %s mmHg. What is the pressure of the dry gas?" % (VP['30.0'], VP['37.0'], Pa),
      [v + ' mmHg', addp(Pa, '-' + VP['30.0']) + ' mmHg', addp(Pa, VP['37.0']) + ' mmHg', Pa + ' mmHg'],
      ["P<sub>gas</sub> = %s &minus; %s, to the ones place." % (Pa, VP['37.0']),
       "This uses the vapor pressure at 30.0 °C; the water is at 37.0 °C.",
       "This adds the water vapor; subtract it.",
       "This forgets the water vapor in the tube."],
      "Use the vapor pressure at the water's temperature and subtract.",
      "%s &minus; %s = <b>%s mmHg</b>." % (Pa, VP['37.0'], v), 2, 1)

    V, C, Pa = '62.5', '30.0', '765'; pw = VP[C]; Po = D(Pa) - D(pw); Ps = addp(Pa, '-' + pw)
    v = Po / ATM_MM * D(V) / 1000 / (R * TK(C)); n = ns(V, Ps, sfT(C))
    Q(T, "Zinc reacts with acid, [[Zn(s) + 2 HCl(aq) -> ZnCl2(aq) + H2(g)]], and %s mL of {H2} is collected over water at %s °C. The barometer reads %s mmHg, and water's vapor pressure at %s °C is %s mmHg. How many moles of {H2} were collected?" % (V, C, Pa, C, pw),
      [S(v, n, 'mol'), S(D(Pa) / ATM_MM * D(V) / 1000 / (R * TK(C)), n, 'mol'), S(Po / ATM_MM * D(V) / (R * TK(C)), n, 'mol'), S(Po * D(V) / 1000 / (R * TK(C)), n, 'mol')],
      ["P<sub>H2</sub> = %s &minus; %s = %s mmHg = %s atm; V = 0.0%s L; n = PV/RT." % (Pa, pw, Ps, num(D(Ps) / ATM_MM, 4), V.replace('.', '')),
       "This forgets to subtract the water vapor.",
       "This uses mL as liters.",
       "This uses mmHg with R = 0.082058."],
      "Dry-gas pressure first, then units that match R.",
      "P<sub>H2</sub> = %s mmHg = %s atm; %s. n = <b>%s</b>." % (Ps, num(D(Ps) / ATM_MM, 4), kt(C), S(v, n, 'mol')), 3, 1)

    Q(T, "A mixture of nitrogen and oxygen at one temperature contains three times as many moles of {N2} as of {O2}. How do their partial pressures compare?",
      ["The partial pressure of {N2} is three times that of {O2}.", "The partial pressures are equal, because both gases are at the same temperature.",
       "The partial pressure of {O2} is three times that of {N2}.", "The partial pressure of {N2} is larger, but by a factor that depends on molar mass."],
      ["Each gas's share of the pressure equals its share of the moles.",
       "Same temperature means same average kinetic energy per particle, but three times the particles make three times the hits.",
       "This reverses the two gases; more moles means more pressure.",
       "Partial pressure depends only on moles (at fixed V and T), not on molar mass."],
      "P<sub>i</sub> = X<sub>i</sub>P<sub>total</sub>.",
      "Three times the moles, <b>three times the partial pressure</b>.", 2)

    X_, Pt = '0.715', '3.60'; xo = 1 - D(X_); v = xo * D(Pt); n = ns(X_, Pt)
    Q(T, "A tank contains only {N2} and {O2} at a total pressure of %s atm. The mole fraction of {N2} is %s. What is the partial pressure of {O2}?" % (Pt, X_),
      [S(v, n, 'atm'), S(D(X_) * D(Pt), n, 'atm'), qd(xo, 3) + ' atm', addp(Pt, '-' + X_) + ' atm'],
      ["X<sub>O2</sub> = 1 &minus; %s = %s; P<sub>O2</sub> = %s &times; %s atm." % (X_, qd(xo, 3), qd(xo, 3), Pt),
       "This is the partial pressure of {N2}.",
       "This is the mole fraction of {O2}; multiply it by the total pressure.",
       "This subtracts a mole fraction from a pressure; they are different quantities."],
      "Mole fractions add to 1.",
      "X<sub>O2</sub> = %s; %s &times; %s = <b>%s</b>." % (qd(xo, 3), qd(xo, 3), Pt, S(v, n, 'atm')), 3, 1)


if __name__ == '__main__':
    build_hw()
    dump(sys.argv[1])
