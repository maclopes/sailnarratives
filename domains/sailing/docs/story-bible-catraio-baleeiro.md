# Story bible and arcs: Catraio and Baleeiro missions

Draft, 2026-11-12. Live version: https://claude.ai/artifact/2Dc9b3b3cuNdKWih3Draqf
Settings, characters and beats are proposals. Facts come from the leaflet source library and must be checked against originals.

## Approach

Each mission is a short story with a beginning, a complication and an ending, and the sailing supplies the complication. Facts are never shown as cards: a character says them because they matter to that character at that moment.

- Story first. The cast and the arc are written by hand. Retrieval then supplies the true detail each beat needs, so it grounds the story instead of driving it.
- Thread chosen: time. Catraio (Tagus) and Baleeiro (Azores) are far apart, so place cannot link them. The link is the working life of the river and the islands through time, each boat a different era seen from the water. A place thread (one landing seen through several boats) stays possible for the Tagus-only missions.
- Fiction and fact are labelled. Characters are invented; the context is documented. Every factual line carries source IDs, and the optional depth-2 card says what is real.
- Instruction as reaction. Sailing guidance is the character reacting to what the player does (a tack, being stuck in irons), not a separate tutorial.

## Cast

Both characters are invented. Their world (trades, boats, dates) comes from the sources.

| Character | Boat and place | What they want | Voice |
| --- | --- | --- | --- |
| Tio Joaquim, catraeiro | Catraio, Lisbon to Almada | To bring today's fares across before the tide and the steamers take the afternoon | Dry, practical, a little proud of a trade he sees shrinking |
| Mestre Manuel, former whaler | Bote baleeiro, off Horta | To take a young crew out to watch, from the kind of boat he once hunted in | Calm, spare, speaks to the crew more than to the player |
| A passenger (Catraio) | Catraio | To reach the south bank for a reason the player learns during the crossing | Curious, asks the questions the player would ask |
| A young crew member (Baleeiro) | Baleeiro | To understand why the old men look at the sea the way they do | Quiet, learns by watching |

The boatmen speak the sailing instruction; the passenger and the young crew member are the player's proxies for the optional questions.

## Mission 3: Passengers with the Catraio

Set on a working day in the mid-1920s (a proposal), the period of the Cooperativa de Catraeiros do Porto de Lisboa. Tio Joaquim has one crossing to make before the tide turns, with a passenger who has not said why she is going to Almada.

| Beat | Sailing trigger | What happens (gist) | Fact retrieval must supply | Concept taught |
| --- | --- | --- | --- | --- |
| Setup | Mission starts at the Lisbon quay | Joaquim sizes up wind and tide and says what kind of crossing it will be | Catraeiros carried people between Lisbon and the south bank | Reading the wind before leaving |
| Complication 1 | First leg is upwind | The boat will not go straight; he explains why they zigzag | Small open boats, sail and oars | Bolina, virar de bordo, caçar |
| Complication 2 | Steamer or other boat close in the channel | A steamer's wake rocks the boat; he grumbles about the fares it takes | Steam arrived in the 1860s; once more than 2,000 boats worked this crossing | Arribar to keep clear, orçar to hold course |
| Turn | Player stuck in irons, or wind shifts | The passenger asks why he stays in a trade that is shrinking; he answers, and she finally says why she is going | The cooperative founded by boatmen at Porto Brandão in the mid-1920s | Cambar, folgar and caçar to get moving again |
| Close | Approach and dock at Almada | A quiet line about the crossing and the people on it; the passenger pays | None needed | Orçar to slow, coming alongside |

Depth-2 epilogue card (optional): the 1966 bridge ended the vehicle ferries, which is why Joaquim's world was already narrowing.

## Mission 4: Whale watching with the Baleeiro

Set today, with a restored bote (a proposal). Mestre Manuel hunted from this kind of boat until the ban in 1984 and now takes a young crew out only to watch. The rocket that once launched the boats becomes the signal to go and look.

| Beat | Sailing trigger | What happens (gist) | Fact retrieval must supply | Concept taught |
| --- | --- | --- | --- | --- |
| Setup | Mission starts off Horta | The vigia's signal goes up; Manuel says what it meant when he was young, and what it means today | On land a lookout watched for the blows and fired a rocket to launch the boats | Approaching under sail and oars |
| Complication 1 | Player approaches from the wrong side or too fast | He tells the crew to come in behind, slowly, and why a whale must not be pushed | The bote was an open boat with a crew of seven | Orçar and arribar to set the angle, folgar to slow |
| Complication 2 | Wind shifts or the whale dives and moves | The crew repositions quietly; the young crew member asks how he knows where it will come up | Boats went out under sail or oars; the hunt used hand-thrown harpoons | Virar de bordo, cambar |
| Turn | Player is close and holds station | Manuel says nothing for a while, then a short line about what he used to do from this spot | Azorean whaling developed in the second half of the 19th century; the hunt ended in 1984 | Holding position, trimming to drift |
| Close | The whale leaves or the timer ends | The ending says you watched it, not harpooned it. Manuel's last line is about the boat, not the whale | In July 2026 a consultation opened on listing the bote's construction and handling as national intangible heritage | Returning to port |

Tone note: Manuel must not romanticise the hunt. The mission keeps one honest line about what it was, and no scoring for approaching.

## Line records and retrieval

See ../schema/line-record.schema.json and ../examples/cat-03-turn-02.json. Three fields do the work that trivia cannot: beat and character fix what a line is for and who says it, and callbacks lets a later line refer to an earlier one the player has heard. If no sourced line exists for a trigger, the game plays a generic, fact-free line instead of inventing one.

## To verify and next steps

- [ ] Confirm the mid-1920s date for the cooperative at Porto Brandão and choose the exact year for the Catraio setting
- [ ] Check the figure of more than 2,000 boats between Lisbon and Almada and the date it applies to
- [ ] Confirm the catraio's size and rig
- [ ] Confirm the bote crew of seven and the role of the vigia's rocket against a second source
- [ ] Ask a historian whether the present-day Baleeiro setting fits how the heritage community would want it told
- [ ] Decide whether the time thread stays, or the Tagus missions get a place thread of their own
- [ ] Write the line bank in Portuguese first, then English and French, with native review
- [ ] Test with players: story arcs vs the same facts as plain cards, measuring recall and enjoyment
