// Thresholds for the observer. Defaults are first guesses from fragateiro's physics and its
// drills (src/world/drills.ts); the workbench lets you tune them against recordings.
// Documented in knowledge/game-physics.yaml.

export interface ObserverConfig {
  /** Point-of-sail band edges, deg off the bow: irons | close-hauled | close reach | beam | broad | running. */
  bands: [number, number, number, number, number];
  /** Wind must be this far from the bow or stern before the tack side counts as changed (drills.ts). */
  sideMarginDeg: number;
  /** Controlled gybe: sheets at most this far out as the stern crosses (drillRules.gybeSheetMax). */
  gybeSheetMax: number;
  capsizeHeelDeg: number;
  irons: { enterSpeed: number; enterSeconds: number; exitAngleDeg: number; exitSpeed: number };
  luffing: { start: number; startSeconds: number; stop: number; stopSeconds: number; steadyYawDegS: number };
  heelWarning: number;
  heelRearm: number;
  gust: { rise: number; windowSeconds: number };
  shift: { deg: number; windowSeconds: number };
  pointOfSailHoldSeconds: number;
  steadyLeg: { headingDeg: number; seconds: number };
  steerageSpeed: number;
  activityWindowSeconds: number;
  timerWarningSeconds: number;
  challenge: {
    decaySeconds: number;
    manoeuvre: { load: number; yawDegS: number; nearDeg: number };
    inIrons: number;
    heelFrom: number;
    closeQuarters: { timeToContact: number; load: number };
    approach: number;
    aground: number;
    gustOrShift: number;
    busyHands: { activity: number; load: number };
    luffing: { above: number; load: number };
    timePressure: number;
  };
  calm: { maxLoad: number; minSeconds: number; maxYawDegS: number };
}

export const DEFAULT_CONFIG: ObserverConfig = {
  bands: [36, 60, 80, 100, 150],
  sideMarginDeg: 20,
  gybeSheetMax: 0.5,
  capsizeHeelDeg: 30,
  irons: { enterSpeed: 0.5, enterSeconds: 3, exitAngleDeg: 45, exitSpeed: 0.8 },
  luffing: { start: 0.5, startSeconds: 5, stop: 0.2, stopSeconds: 3, steadyYawDegS: 3 },
  heelWarning: 0.7,
  heelRearm: 0.5,
  gust: { rise: 0.3, windowSeconds: 5 },
  shift: { deg: 10, windowSeconds: 5 },
  pointOfSailHoldSeconds: 5,
  steadyLeg: { headingDeg: 10, seconds: 20 },
  steerageSpeed: 0.8,
  activityWindowSeconds: 2,
  timerWarningSeconds: 15,
  challenge: {
    decaySeconds: 3,
    manoeuvre: { load: 0.9, yawDegS: 3, nearDeg: 20 },
    inIrons: 0.8,
    heelFrom: 0.6,
    closeQuarters: { timeToContact: 15, load: 0.85 },
    approach: 0.7,
    aground: 0.8,
    gustOrShift: 0.5,
    busyHands: { activity: 0.6, load: 0.5 },
    luffing: { above: 0.5, load: 0.4 },
    timePressure: 0.6,
  },
  calm: { maxLoad: 0.3, minSeconds: 2, maxYawDegS: 2 },
};

/** Deep-merge partial overrides (e.g. from the workbench sliders) onto the defaults. */
export function withConfig(overrides: DeepPartial<ObserverConfig> = {}): ObserverConfig {
  return merge(DEFAULT_CONFIG, overrides) as ObserverConfig;
}

export type DeepPartial<T> = { [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K] };

function merge(base: unknown, over: unknown): unknown {
  if (over === undefined) return structuredClone(base);
  if (Array.isArray(base) || typeof base !== 'object' || base === null) return over;
  const out: Record<string, unknown> = {};
  const b = base as Record<string, unknown>;
  const o = over as Record<string, unknown>;
  for (const k of new Set([...Object.keys(b), ...Object.keys(o)])) out[k] = merge(b[k], o[k]);
  return out;
}
