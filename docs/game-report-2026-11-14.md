# Game report: fragateiro against the sources, 14 November 2026

Built by the workbench (version 29) on 14 November 2026 at 10:59 UTC, from the concept table
(935 concepts), the history table (283 practices) and the activity proposals, against the game
at commit `1d66225` (main). 18 sources are behind the findings. Complete lists are in the
appendices; this part explains them and ranks what matters.

How the report is made, and what each status means: `docs/workbench-method.md`, section 8.
Every finding counts its **independent sources**; a finding with more sources is more certain.
The sources' titles are shortened here (Gaspar = *Os portos fluviais do Tejo*; Pedrosa = *A
Muleta e a Tartaranha*; Lisboa Medieval = *Territórios da Lisboa Medieval*).

## 1. Summary

| | In the game | Not in the game | Change since the report of 07:11 |
| --- | --- | --- | --- |
| Boats | 6 (+ the Rabelo, in development) | 104 | missing 123 → 104: spellings merged ("Barco Moliceiro" = Moliceiro) |
| Places | 37 (23 ports, 3 landmarks, 11 named on the maps) | 120 (46 missing on a map, 73 outside the maps, 1 only a sea mark) + 21 of unknown area | the river's own names (13) and 69 countries, seas and regions no longer counted as places |
| Sailing and boat concepts | 133 shown | 57 not shown, 37 out of scope | 7 more not shown (new concepts from the moliceiro sources) |
| Historical practices | 10 covered, 41 partly | 60 with no activity | 85 → 111 practices compared |
| Conflicts between sources | | 11 (10 real) | same |

**The five findings that matter most for the game's developers:**

1. **The river boats most named in the sources are missing.** The *barco d'água acima* (10
   sources), the *varino* (9), the *barca* (8), the *bote* (7), the *batel* (6) and the
   *bateira* (6) are each named by more sources than three of the game's boats (Canoa 4,
   Catraio 3, Moliceiro 3). The varino and the barco d'água acima were the Tagus' main cargo
   boats.
2. **The upper estuary and the river above Vila Franca are not on the maps.** Santarém (6
   sources), Chamusca, Azambuja, Porto do Sabugueiro (3 each), Valada, Muge and Almeirim (2 each)
   lie between the game's Tagus map and its Middle Tagus map. Inside the Tagus map, the
   Mouchões (6), Mar da Palha (4), the bar (Barra do Tejo, 4) and the Cais das Colunas (3) have
   no name.
3. **Water depth and current are the simulation's biggest gap.** Of the 57 concepts the game
   cannot show, 13 need tide or river current (sailing upstream, the flood tide, floods) and 11
   need water depth (silting, low water, grounding on sand).
4. **Cargo is the most requested game addition**: loading and weight would unlock 12 proposed
   activities and improve 21 (13 sources), ahead of a new map area (15 unlocked) and new boats
   (15 unlocked).
5. **The game covers the main river work well**: crossings between the banks, freight from
   the Ribatejo to Lisbon, supplying ships at anchor, the muleta's fishing and moliço gathering
   are all covered by existing activities.

---

## 2. Boats

### In the game

| Boat | Sources | Also written in the sources |
| --- | --- | --- |
| Fragata | 9 | |
| Muleta | 8 | |
| Falua | 8 | |
| Canoa | 4 | |
| Catraio | 3 | |
| Moliceiro | 3 | Barco Moliceiro |
| Rabelo (in development) | 1 | Barco Rabelo |

The Baleeiro, the Bac and the Pinasse are in the game but no source names them as boats (the
registry has no Azorean, Arcachon or Aveiro-coast sources).

### Missing, ranked by sources

| Boat | Sources | Named by | Note |
| --- | --- | --- | --- |
| Barco d'água acima | 10 | mediotejo, barcos do tejo, Lisboa Medieval, Barcos Tradicionais do Tejo, Freire, Embarcações do Rio Tejo, Gaspar, getLISBON, Museu da Paisagem, Cacilheiros no Rio Tejo | the generic name of the upriver cargo boats; "Barco de Riba-Tejo" (2 + 1) is probably the same boat |
| Varino | 9 | mediotejo, Freire, getLISBON, Embarcações do Rio Tejo, barcos do tejo, Cacilheiros, Barcos Tradicionais do Tejo, Portugal Marítimo, Gaspar | flat-bottomed cargo boat of the estuary and the lower river |
| Barca | 8 | getLISBON, Embarcações, barcos do tejo, Cacilheiros, Lisboa Medieval, Gaspar, o tejo, Pedrosa | a general word too: check which sources mean a type |
| Vapor (steamboat) | 7 | Freire, getLISBON, Cacilheiros, mediotejo, Museu da Paisagem, Barcos Tradicionais do Tejo, Gaspar | the competitor of sail from the 19th century; could appear as traffic |
| Bote | 7 | getLISBON, barcos do tejo, Cacilheiros, Barcos Tradicionais do Tejo, Pedrosa, Embarcações, Portugal Marítimo | "Bote de fragata" (4) and "Bote cacilheiro" (4) are listed apart |
| Batel | 6 | getLISBON, Pedrosa, Gaspar, barcos do tejo, Lisboa Medieval, Portugal Marítimo | the boat of the 1572 *Regimento dos Barqueiros* |
| Bateira | 6 | getLISBON, Embarcações, barcos do tejo, Pedrosa, Lisboa Medieval, Portugal Marítimo | the Avieiro fishermen's boat; see the conflict in section 6 |
| Saveiro | 4 | Freire, getLISBON, Pedrosa, Mar da Costa | |
| Bote cacilheiro, Canoa cacilheira | 4 each | getLISBON, Cacilheiros, Portugal Marítimo, … | the ferries before the steam *cacilheiros* |
| Bote de fragata | 4 | getLISBON, barcos do tejo, Cacilheiros, Barcos Tradicionais do Tejo | the fragata's own rowing boat (it towed the fragata when becalmed) |
| Avieiro, Ferry, Enviada | 3 each | | |

