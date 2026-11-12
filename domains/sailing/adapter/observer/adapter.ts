// Build a Frame from a fragateiro SailboatSim. Structural types only: the runtime does not
// import the game, so it stays dependency-free and works with any simulator of this shape.

import type { Frame, FrameContext } from './types';

interface SimLike {
  spec: { id: string; sails: { id: string; group: string }[] };
  state: { time: number; heading: number; u: number; v: number; r: number; heel: number; x: number; y: number };
  controls: { rudder: number; sheets: Record<string, number>; mode: string };
  report: {
    sails: { id: string; active: boolean; luffing: boolean }[];
    trueWindAngleDeg: number; apparentWindAngleDeg: number; apparentWindSpeed: number;
  };
  wind: { at(t: number, x: number, y: number): { from: number; speed: number } };
  bestSheets(): Record<string, number>;
}

export function fromSim(sim: SimLike, context?: FrameContext): Frame {
  const s = sim.state;
  const w = sim.wind.at(s.time, s.x, s.y);
  const active = sim.report.sails.filter((x) => x.active);
  return {
    t: s.time,
    heading: s.heading,
    u: s.u,
    v: s.v,
    r: s.r,
    heel: s.heel,
    rudder: sim.controls.rudder,
    sheets: { ...sim.controls.sheets },
    bestSheets: sim.bestSheets(),
    twaDeg: sim.report.trueWindAngleDeg,
    awaDeg: sim.report.apparentWindAngleDeg,
    aws: sim.report.apparentWindSpeed,
    windFromDeg: ((w.from * 180) / Math.PI + 360) % 360,
    windSpeed: w.speed,
    luffing: active.length ? active.filter((x) => x.luffing).length / active.length : 0,
    mode: sim.controls.mode,
    boat: sim.spec.id,
    context,
  };
}
