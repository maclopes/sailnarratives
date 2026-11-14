// Types of a line bank as the game receives it (contract: the game's content/narrative/README.md).

export type Delivery = "cue" | "story" | "reflection" | "leg" | "curiosity" | "ack" | "trivia";

export interface BankLine {
  id: string;
  /** setup, complication, turn, close, leg, place, curiosity, ack, trivia */
  beat?: string;
  /** a game moment id, `near_place:<name>`, or `idle` for lines played in quiet moments */
  trigger: string;
  delivery: Delivery;
  speaker: string;
  text: Record<string, string>;
  /** for a cue that asks the player to do something: the moments that show it was done */
  expects?: string[];
  /** seconds to wait for an expected moment (default 15) */
  within?: number;
  /** for trivia: boat, place, fish, work, people… */
  topic?: string;
  when?: { boats?: string[]; areas?: string[]; places?: string[] };
  audio?: Record<string, { file: string; seconds: number }>;
  fictional?: boolean;
  sources?: string[];
  status: "verified" | "approved";
}

export interface LineBank {
  version: number;
  minigame: string;
  variant: string;
  languages: string[];
  cast: { id: string; name: Record<string, string>; fictional?: boolean }[];
  lines: BankLine[];
}