74 more boats are named by one source each and 16 by two (Appendix A). Many of those are boats
of other rivers and coasts (the Douro's Rabelo-family boats, the Lancha Poveira, the Maceira),
from the *Portugal Marítimo* catalogue.

**Names still split (to merge by hand or in the pack's `aliases.yaml`):** Barco de Riba-Tejo /
Barco de Riba Tejo; possibly Barco d'água acima / Barco de Riba-Tejo; Barino / Muleta (a source
writes "Muleta / Barino").

## 3. Places

### In the game

Ports named by the sources: Lisboa (11 sources), Abrantes (7), Tancos (6), Seixal (6), Vila Nova
da Barquinha (5), Constância (5), Barreiro, Setúbal (3 each), Praia do Ribatejo, Vila Franca de
Xira, Alcochete, Sesimbra, Almada, Montijo, Sacavém, Murtosa, Torreira, Cais do Bico (2 each), and
Castelo de Almourol, Alverca, Moita, Ílhavo, Trafaria. Landmarks: Ponte Marechal Carmona, Ponte 25
de Abril, Torre de Belém. Named on the maps but not ports: Ribeira, Belém (3 each), Costa da
Caparica, Rossio ao Sul do Tejo (2 each), Alhandra, Rio de Moinhos, Quinta da Cardiga, Alpriate,
Pardilhó, Monte, Cova do Vapor.

### Missing on a map the game already has (46)

| Place | Map | Sources | Note |
| --- | --- | --- | --- |
| Mouchões | Middle Tagus (6), Tagus (2) | Freire, Lisboa Medieval, getLISBON, Embarcações, Cacilheiros, Portugal Marítimo | the islands of the upper estuary, Avieiro fishing and freight; they lie between the two maps |
| Barra do Tejo | Tagus | mediotejo, Pedrosa, Embarcações, barcos do tejo | the bar: pilotage, the limit for river boats |
| Mar da Palha | Tagus | Freire, Embarcações, barcos do tejo, Cacilheiros | the inner estuary |
| Cais das Colunas | Tagus | getLISBON, Cacilheiros | the landing at Terreiro do Paço |
| Mar entre o Cabo da Roca e Setúbal | Tagus | Pedrosa, Embarcações, Portugal Marítimo | the muleta's sea fishing grounds ("Entre-Cabos") |
| Ribeira de Sacavém, Ponta do Montijo | Tagus | 2 each | |
| Museu de Marinha, Biblioteca da Sociedade de Geografia | Tagus | 2 each | institutions, not places to sail to |

**Noise:** "Porto de Lisboa" (6) and "Ribeira de Lisboa" are Lisbon's harbour, which the game
has as Lisboa; "Rio de Lisboa" and "Margem Direita do Tejo" (4) are the river itself. Workbench
version 30 merges them (the pack's `aliases.yaml`); the next build will not list them.

### Outside the game's maps (73)

- **Between the Tagus map and the Middle Tagus map** (the strongest case for a new map area):
  Santarém (6), Chamusca, Azambuja, Porto do Sabugueiro (3 each), Valada, Muge, Almeirim, Paço de
  Almeirim (2 each), Salvaterra de Magos, Benavente, Samora Correia, Vila Nova da Rainha, Cartaxo,
  Montalvo (1 each).
- **Above the Middle Tagus map:** the Zêzere (3), Portas do Ródão, Belver, Fratel, Erges, the
  Ocreza, Cachão do Cabril, Castelo de Bode, Tomar and the Nabão.
- **Far away** (trade and history, not places to sail to): Ceuta, Alcántara, Seville, Sanlúcar,
  Marseille, Messina, Chioggia, Pesaro, Arguim, Cabo Branco, Toledo, Aranjuez and others.

### Area unknown (21) and only a sea mark (1)

The 21 of unknown area are mostly small river ports of the medieval sources (Porto de Arraiolos,
Portos dos Frades, Porto da Cortiça, 3 sources each) whose location Claude could not place; a
historian could. **Cacilhas** (2 sources) is on the Tagus map only as a sea mark, though it was
the main ferry landing of the south bank: a candidate for a named place.

## 4. Sailing and the boat

**Shown by the simulation (133):** the points of sail, tacking, gybing, in irons, sheeting in
and easing, heading up and bearing away, leeway, heel, gusts, docking; and the boats' parts the
game models: shallow draught (8 sources), rudder (7), flat bottom (7), keel (6), half keel (5),
the leeboard, the gaff sail, the bastardo, the moliceiro's trapezoidal sail, the steering oar
(*esparrela*) and others.

**Not shown (57), grouped by what the game would need:**

| The game would need | Concepts | Examples (sources) |
| --- | --- | --- |
| Tide and river current | 13 | sailing upstream (3), floods and flood tides (3), tidal influence, current speed, using the flood tide to go upriver, the river's regime and rainfall, rapids |
| Water depth, silting, seasons | 11 | silting of the riverbed (6), low water in the dry season, navigability, sand and grounding, the silted reach between Almourol and Muge, the irregular bed below Tancos |
| Other rigs and hull shapes | 10 | the lateen sail (7, see below), rig type, gaff rig, lug rig, curved or straight bows, raked masts, raised ends, the gondolé hull, the *botalós* |
| Cargo, fishing gear, stability | 8 | the cargo hold with *paneiros*, false bulwarks (3 each), the *tartaranha* and *varredoura* nets, net mesh, fish holds, ballast, capsizing |
| Sail handling controls | 7 | reefing (2), lowering the sail (*amainar*, 2), setting the tack (*amurar*, 2), the yard (3), bare poles, the gybe warning |
| Towing, poling, bridges, locks | 5 | towpaths (*sirga*, 3), towing past rapids, the raised bow for poling, lowering the mast for bridges, locks |
| Decoration | 3 | the moliceiro's painted panels (*jornal da ria*), the builder's mark, polychrome painting |

**To check:** the lateen sail (7 sources) is reported "not shown", but the game's Muleta carries
lateen-like sails; the concept is not linked to the simulation in the concept table. Link it by
hand when the workbench allows it, or accept it as a classification error.

**Out of scope (37):** parts the visitor does not need (bow, stern, beam, quarter, the stern
store), and details of the moliceiro's construction.

## 5. Historical practices and the game's activities

**Covered (10):**

| Practice | Sources | Game activity |
| --- | --- | --- |
| River traffic linking the banks until the mid-20th century | 5 | Passengers |
| *Barcos d'água acima* carrying freight Ribatejo–Lisbon | 4 | route Vila Franca–Lisboa |
| Supplying ships at anchor in Lisbon | 4 | Supplies |
| The muleta's fishing grounds with the *tartaranha* | 3 | Fishing |
| Moliço gathering with moliceiros | 3 | Seaweed |
| Bote passenger service Cacilhas–Almada–Lisboa | 2 | route Lisboa–Almada |
| Keel boats carrying people and cargo from Cacilhas; the medieval Tagus as a busy river; Enviadas ferrying the catch; whaling in the Azores | 1 each | Moita–Lisboa route, Cargo, supply missions, whaling |

**Partly covered (41):** the game has the activity, but not the boat, the place, the cargo or
the way it was done. The differences that recur:
- *the cargo*: cork, lime, timber, wheat, wine, salt and fish are all carried as generic cargo
  on the routes to Lisbon;
- *the place*: Montijo (Aldeia Galega), the Mouchões, Santarém, the Rossio de Abrantes, Porto de
  Muge;
- *the boat*: cangueiros, bateiras, steamers, and boats of other coasts (Lancha Poveira,
  Maceira, Canoa da Picada);
- *the fishing method*: paying out and hauling the *tartaranha*, sardine picking, line fishing,
  beach launching.

The strongest: fragatas handling cargo in Lisbon harbour (2 sources; the Cargo mini-game has no
loading), muletas and rascas trading beyond the bar (2), the Avieiros fishing and living aboard
their bateiras (2), the boat service Lisbon–Montijo (Aldeia Galega, 2), cangueiros hauling heavy
cargo (2).

**No activity (60):** they fall into four groups.
- *Sailing work the game could add* (20): the crew of a barco d'água acima (arrais, camaradas,
  moços, 2 sources), the fragata rowed and towed when becalmed (2), the muleta rigged as an
  *iate* (2), *xávega* beach nets at Costa da Caparica (2), the royal boat journeys Almeirim–
  Lisbon (2), Santarém's medieval sea links (2), the muleta's coastal trade to the Algarve and
  Morocco, the tartaranha fishermen as bar pilots, furling the muleta's sail, *tapa-esteiros*
  fishing in the Mar da Palha, towing past the rapids at Cachão do Cabril, upriver crews poling
  and towing, rafting timber and cork, fuel barges to the Rossio quay, ore convoys from
  Alcántara, steam cargo at the Barquinha quay, car ferries.
- *Boatbuilding and decoration* (12): the moliceiro's construction, caulking, painting and
  festival dress (2 sources each for painting and caulking); the shipyards of Barreiro, Seixal
  and Trafaria. Not sailing, but material for a logbook or a museum panel.
- *Economy and society* (20): trade organisation at Abrantes, the railway company hiring
  boatmen and buying boats, brandy distilling to save freight, the boatmen leaving the upriver
  ports, ox-cart transport to the river ports, the royal household's fish, fishing settlements
  at Costa da Caparica.
- *Unrelated to the game* (8): Nile irrigation, the Almourol dam project, regulating the river
  by afforestation, Roman inland navigation, industry siting, the curative springs, right-bank
  forestry, the Ribatejo's agricultural conversion. These should be left out in the History tab
  so they stop appearing here.

## 6. Conflicts between sources

| Concept | Kind | What differs | Next step |
| --- | --- | --- | --- |
| Close-hauled; Beating to windward | number | 45–50° to the wind in the sailing course; about 36° for the game's Falua, 50° for the Rabelo | a design choice: the game's figure is per boat; say so in the lines |
| Square sail no-go angle | number | about 50° (Rabelo) against "braced to 35°" | ask a sailor of square-rigged boats |
| Downwind sail setting | number | sails at 90° to the wind (course) against the game's sheet stop of 20° | check the course; probably a different measure |
| Estuary navigation | number | traffic up to 20–30 km above Lisbon, or as far as the tide (Sabugueiro) | the historian |
| Batel passenger limit | number | 8 or 12 people in two paragraphs of the 1572 regulation | read the regulation: different routes? |
| Scheduled service (barco da carreira) | number | one boat a week, 2–4 barcas per route, 100 Abrantes boats in 1552 | probably different periods; the historian |
| Leeboard (*tábua de bolina*) | definition | a board lowered in shallow water, or a fixed lateral keel | ask a sailor; the game's muleta has one |
| Gust | definition | a stronger wind (method document), or also a change of direction (the game) | a design choice |
| Bateira | definition | a cargo boat, the Avieiros' fishing boat and home, or a small boat on the Lisbon run | different bateiras: split the concept |
| Leeward | — | "No conflict" recorded as a conflict | remove (noise) |

## 7. Game additions the proposed activities need

| Addition | Activities it would unlock | It would improve | Sources behind them | Examples |
| --- | --- | --- | --- | --- |
| Cargo loading and weight | 12 | 21 | 13 | Fair wind to Lisbon, Supply run to the anchored ship, Docking at Cais das Colunas, Fish to the Ribeira |
| New map area | 15 | 4 | 8 | Fair wind to Lisbon (Ribatejo), Upriver with salt and cloth, Hauled past the rapids |
| New boat | 15 | 2 | 10 | Quay of the steam cargo boats, Net boat in the Mar da Palha, Avieiro day on the river |
| Crew and tasks aboard | 8 | 6 | 11 | The arrais at the helm, Becalmed fragata, Shorten sail |
| Fishing net and catch | 7 | 4 | 4 | Entre-Cabos fishing run, Haul the net broadside |
| Water depth and shallows | 6 | 4 | 9 | Pilot across the bar, Poling upriver, Shallow lagoon boat, Moliço run |
| Tide and current | 4 | 9 | 10 | Back upriver with the wind, Small catraio crossing, Last sail upriver |
| Towing | 4 | 1 | 6 | Becalmed fragata, Ore convoy through the rapids |
| Steam and motor traffic | 2 | 2 | 3 | Sailing upstream after the steamer, Ferry crossing with cargo |
| Rowing and poling | 2 | 2 | 6 | Cross and carry, Poling upriver |
| Rig changes | 2 | 1 | 2 | Change the rig, Shorten sail |
| River bar and pilotage | 1 | 2 | 3 | Pilot across the bar, Over the bar |

**Anachronisms:** none reported, because no narrative has a period set. Once a period is set
(for example the 1920s), the report lists the landmarks built later (Ponte 25 de Abril, Cristo
Rei…) for a historical edition to hide.

## 8. Recommendations for the game's developers, in order

1. **Add the Varino and the barco d'água acima** (10 and 9 sources), the river's cargo boats; the
   Bote and the Batel next (7 and 6).
2. **Fill the gap between the two Tagus maps** (Vila Franca to Constância: Santarém, Valada,
   Muge, the Mouchões), or extend the Tagus map upriver to the Mouchões.
3. **Name the Mar da Palha, the bar, the Cais das Colunas and Cacilhas** on the Tagus map.
4. **Cargo loading and weight** (12 activities unlocked, 21 improved).
5. **A current and water depth**, starting with a simple ebb and flood on the estuary map (13 +
   11 concepts; 13 activities unlocked or improved by tide and current, 10 by depth).
6. **Sail handling**: reefing and lowering the sail (2 sources each).

Issue drafts for each of these, with the evidence, are in the workbench's Game report tab
("Issue drafts", threshold 2 sources).

## 9. Quality of this report, and what to do next

- **Still to run in the workbench:** the check against the game for the last 44 concepts (they
  have no scope or simulation link yet) and **Write summary** (the summary dates from 12
  November).
- **Noise to clean:** Lisbon's harbour names and the river's banks (fixed in workbench version
  30, for the next build); Mouchões placed in two areas; "Barco de
  Riba-Tejo" spelt two ways; 17 practices unrelated to the game (leave them out in History);
  "Leeward: No conflict".
- **Sources:** the Baleeiro, the Bac and the Pinasse have no source; Azorean, Arcachon and
  Aveiro-coast sources would let the report evaluate those areas too.

---


## Appendix A. Boats named in the sources and not in the game (all)

| Boat | Sources | Which | Also written |
| --- | --- | --- | --- |
| Barco d'água acima | 10 | Barcos Tradicionais do Tejo e a Sua Co, Cacilheiros no Rio Tejo, Embarcações do Rio Tejo, Freire, Gaspar, Museu da Paisagem, Territorios da Lisboa Medieval 3 225, barcos do tejo, getLISBON, mediotejo | Barco de água acima |
| Varino | 9 | Barcos Tradicionais do Tejo e a Sua Co, Cacilheiros no Rio Tejo, Embarcações do Rio Tejo, Freire, Gaspar, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS, barcos do tejo, getLISBON, mediotejo |  |
| Barca | 8 | Cacilheiros no Rio Tejo, Embarcações do Rio Tejo, Gaspar, Pedrosa, Territorios da Lisboa Medieval 3 225, barcos do tejo, getLISBON, o tejo originalsite |  |
| Bote | 7 | Barcos Tradicionais do Tejo e a Sua Co, Cacilheiros no Rio Tejo, Embarcações do Rio Tejo, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS, Pedrosa, barcos do tejo, getLISBON |  |
| Vapor | 7 | Barcos Tradicionais do Tejo e a Sua Co, Cacilheiros no Rio Tejo, Freire, Gaspar, Museu da Paisagem, getLISBON, mediotejo |  |
| Bateira | 6 | Embarcações do Rio Tejo, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS, Pedrosa, Territorios da Lisboa Medieval 3 225, barcos do tejo, getLISBON |  |
| Batel | 6 | Gaspar, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS, Pedrosa, Territorios da Lisboa Medieval 3 225, barcos do tejo, getLISBON | Batel do Tejo |
| Bote cacilheiro | 4 | Cacilheiros no Rio Tejo, Embarcações do Rio Tejo, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS, getLISBON |  |
| Bote de fragata | 4 | Barcos Tradicionais do Tejo e a Sua Co, Cacilheiros no Rio Tejo, barcos do tejo, getLISBON |  |
| Canoa cacilheira | 4 | Barcos Tradicionais do Tejo e a Sua Co, Cacilheiros no Rio Tejo, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS, getLISBON |  |
| Saveiro | 4 | Freire, Mar da Costa, Pedrosa, getLISBON |  |
| Avieiro | 3 | Freire, Territorios da Lisboa Medieval 3 225, barcos do tejo |  |
| Enviada | 3 | Embarcações do Rio Tejo, Pedrosa, barcos do tejo |  |
| Ferry | 3 | Cacilheiros no Rio Tejo, Museu da Paisagem, getLISBON |  |
| Barco da carreira | 2 | Gaspar, Pedrosa |  |
| Barco de Riba-Tejo | 2 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS, Pedrosa |  |
| Barco de dez mil ânforas | 2 | Embarcações do Rio Tejo, Territorios da Lisboa Medieval 3 225 |  |
| Barino | 2 | Barcos Tradicionais do Tejo e a Sua Co, Embarcações do Rio Tejo |  |
| Bote catralo | 2 | Barcos Tradicionais do Tejo e a Sua Co, Embarcações do Rio Tejo |  |
| Bote de pinho | 2 | Barcos Tradicionais do Tejo e a Sua Co, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Cangueiro | 2 | Barcos Tradicionais do Tejo e a Sua Co, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Caravela | 2 | Pedrosa, barcos do tejo |  |
| Caravelão | 2 | Territorios da Lisboa Medieval 3 225, barcos do tejo |  |
| Caíque | 2 | Cacilheiros no Rio Tejo, getLISBON |  |
| Hiate de poupa fechada | 2 | Barcos Tradicionais do Tejo e a Sua Co, Embarcações do Rio Tejo |  |
| Lancha Poveira | 2 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS, Pedrosa |  |
| Navio | 2 | Territorios da Lisboa Medieval 3 225, barcos do tejo |  |
| Piroga monóxila | 2 | Embarcações do Rio Tejo, Territorios da Lisboa Medieval 3 225 |  |
| Praieira | 2 | Embarcações do Rio Tejo, PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Rasca | 2 | Pedrosa, barcos do tejo |  |
| Avarga | 1 | Territorios da Lisboa Medieval 3 225 |  |
| Baleeira da Câmara de Lobos | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Baleeira do Pico | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Barca da Amieira | 1 | o tejo originalsite |  |
| Barca da Pesca do Alto | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Barca de moinho | 1 | Territorios da Lisboa Medieval 3 225 |  |
| Barca de passagem | 1 | Gaspar |  |
| Barca de peixe miúdo | 1 | Territorios da Lisboa Medieval 3 225 |  |
| Barca do pescado | 1 | barcos do tejo |  |
| Barca grande | 1 | Pedrosa |  |
| Barcaça | 1 | Gaspar |  |
| Barco Valboeiro | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Barco da Pesca do Carapau | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Barco de Avintes | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Barco de Riba Tejo | 1 | Pedrosa |  |
| Barco de Sacavém | 1 | Gaspar |  |
| Barco de couro | 1 | Embarcações do Rio Tejo |  |
| Barco de Ílhavo | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Barco dos moios | 1 | barcos do tejo |  |
| Barco Ílhavo | 1 | Embarcações do Rio Tejo |  |
| Barinel | 1 | barcos do tejo |  |
| Barquinho do Rio Minho | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Batel de pesca | 1 | Pedrosa |  |
| Bean-cod | 1 | Pedrosa |  |
| Bote da tartaranha | 1 | Pedrosa |  |
| Bote de tartaranha | 1 | Pedrosa |  |
| Bote do Pinho | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Bou | 1 | Pedrosa |  |
| Cacilheiro | 1 | Cacilheiros no Rio Tejo |  |
| Cacilheiro a vapor | 1 | Cacilheiros no Rio Tejo |  |
| Canoa da Picada | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Canoa do Espinel | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Caravela latina | 1 | Pedrosa |  |
| Catamarã | 1 | Museu da Paisagem |  |
| Catrafúcio | 1 | Freire |  |
| Caíque do Algarve | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Cesto de junco | 1 | o tejo originalsite |  |
| Cesto de vime | 1 | o tejo originalsite |  |
| Chalupa | 1 | o tejo originalsite |  |
| Chalupa de quatro remos | 1 | o tejo originalsite |  |
| Chincha | 1 | Pedrosa |  |
| Cu de lobo | 1 | Territorios da Lisboa Medieval 3 225 |  |
| Dóris | 1 | Pedrosa |  |
| Eborense | 1 | Cacilheiros no Rio Tejo |  |
| Enviada da Arte da Chávega | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Enviado do Atum | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Escaler | 1 | barcos do tejo |  |
| Ferry-boat | 1 | Cacilheiros no Rio Tejo |  |
| Fragateiro | 1 | Embarcações do Rio Tejo |  |
| Galé | 1 | Territorios da Lisboa Medieval 3 225 |  |
| Guiga | 1 | barcos do tejo |  |
| Gôndola | 1 | Pedrosa |  |
| Hiate | 1 | barcos do tejo |  |
| Jacht | 1 | Pedrosa |  |
| Jangada | 1 | Gaspar |  |
| Lancha | 1 | Pedrosa |  |
| Lancha do Alto | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Maceira | 1 | PORTUGAL MARÍTIMO  BARCOS TRADICIONAIS |  |
| Moinho | 1 | barcos do tejo |  |
| Monte Pragal | 1 | Cacilheiros no Rio Tejo |  |
| Muletim | 1 | Pedrosa |  |
| Nascara | 1 | Pedrosa |  |
| Nau | 1 | Territorios da Lisboa Medieval 3 225 |  |
| Navio de vela | 1 | Freire |  |
| Pinque | 1 | Pedrosa |  |
| Saveiro Meia-Lua | 1 | Mar da Costa |  |
| Saveiros and muletas (fishing) | 1 | Cacilheiros no Rio Tejo |  |
| Setubalense | 1 | Cacilheiros no Rio Tejo |  |
| Tartana | 1 | Pedrosa |  |
| Tartaranha | 1 | Pedrosa |  |
| Tasorea | 1 | Territorios da Lisboa Medieval 3 225 |  |
| Tasoreira | 1 | Territorios da Lisboa Medieval 3 225 |  |
| Terrada | 1 | Pedrosa |  |
| Veleiro | 1 | Freire |  |

## Appendix B. Places by status (all)

### Missing on the area's map (46)

Mouchões [Middle Tagus] (6), Porto de Lisboa [Tagus] (6), Barra do Tejo [Tagus] (4), Mar da Palha [Tagus] (4), Margem Direita do Tejo [Tagus] (4), Cais das Colunas [Tagus] (3), Mar entre o Cabo da Roca e Setúbal [Tagus] (3), Biblioteca da Sociedade de Geografia [Tagus] (2), Mouchões [Tagus] (2), Museu de Marinha [Tagus] (2), Ponta do Montijo [Tagus] (2), Ribeira de Sacavém [Tagus] (2), Alfama [Tagus] (1), Alvega [Middle Tagus] (1), Barca Nova [Middle Tagus] (1), Barra de Lisboa [Tagus] (1), Barreiras do Tejo [Tagus] (1), Barreiras do Tejo [Middle Tagus] (1), Cabedelo [Tagus] (1), Cais de Vila Franca de Xira [Tagus] (1), Cais do Sodré [Tagus] (1), Cais do Vapor [Middle Tagus] (1), Canais urbanos da Ria de Aveiro [Ria de Aveiro] (1), Canal Central da Ria [Ria de Aveiro] (1), Cardiga [Middle Tagus] (1), Castanheira do Ribatejo [Tagus] (1), Embocadura do Tejo [Tagus] (1), Entre-Cabos [Tagus] (1), Ermida de Nossa Senhora dos Remédios [Tagus] (1), Estação Fluvial de Belém [Tagus] (1), Esteiros do Termo de Lisboa [Tagus] (1), Estuário do Tejo a montante de Lisboa [Tagus] (1), Faial [Azores] (1), Porto de Muge [Middle Tagus] (1), Porto do Tejo [Tagus] (1), Povos [Tagus] (1), Praia da Trafaria [Tagus] (1), Ribeira de Lisboa [Tagus] (1), Ribeira de Muge [Middle Tagus] (1), Rio Zêzere [Middle Tagus] (1), Rio de Lisboa [Tagus] (1), Rossio [Middle Tagus] (1), Rossio de Abrantes [Middle Tagus] (1), Serra de Monsanto [Tagus] (1), Tejo a jusante de Tancos [Middle Tagus] (1), Vala do Carregado [Tagus] (1)

### Outside the game's maps (73)

Santarém (6), Azambuja (3), Chamusca (3), Porto do Sabugueiro (3), Zêzere (3), Alcántara (2), Almeirim (2), Ceuta (2), Entroncamento (2), Muge (2), Paço de Almeirim (2), Praia da Tocha (2), Valada (2), Vilar Formoso (2), Alenquer (1), Alfeizerão (1), Aranjuez (1), Arguim (1), Ayamonte (1), Belver (1), Benavente (1), Cabo Branco (1), Cachão do Cabril (1), Campo da Valada (1), Caparica (1), Cartaxo (1), Castelo de Bode (1), Castelo de Santa Cruz do Cabo de Gué (1), Chioggia (1), Cortes (1), Erges (1), Estreito de Gibraltar (1), Fonte da Telha (1), Fonte das Virtudes (1), Fratel (1), Genebra (1), Golfo de Cádis (1), Largo da Coroa (1), Marseille (1), Messina (1), Moncorvo (1), Montalvo (1), Monte Gordo (1), Ocreza (1), Olhão (1), Paris (1), Pesaro (1), Ponsul (1), Ponte de Sor (1), Portas do Ródão (1), Porto (1), Portos da Chamusca (1), Prado (1), Ribeira de Nisa (1), Rio Mondego (1), Rio Nabão (1), Sabugueiro (1), Salvaterra de Magos (1), Samora Correia (1), Sanlúcar de Barrameda (1), Segura (1), Sevilha (1), Sorraia (1), Talavera de la Reina (1), Tejo a montante de Almourol (1), Tejo upstream of Almourol (1), Toledo (1), Tomar (1), Vendas Novas (1), Vila Nova da Rainha (1), Vila Praia de Âncora (1), Vila Real de Santo António (1), Évora (1)

### Area unknown (21)

Wooden-boat shipyards (4), Porto da Cortiça (3), Porto de Arraiolos (3), Porto do Carv (3), Portos dos Frades (3), Lezírias (2), Alvito (1), Amoreira (1), Areal (1), Bogas (1), Canalem veterem (1), Capela do Senhor da Boa Morte (1), Charneca (1), Leito do Tejo (1), Mosela (1), Ponta do Cabedelo (1), Ponte da Marinha (1), Ribeira Nova (1), Rápidos (1), São Lourenço (1), Terra Alta (1)

### Only a sea mark (1)

Cacilhas [Tagus] (2)

### On the map, not a port (11)

Belém [Tagus] (3), Ribeira [Tagus] (3), Costa da Caparica [Tagus] (2), Rossio ao Sul do Tejo [Middle Tagus] (2), Alhandra [Tagus] (1), Alpriate [Tagus] (1), Cova do Vapor [Tagus] (1), Monte [Ria de Aveiro] (1), Pardilhó [Ria de Aveiro] (1), Quinta da Cardiga [Middle Tagus] (1), Rio de Moinhos [Middle Tagus] (1)

### Ports (23)

Lisboa [Tagus] (11), Abrantes [Middle Tagus] (7), Seixal [Tagus] (6), Tancos [Middle Tagus] (6), Constância [Middle Tagus] (5), Vila Nova da Barquinha [Middle Tagus] (5), Barreiro [Tagus] (3), Setúbal [Tagus] (3), Alcochete [Tagus] (2), Almada [Tagus] (2), Cais do Bico [Ria de Aveiro] (2), Montijo [Tagus] (2), Murtosa [Ria de Aveiro] (2), Praia do Ribatejo [Middle Tagus] (2), Sacavém [Tagus] (2), Sesimbra [Tagus] (2), Torreira [Ria de Aveiro] (2), Vila Franca de Xira [Tagus] (2), Alverca do Ribatejo [Tagus] (1), Castelo de Almourol [Middle Tagus] (1), Moita [Tagus] (1), Trafaria [Tagus] (1), Ílhavo [Ria de Aveiro] (1)

### Landmarks (3)

Ponte Marechal Carmona [Tagus] (2), Ponte 25 de Abril [Tagus] (1), Torre de Belém [Tagus] (1)

### The river or area itself (not counted) (13)

Esteiros do Tejo [Tagus] (6), Tejo [Tagus] (5), Foz do Tejo [Tagus] (4), Baixo Tejo [Tagus] (2), Margem Sul do Tejo [Tagus] (2), Alto Tejo (1), Canais do Tejo [Tagus] (1), Lezírias do Tejo (1), Margem do Tejo (1), Margens do Tejo [Tagus] (1), Ria de Aveiro [Ria de Aveiro] (1), Tejo abaixo de Santarém [Middle Tagus] (1), Tejo entre Abrantes e Azambuja [Middle Tagus] (1)

### Countries, seas and regions (not counted, 69)

Alentejo, Algarve, Alto Alentejo, Aveiro region, Azores, Baixo Tejo, Catalonia, Cova da Beira, Danúbio, Douro, England, Estuário do Tejo, Euphrates, Europe, France, Galicia, Golfo Pérsico, Holanda, Indian Ocean, Indies, Indus, Italy, Loire, Mallorca, Mediterranean, Mesopotamia, Nile, Nilo, North America, Northern provinces, Portugal, Portuguese Tagus, Portuguese and Spanish waters, Portuguese rivers, Provence, Região de Aveiro, Região de Aveiro, ria, Reno, Ria, Ria de Aveiro, Riba Tejo region, Ribatejo, Rio Minho, Ródano, Siniscalcato de Beaucaire (Provence), Spain, Spanish waters, Tagus, Tagus and tributaries in Spain, Tagus basin, Tagus basin in Spain, Tagus basin, Portugal, Tagus estuary, Tagus estuary ports, Tagus margins, Tagus, between the two banks, Tejo, Tejo estuary, Tibre, coast and interior of Portugal, coast of Portugal, coasts and rivers of Portugal, estuary and home regions, interior of Portugal, lower, middle and upper Tagus, rio Tejo, vale do Tejo, west coast, whole lagoon (Ria de Aveiro)

## Appendix C. Sailing and boat concepts the simulation does not show (all)

| Concept | Kind | The game would need | Sources |
| --- | --- | --- | --- |
| Lateen sail | boat part or gear | lateen sail rig | 7 |
| Silting of riverbed | sailing | water depth and silting | 6 |
| Cargo hold with paneiros | boat part or gear | cargo stowage detail | 3 |
| False bulwarks (bordas falsas) | boat part or gear | cargo stowage detail | 3 |
| Floods and flood tides | sailing | river flow and flood events | 3 |
| Towpaths (sirgadouros, caminhos de sirga) | boat part or gear | towing from the bank | 3 |
| Upstream direction (montante) | sailing | current direction and upstream sailing | 3 |
| Yard (verga) | boat part or gear | — | 3 |
| Aground | sailing | — | 2 |
| Amurar (setting the tack) | sailing | sail handling control | 2 |
| Current speed | sailing | tide and current | 2 |
| Curved or straight bows | boat part or gear | bow shape variants | 2 |
| Gaff rig | boat part or gear | gaff rig and jib | 2 |
| Low-water dry season | sailing | seasonal water depth | 2 |
| Lowering the sail (amainar) | sailing | sail lowering control | 2 |
| Navigability of the Tagus | sailing | seasonal water depth | 2 |
| Navigation hindered by sand and silt | sailing | water depth and silting | 2 |
| Net mesh size | boat part or gear | net mesh size and catch selectivity | 2 |
| Reefing | sailing | reefing control | 2 |
| Rig type | boat part or gear | multiple rig types | 2 |
| River flow (caudal) | sailing | seasonal river flow | 2 |
| River regime and rainfall | sailing | seasonal rainfall and river flow | 2 |
| Tidal influence on the Tagus | sailing | tide and current | 2 |
| Aft-raked mast | boat part or gear | mast rake setting | 1 |
| Ballast | boat part or gear | ballast and stability model | 1 |
| Bare poles | sailing | bare poles in storm | 1 |
| Bastard lateen yard | boat part or gear | lateen rig handling | 1 |
| Botalós (bow and stern poles) | boat part or gear | sail handling gear | 1 |
| Builder's mark | boat part or gear | decorative rudder marking | 1 |
| Capsizing of fishing boat (virada) | sailing | capsizing and stability model | 1 |
| Estuary navigation (tidal reach) | sailing | tide and current | 1 |
| Fish holds below deck | boat part or gear | fish hold and catch storage | 1 |
| Gondolé hull shape | boat part or gear | hull shape variations | 1 |
| Gybe warning command | sailing | crew commands | 1 |
| Irregular riverbed below Tancos | sailing | water depth and shifting riverbed | 1 |
| Jornal da ria (panels as news) | boat part or gear | decorative panels that change | 1 |
| Lug rig | boat part or gear | lug rig option | 1 |
| Mast-lowering system for bridges | boat part or gear | mast lowering control, bridges | 1 |
| Moliço scarcity and tide changes | sailing | tide and current | 1 |
| Natural and artificial obstacles to navigation | sailing | currents, obstacles, shallows | 1 |
| Navigation locks | boat part or gear | lock mechanics | 1 |
| Polychrome painting style | boat part or gear | decorative hull painting | 1 |
| Rainy season navigation | sailing | seasonal water level and current | 1 |
| Raised aft platform (castelo) | boat part or gear | steering oar control | 1 |
| Raised bow for poling | boat part or gear | poling | 1 |
| Raised inward-curving bow and stern | boat part or gear | hull shape variations | 1 |
| Rapids and mutual towing | sailing | river current and rapids | 1 |
| River depth | sailing | water depth | 1 |
| River regime and floods | sailing | river flow and floods | 1 |
| Silted reach between Almourol and Muge | sailing | water depth and silting | 1 |
| Summer low water and timber rafts | sailing | water depth by season | 1 |
| Summer sand on riverbed and grounding | sailing | water depth and grounding | 1 |
| Tartaranha (trawl net) | boat part or gear | trawl net fishing | 1 |
| Tidal waters of the lower Tagus | sailing | tide and current | 1 |
| Torrential river regime | sailing | variable river flow | 1 |
| Using flood tide to travel upriver | sailing | tide and current | 1 |
| Varredoura net | boat part or gear | fishing net gear | 1 |

Shown by the simulation (133): Shallow draught (8), Flat bottom hull (7), Rudder (7), Keel (6), Half keel (5), Sails powering Tagus boats (4), Approach and docking (3), Close-hauled (3), Gaff sail (vela de carangueja) (3), Gybing (3), Leeward (3), Leeway (sideways drift) (3), Sheet (3), Small bow sail (3), Tacking (3), Windward (3), Bastardo (large triangular main sail) (2), Bearing away (2), Easing the sheets (2), Forward-raked mast of the muleta (2), Heading up (2), Heel (2), In irons / head to wind (2), Leeboard (2), Masts and sails varying by function (2), Moliceiro trapezoidal sail (2), Muleta main sail (vela grande) (2), Running (wind astern) (2), Sail plan (velame) (2), Sail trim (2), Sheeting in (2), Sprit sail (2), Staysail (2), Steering oar (esparrela) (2), Vessel carrying capacity (lotação) (2), Xarolo rudder (2), Amurar e caçar (tacking and sheeting) (1), Apparent wind (1), Balancing forces on sails (1), Beam reach (1), Beating to windward (1), Blade rudder (leme de pá) (1), Bolinão (sail tensioning rope) (1), Boom (1), Broad reach (1), Centreboard (patilhão) (1), Cevadeira (quadrangular forward sail) (1), Charolo (transverse steering bar) (1), Close reach (1), Downwind sail setting rule (1), Drag (1), Drifting with current and wind (1), Drive (windward thrust) (1), Eight auxiliary trawling sails (1), Entremesa da ré (helmsman's seat lid) (1), Excessive heeling (1), Fair wind voyage to Lisbon (1), Fishing net types on the Tagus (1), Fishing nets as obstructions (1), Fixed rudder of the fragata (1), Fragateiro rig (1), Fresh northerly wind (1), Full rounded hull (casco bojudo) (1), Gale (vendaval) (1), Gust (1), Gybe procedure (1), Inboard rudder (1), Jib (bujarrona) (1), Keeled boats of Mar da Palha (1), Leech (1), Leg of a zigzag course (1), Lift (leeward suction) (1), Luffing (sail flapping) (1), Mainsail (1), Mainsheet (1), Mizzen (mezena) (1), Moitão (bow pulley) (1), Moliceiro load capacity (1), Muleta small forestay sails (1), Muleta stays with small sails (1), Net sleeves (manga, mão) (1), Net wing lines (alares) (1), Outboard rudder (1), Outboard tiller rudder (1), Over-eased sails (1), Points of sail (1), Port tack (1), Reaching (wind abeam to abaft the beam) (1), Rough sea conditions (1), Round sail rig (velame redondo) (1), Rudder pintles and gudgeons (1), Rudder tackles and cords (1), Sail area (1), Sail as airfoil (1), Sail camber (1), Sail rig (aparelho vélico) (1), Shallow moliço grounds (1), Square or round rig (1), Square sail (1), Square sail required on muletas (1), Starboard tack (1), Tack side (which side the wind comes from) (1), Tartaranha boat sail plan (1), Tiller (1), Tiller centred (1), Tiller-type rudder (leme de cana) (1), Tostes (moliceiro leeboards) (1), Trapezoidal sail (1), True wind (1), Upwind sailing (1), Upwind trim rule (1), Varredoura sails (1), Veleiro (good sailer) (1), Voyage durations (1), Wind indicator (1), Wind on the quarter (1), Wind shift (1), Wing and wing (1), Winter lowering lines (carregadeiras) (1), Added mass (0), Angle of attack (0), Foil (lifting surface) (0), Going backwards (drag astern) (0), Hull speed (0), No-go zone (0), Sail lift/drag ratio (0), Single-sail fore-and-aft rigs (0), Square sail no-go angle (0), Surge, sway, yaw (0), Trimming front and rear sails to turn (0), Wearing round instead of tacking (0), Windage (0), Yaw damping (0)

Out of scope (37): Quarter (hull area), Beam (widest part), Bow quarter (hull area), Port side, Starboard side, Rigging (spars and stays), Mast, Stern, Bow, Beam of hull (boca), Cabeleira ou borla (varino bow tuft), Flat transom stern, Masthead colour marking (calcês), Water mills on the river, Fixed fishing structures, Apegadas raised structure, Camareta shelter, Bastard lateen sail, Diverging masts, Asymmetric forward-raked masts, Toothed bow (proa dentada), Open-waisted hull (boca aberta), Low hull sides, Moliço rakes (ancinhos), Hull length, Castelo da proa (bow cabin), Cagarete (stern store), Bow and stern stem pieces (rodas), Top side plank (tábua de verdejar), Mast socket (pia), Stern bulkhead compartment (entremesa), Non-slip grip material (sarrim), Moliceiro size and dimensions, Moliceiro hull shape description, Lowered midship side for loading, Hull side (costado), Farming tools (alfaias)

## Appendix D. Historical practices against the game's activities (all)

### Covered (10)

| Practice | Sources | Closest activity | Why |
| --- | --- | --- | --- |
| River traffic linking Tagus banks until mid-20th century | 5 | mini.passengers | Passenger and cargo routes across and along the Tagus with period boats. |
| Barcos d'água acima carrying freight Ribatejo-Lisboa | 4 | route.vfx-lisboa | Cargo run down the Tagus from the lezírias to Lisbon matches freight transport. |
| Supplying anchored ships at Lisbon | 4 | mini.supplies | Supply run takes goods out to a boat at sea; here ships at anchor. |
| Moliço gathering with moliceiros | 3 | mini.seaweed | Gathering moliço with a Moliceiro in the Ria de Aveiro. |
| Muleta fishing grounds with tartaranha net | 3 | mini.fishing | Muleta drags net over Tagus shoals, with Seixal and barra grounds. |
| Bote passenger service Cacilhas-Almada-Lisboa | 2 | route.lisboa-almada | Passengers across the river between Lisbon and Almada, as catraios did. |
| Enviada and Enviado boats ferrying catch | 1 | kind.supply | Supply run ferries goods and fish between a fishing boat and shore. |
| Keel boats carrying people and cargo from Cacilhas | 1 | route.moita-lisboa | Cargo from the south bank; keel boat and Cacilhas origin differ slightly. |
| Medieval Tagus as busy river highway | 1 | mini.busy | Busy Tagus cargo crossing among many boats with Fragata matches the river highway. |
| Whaling in the Azores and Madeira | 1 | kind.whaling | Whaling mission with Azorean whalers approaching a sperm whale from astern. |

### Partly covered (41)

| Practice | Sources | Closest activity | Why |
| --- | --- | --- | --- |
| Avieiros fishing and living aboard bateiras | 2 | kind.fishing | Fishing exists, but not Avieiro bateiras or life aboard. |
| Boat service Lisbon to Montijo (Aldeia Galega) | 2 | route.moita-lisboa | Similar south bank to Lisbon route, but Montijo itself is not a route. |
| Boat types and uses by Tagus section | 2 | route.barquinha-almourol | Middle Tagus routes exist, but not the flat-bottomed boats or river fishing. |
| Cangueiros hauling heavy cargo to Lisbon | 2 | route.moita-lisboa | Cargo to Lisbon exists, but not cangueiro boats or specific materials. |
| Fragatas handling cargo at Lisbon harbour | 2 | mini.busy | Fragata cargo crossing exists, but no loading or unloading of anchored ships. |
| Muletas and rascas trading beyond the bar | 2 | kind.supply | Supply run goes out to sea, but not trading cargo beyond the bar. |
| 15th-century trade between Lisbon, the south bank and upriver | 1 | route.moita-lisboa | South bank to Lisbon trade exists; Coina, Almada and upriver links differ. |
| 16th-century produce and wine shipped to Lisbon | 1 | route.vfx-lisboa | Long haul down from the lezírias, but no melons or wine. |
| Avieiros and freight traffic in the Mouchões | 1 | route.vfx-lisboa | Freight transport near Vila Franca exists, but not in the Mouchões. |
| Azorean mackerel fishing boat | 1 | kind.fishing | Fishing exists, but not Azorean mackerel fishing with oars and bow pulley. |
| Barcas calling at Porto de Muge at rent time | 1 | route.moita-lisboa | Tagus cargo and passenger routes exist, but not rent-time calls at Porto de Muge. |
| Barco Rabelo carrying wine down the Douro | 1 | route.vfx-lisboa | River cargo haul exists on the Tagus, not wine barrels down the Douro. |
| Barquinho do Rio Minho river crossing and cargo | 1 | mini.passengers | River passenger and cargo crossings exist, but not on the Minho or with this boat. |
| Boat freight from Rossio to Lisbon | 1 | route.vfx-lisboa | Goods to Lisbon from upriver, but not Rossio or wheat and cork. |
| Boats serving Lisbon from Tagus ports in 16th century | 1 | route.vfx-lisboa | Tagus ports to Lisbon cargo, but not Vila Nova da Rainha or schedules. |
| Bote do Pinho carrying pine branches | 1 | kind.transport | Cargo transport exists on the Tagus, but not pine branches by Bote do Pinho. |
| Canoa da Picada sardine fishing | 1 | ground.cascais | Cascais fishing ground exists, but not sardine picking or Canoa da Picada racing. |
| Canoa do Espinel line fishing at Olhão | 1 | kind.fishing | Fishing exists, but not espinel line fishing at Olhão. |
| Cork shipping from Rossio de Abrantes | 1 | route.vfx-lisboa | Upriver cargo to Lisbon exists, but not cork or Rossio. |
| Costa de Caparica beach fishing | 1 | kind.fishing | Fishing exists, but not beach launching at Costa de Caparica. |
| Deep-sea fishing boats of Sesimbra and Setúbal | 1 | kind.fishing | Fishing exists, but not deep-sea fishing with oars off Sesimbra. |
| Douro boats named by cargo (Valboeiro and Avintes) | 1 | kind.transport | Carrying goods and passengers between banks exists, but not on the Douro. |
| Fish landing at Lisbon by muletas | 1 | mini.supplies | Bringing fish home exists, but not landing catches at Lisbon. |
| Goods carried upriver on the Tagus | 1 | route.constancia-abrantes | Upriver runs exist, but not salt and fish cargo. |
| Hauling the tartaranha net | 1 | mini.fishing | Net dragging exists, but not paying out cable or hours-long hand hauling. |
| Industrial export by river boat to Tejo estuary ships | 1 | route.moita-lisboa | Cargo to Lisbon is similar, but not transfer to estuary ships. |
| Lancha Poveira fisheries | 1 | kind.fishing | Fishing is offered, but not Poveira boats or their different fisheries. |
| Lenten flatfish fishing for the king despite tartaranha ban | 1 | kind.fishing | Fishing in the Tagus exists, but no tartaranha, Lent or royal supply. |
| Lime shipment to Lisbon via river ports | 1 | kind.transport | Generic cargo exists, but no lime or north bank ports. |
| Lisbon bathers reaching south-bank beaches | 1 | route.lisboa-almada | Passenger crossing of the Tagus exists, but not bathers going to Trafaria. |
| Maceira fishing at Vila Praia de Âncora | 1 | kind.fishing | Fishing exists, but with the Muleta, not the Maceira at Âncora. |
| Medieval Tagus river fishing | 1 | kind.fishing | Fishing exists, but with Muleta at sea, not bateis in Tagus currents. |
| Moliceiro propulsion: poling, towing, sailing | 1 | mini.seaweed | Moliceiro sailing exists, but poling and towing are not described. |
| Priors travelling by Barca da Amieira | 1 | route.barquinha-almourol | Passenger river travel exists, but not on Barca da Amieira or Flor da Rosa. |
| Recreations of moliço harvesting | 1 | mini.seaweed | Museum mini-game recreates moliço gathering, though not as a staged ethnographic display. |
| Santarém region supplying Lisbon with cereals and timber | 1 | route.constancia-abrantes | Upper Tagus cargo runs exist, but no Santarém route or cereals and timber supply. |
| Sea fishing at Foz and Embocadura | 1 | ground.barra | Fishing at river mouth exists, but with the Muleta, not Foz/Embocadura specifically. |
| Steamer passenger travel on the upper Tagus | 1 | kind.transport | Passenger routes exist, but not by steamer or Santarém route. |
| Tagus fish markets and trade | 1 | kind.fishing | Fishing and cargo exist, but not selling at Tagus markets. |
| Timber floated and shipped to Lisbon | 1 | route.vfx-lisboa | Downriver haul from Vila Franca to Lisbon exists, but timber floating doesn't. |
| Western coast timber reaching Lisbon by sea | 1 | route.moita-lisboa | Cargo to Lisbon exists, but not timber, rafts, or sea arrival. |

### No activity (60)

| Practice | Sources | Closest activity | Why |
| --- | --- | --- | --- |
| Barco d'água acima crew roles | 2 | — | No crew roles or hierarchy (arrais, camaradas, moços) in any game activity. |
| Fragata crew and rowing | 2 | — | No rowing or towing of a fragata when becalmed. |
| Medieval Santarém maritime links | 2 | — | No medieval maritime links with North Africa or Europe. |
| Moliceiro caulking and pitching | 2 | — | Caulking and pitching isn't offered. |
| Moliceiro panel painting | 2 | — | Panel painting is not an activity. |
| Muleta rigged as iate | 2 | — | No option to rig a Muleta as an iate. |
| Royal boat travel Almeirim-Lisbon | 2 | — | No royal travel route between Almeirim and Lisbon. |
| Xávega beach-hauled net at Costa de Caparica | 2 | — | Beach-hauled xávega net fishing is not offered. |
| Abrantes foreign trade organisation | 1 | — | Trade organisation is not a playable activity. |
| Adaptation of tools and boats for moliço harvesting | 1 | — | Adapting tools and boats for loading moliço isn't represented. |
| Alcántara ore convoys to Lisbon | 1 | — | No Alcántara ore convoys or rapids route. |
| Almourol dam and canals | 1 | — | Dam and irrigation engineering proposal; the game has nothing comparable. |
| Boatmen leaving upriver ports | 1 | — | Boatmen relocating or changing careers is not playable. |
| Brandy distilling to cut freight cost | 1 | — | Brandy distilling is not in the game. |
| Car-carrying ferries | 1 | — | No car-carrying ferries or vehicle transport. |
| Charneca scrub, firewood and charcoal | 1 | — | Land-based scrub, firewood and charcoal production is not a sailing activity. |
| Cod ships' small boats | 1 | — | No cod ship dories or daily rowing from the fishing ground. |
| Crews and shipyards of Barreiro, Seixal and Trafaria | 1 | — | Shipyard origins and crew recruitment are not playable activities. |
| Curative springs of Fonte das Virtudes | 1 | — | Medical spa treatment at springs; no game equivalent. |
| Decorative painting of Tagus boats | 1 | — | Boat decoration painting is not a game activity. |
| Dry-season rafting of timber and cork | 1 | — | Rafting timber and cork is not offered. |
| Early illustrations of tartana and muleta | 1 | — | Early illustrations are documentary, with no matching game activity. |
| Fonte da Telha fishing hamlet huts | 1 | — | Hamlet huts and housing; no sailing activity matches. |
| French proposals to introduce the tartana in Portugal | 1 | — | Historical proposals to introduce the tartana are not playable. |
| Fuel barges to Rossio quay | 1 | — | No fuel barge runs or quay pumping. |
| Furling the muleta sail | 1 | — | Furling with brails and climbing the yard is not modelled. |
| Galician caravels fishing at Cabo Branco | 1 | — | No Galician caravel voyages to Cabo Branco. |
| Industry siting near navigable waterways | 1 | — | Industrial siting near waterways is not represented. |
| José da Silva's boat business at Constância | 1 | — | Boat business and building at Constância are not represented. |
| Large boats built in northern coastal shipyards | 1 | — | Northern shipyard boat building is not represented. |
| Leeboard of the muleta and its origins | 1 | — | Leeboard history is not an activity, though the Muleta may have one. |
| Moliceiro boatbuilding knowledge transmission | 1 | — | Oral transmission of boatbuilding skills isn't gameplay. |
| Moliceiro construction | 1 | — | Boat construction isn't playable; the game only offers sailing. |
| Moliceiro festival decoration | 1 | — | Festival decoration with flags and branches isn't offered. |
| Moliceiro hull construction | 1 | — | Hull construction isn't offered. |
| Moliceiro hull laying out on stakes | 1 | — | Laying out hull stakes isn't offered. |
| Moliceiro shipyards and building knowledge | 1 | — | Shipyard lineages and building knowledge aren't gameplay. |
| Muleta coastal trade to Algarve and Morocco | 1 | — | No Algarve or Moroccan coastal trading routes for the Muleta. |
| Nile irrigation | 1 | — | Nile irrigation is outside the game's places and activities. |
| Overland ox-cart transport to river ports | 1 | — | Overland ox-cart transport is not a sailing activity in the game. |
| Overland ox-cart transport to river ports | 1 | — | Ox-cart haulage to paper mills is overland, not in the game. |
| Railway company hiring boatmen and buying boats | 1 | — | Railway company labour and boat-buying policy has no gameplay equivalent. |
| Regulating Tagus flow by afforestation and dams | 1 | — | River flow regulation by afforestation and dams is not a sailing activity. |
| Ribatejo agricultural conversion | 1 | — | Agricultural and wine-economy policy; no matching game activity. |
| Right bank forestry | 1 | — | Right bank forestry has no game activity. |
| Riverbank and angling fishing on the Tagus | 1 | — | Bank and angling fishing from shore is not offered; fishing is boat-based. |
| Riverside villagers managing fresh water | 1 | — | Village water management through ditches and channels is not represented. |
| Roman use of inland navigation | 1 | — | Roman inland navigation has no game equivalent. |
| Rossio de Abrantes wholesale and redistribution | 1 | — | Wholesale and redistribution at Rossio are not represented. |
| Settlement of Costa da Caparica by Ílhavo and Algarve fishermen | 1 | — | Settlement history of fishing communities; no game activity. |
| Steam cargo and warehouse trade at Barquinha quay | 1 | — | No steam cargo boats or quay warehouse trade at Barquinha. |
| Supplying the royal household with fish | 1 | — | Supplying a royal household with fish is not a game activity. |
| Tapa-esteiros fishing in Mar da Palha | 1 | — | Tapa-esteiros fishing with a support canoa is not offered. |
| Tartana rigging and foreign crews | 1 | — | Tartana rigging and foreign crews are not represented. |
| Tartaranha fishermen as bar pilots and fish suppliers | 1 | — | No bar pilotage or assisting India ships by fishermen. |
| Timber felling and transport to Tagus | 1 | — | Timber felling and treatment are not sailing activities. |
| Towing boats from the bank at Cachão do Cabril | 1 | — | No towing from the bank or rapids passage in the game. |
| Upriver crews poling and towing barcos de água acima | 1 | — | No poling or towing upriver; upper Tagus routes are sailed. |
| Valada flood dikes | 1 | — | Flood dikes are not a sailing activity. |
| Wasteful sale of young shad | 1 | — | Wasteful sale of young shad has no equivalent. |
