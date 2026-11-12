// Generic runtime: no dependencies, no LLM calls. Domain packs supply the adapter that turns
// a simulation's state into events and a difficulty level (see domains/sailing/adapter).
// The scheduler that times lines by difficulty will live here.

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
