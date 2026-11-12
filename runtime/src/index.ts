// Runtime selector for the Tagus sailing game.
// Implemented in prompt 07 (createNarrator, onTrigger, heard, reset, requestCuriosity).
// For now this only exports the line-record type shared with the pipeline.

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
