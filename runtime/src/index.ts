// Runtime for the Tagus sailing game: no dependencies, no LLM calls.
// observer/: reads the physics each step and reports events and the challenge level.
// The challenge-aware scheduler (phase 2) builds on it.

export * from './observer';

export type Beat = "setup" | "complication" | "turn" | "close" | "epilogue" | "generic";
export type Status = "draft" | "verified" | "reviewed" | "approved";

export interface LineRecord {
  id: string;
  mission: number;
  boat: string;
  zone: string;
  beat: Beat;
  trigger: string;
  character: string;
  thread?: string;
  concept?: string;
  text: { pt: string; en?: string; fr?: string };
  depth: 1 | 2;
  fictional?: boolean;
  sources: string[];
  callbacks?: string[];
  status: Status;
}
