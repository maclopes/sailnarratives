// The observer: feed it one Frame per step (10 Hz is enough) and it reports derived
// quantities, events (the trigger vocabulary) and the challenge level.

import { withConfig, type DeepPartial, type ObserverConfig } from './config';
import type { ChallengeFactor, Derived, Frame, Observation, ObserverEvent, PointOfSail } from './types';

const DEG = 180 / Math.PI;
const KNOT = 0.514444;
const POINTS: PointOfSail[] = ['in_irons', 'close_hauled', 'close_reach', 'beam_reach', 'broad_reach', 'running'];

interface Sample { t: number; windSpeed: number; windFrom: number; heading: number }

export class Observer {
  readonly config: ObserverConfig;
  private last?: Frame;
  private history: Sample[] = [];
  private activity = 0;
  // event state
  private side: 1 | -1 | 0 = 0;
  private crossing: 'bow' | 'stern' | null = null;
  private crossingSheet = 0;
  private ironsSince: number | null = null;
  private inIrons = false;
  private luffSince: number | null = null;
  private luffClearSince: number | null = null;
  private luffingOn = false;
  private heelWarned = false;
  private capsized = false;
  private gustUntil = -Infinity;
  private shiftUntil = -Infinity;
  private gustArmed = true;
  private shiftArmed = true;
  private pos: PointOfSail | null = null;
  private posCandidate: PointOfSail | null = null;
  private posSince = 0;
  private legStart: { t: number; heading: number } | null = null;
  private legReported = false;
  private aground = false;
  private approaching = false;
  private timerWarned = false;
  private timerEnded = false;
  private started = false;
  // challenge state
  private load = 0;
  private calmSince: number | null = null;

  constructor(overrides: DeepPartial<ObserverConfig> = {}) {
    this.config = withConfig(overrides);
  }

  reset(): void {
    Object.assign(this, new Observer(this.config as DeepPartial<ObserverConfig>));
  }

  push(f: Frame): Observation {
    const dt = this.last ? Math.max(0, f.t - this.last.t) : 0;
    this.updateActivity(f, dt);
    this.history.push({ t: f.t, windSpeed: f.windSpeed, windFrom: f.windFromDeg, heading: f.heading });
    const horizon = Math.max(this.config.gust.windowSeconds, this.config.shift.windowSeconds, this.config.steadyLeg.seconds);
    while (this.history.length && this.history[0]!.t < f.t - horizon) this.history.shift();

    const derived = this.derive(f);
    const events: ObserverEvent[] = [];
    const emit = (type: string, data?: ObserverEvent['data']) => events.push(data ? { type, t: f.t, data } : { type, t: f.t });

    if (!this.started) { this.started = true; emit('start'); }
    this.detectTurns(f, emit);
    this.detectIrons(f, emit);
    this.detectLuffing(f, derived, emit);
    this.detectHeel(derived, emit);
    this.detectWind(f, emit);
    this.detectPointOfSail(f, derived, emit);
    this.detectSteadyLeg(f, emit);
    this.detectContext(f, emit);

    const { rawLoad, factors } = this.challenge(f, derived);
    this.load = Math.max(rawLoad, this.load - (dt / this.config.challenge.decaySeconds));
    const steady = Math.abs(f.r * DEG) <= this.config.calm.maxYawDegS;
    if (this.load < this.config.calm.maxLoad && steady) this.calmSince ??= f.t;
    else this.calmSince = null;
    const calmFor = this.calmSince === null ? 0 : f.t - this.calmSince;
    const calm = this.calmSince !== null && calmFor >= this.config.calm.minSeconds;

    this.last = f;
    return { t: f.t, derived, events, rawLoad, load: this.load, factors, calm, calmFor: calm ? calmFor : 0 };
  }

  // ---- derived quantities -------------------------------------------------------------

  private derive(f: Frame): Derived {
    const speed = Math.hypot(f.u, f.v);
    const twa = Math.abs(f.twaDeg);
    const b = this.config.bands;
    const idx = b.findIndex((edge) => twa < edge);
    let trimError: number | undefined;
    if (f.bestSheets) {
      const groups = Object.keys(f.bestSheets).filter((g) => g in f.sheets);
      if (groups.length) trimError = groups.reduce((s, g) => s + Math.abs(f.sheets[g]! - f.bestSheets![g]!), 0) / groups.length;
    }
    return {
      speedKn: speed / KNOT,
      pointOfSail: POINTS[idx === -1 ? 5 : idx]!,
      tackSide: f.twaDeg >= 0 ? 1 : -1,
      luffing: f.luffing,
      trimError,
      heelRatio: Math.abs(f.heel * DEG) / this.config.capsizeHeelDeg,
      leewayDeg: Math.atan2(f.v, Math.max(Math.abs(f.u), 1e-6)) * DEG,
      vmgUpwind: speed * Math.cos(twa / DEG),
      steerage: f.u > this.config.steerageSpeed,
      controlActivity: this.activity,
    };
  }

  private updateActivity(f: Frame, dt: number): void {
    if (!this.last || dt <= 0) return;
    let change = Math.abs(f.rudder - this.last.rudder) / 2;
    for (const g of Object.keys(f.sheets)) change += Math.abs(f.sheets[g]! - (this.last.sheets[g] ?? f.sheets[g]!));
    const rate = change / dt;
    const k = Math.min(1, dt / this.config.activityWindowSeconds);
    this.activity += (rate - this.activity) * k;
  }

  // ---- events -------------------------------------------------------------------------

  private detectTurns(f: Frame, emit: (t: string, d?: ObserverEvent['data']) => void): void {
    const twa = Math.abs(f.twaDeg);
    const m = this.config.sideMarginDeg;
    const maxSheet = Math.max(0, ...Object.values(f.sheets));
    if (twa < m) this.crossing = 'bow';
    if (twa > 180 - m) { if (this.crossing !== 'stern') this.crossingSheet = maxSheet; this.crossing = 'stern'; }
    if (twa <= m || twa >= 180 - m) return;
    const side: 1 | -1 = f.twaDeg > 0 ? 1 : -1;
    if (this.side === 0) { this.side = side; return; }
    if (side === this.side) { this.crossing = null; return; }
    const through = this.crossing ?? (twa < 90 ? 'bow' : 'stern');
    if (through === 'bow') emit('tack', { to: side > 0 ? 'starboard' : 'port' });
    else {
      const sheet = Math.max(this.crossingSheet, maxSheet);
      emit('gybe', { to: side > 0 ? 'starboard' : 'port', sheet: round(sheet) });
      emit(sheet <= this.config.gybeSheetMax ? 'gybe_controlled' : 'gybe_uncontrolled', { sheet: round(sheet) });
    }
    this.side = side;
    this.crossing = null;
  }

  private detectIrons(f: Frame, emit: (t: string) => void): void {
    const c = this.config.irons;
    const twa = Math.abs(f.twaDeg);
    if (!this.inIrons) {
      if (twa < this.config.bands[0] && f.u < c.enterSpeed) {
        this.ironsSince ??= f.t;
        if (f.t - this.ironsSince >= c.enterSeconds) { this.inIrons = true; emit('enter_irons'); }
      } else this.ironsSince = null;
    } else if (twa > c.exitAngleDeg && f.u > c.exitSpeed) {
      this.inIrons = false;
      this.ironsSince = null;
      emit('out_of_irons');
    }
  }

  private detectLuffing(f: Frame, d: Derived, emit: (t: string) => void): void {
    const c = this.config.luffing;
    const steady = Math.abs(f.r * DEG) < c.steadyYawDegS;
    if (!this.luffingOn) {
      if (d.luffing > c.start && steady && !this.inIrons) {
        this.luffSince ??= f.t;
        if (f.t - this.luffSince >= c.startSeconds) { this.luffingOn = true; this.luffClearSince = null; emit('luffing_start'); }
      } else this.luffSince = null;
    } else if (d.luffing < c.stop) {
      this.luffClearSince ??= f.t;
      if (f.t - this.luffClearSince >= c.stopSeconds) { this.luffingOn = false; this.luffSince = null; emit('luffing_stop'); }
    } else this.luffClearSince = null;
  }

  private detectHeel(d: Derived, emit: (t: string) => void): void {
    if (d.heelRatio >= 1 && !this.capsized) { this.capsized = true; emit('capsize'); }
    if (d.heelRatio > this.config.heelWarning && !this.heelWarned) { this.heelWarned = true; emit('heel_warning'); }
    if (d.heelRatio < this.config.heelRearm) { this.heelWarned = false; this.capsized = false; }
  }

  private detectWind(f: Frame, emit: (t: string) => void): void {
    const g = this.config.gust;
    const recent = this.history.filter((s) => s.t >= f.t - g.windowSeconds);
    const minSpeed = Math.min(...recent.map((s) => s.windSpeed));
    if (minSpeed > 0 && f.windSpeed > minSpeed * (1 + g.rise)) {
      if (this.gustArmed) { emit('gust'); this.gustArmed = false; this.gustUntil = f.t + g.windowSeconds; }
    } else if (f.t > this.gustUntil) this.gustArmed = true;

    const s = this.config.shift;
    const dirs = this.history.filter((x) => x.t >= f.t - s.windowSeconds).map((x) => angleDiff(x.windFrom, f.windFromDeg));
    const spread = Math.max(...dirs.map(Math.abs));
    if (spread >= s.deg) {
      if (this.shiftArmed) { emit('wind_shift'); this.shiftArmed = false; this.shiftUntil = f.t + s.windowSeconds; }
    } else if (f.t > this.shiftUntil) this.shiftArmed = true;
  }

  private detectPointOfSail(f: Frame, d: Derived, emit: (t: string, data?: ObserverEvent['data']) => void): void {
    if (d.pointOfSail !== this.posCandidate) { this.posCandidate = d.pointOfSail; this.posSince = f.t; }
    if (this.posCandidate !== this.pos && f.t - this.posSince >= this.config.pointOfSailHoldSeconds) {
      const from = this.pos;
      this.pos = this.posCandidate;
      if (from) emit('point_of_sail_change', { from, to: this.pos });
    }
  }

  private detectSteadyLeg(f: Frame, emit: (t: string) => void): void {
    const c = this.config.steadyLeg;
    if (!this.legStart || Math.abs(angleDiff(this.legStart.heading * DEG, f.heading * DEG)) > c.headingDeg) {
      this.legStart = { t: f.t, heading: f.heading };
      this.legReported = false;
      return;
    }
    if (!this.legReported && f.t - this.legStart.t >= c.seconds) { this.legReported = true; emit('steady_leg'); }
  }

  private detectContext(f: Frame, emit: (t: string) => void): void {
    const c = f.context;
    if (!c) return;
    if (c.aground && !this.aground) emit('aground');
    if (!c.aground && this.aground) emit('refloat');
    this.aground = !!c.aground;
    if (c.collision) emit('collision');
    if (c.timeToContact !== undefined && c.timeToContact < this.config.challenge.closeQuarters.timeToContact && !c.aground) {
      // near_vessel is raised by the game (it knows what is near); here only the load counts.
    }
    const near = c.distanceToTarget !== undefined && c.approachDistance !== undefined && c.distanceToTarget < c.approachDistance;
    if (near && !this.approaching) emit('approach_target');
    this.approaching = near;
    if (c.arrived) emit('arrive');
    if (c.timeLeft !== undefined) {
      if (c.timeLeft <= this.config.timerWarningSeconds && c.timeLeft > 0 && !this.timerWarned) { this.timerWarned = true; emit('timer_warning'); }
      if (c.timeLeft <= 0 && !this.timerEnded) { this.timerEnded = true; emit('timer_end'); }
    }
    for (const e of c.events ?? []) emit(e);
  }

  // ---- challenge ----------------------------------------------------------------------

  private challenge(f: Frame, d: Derived): { rawLoad: number; factors: Partial<Record<ChallengeFactor, number>> } {
    const c = this.config.challenge;
    const factors: Partial<Record<ChallengeFactor, number>> = {};
    const twa = Math.abs(f.twaDeg);
    const nearAxis = twa < c.manoeuvre.nearDeg || twa > 180 - c.manoeuvre.nearDeg;
    if (nearAxis && Math.abs(f.r * DEG) > c.manoeuvre.yawDegS) factors.manoeuvre = c.manoeuvre.load;
    if (this.inIrons) factors.in_irons = c.inIrons;
    if (d.heelRatio > c.heelFrom) factors.heel = Math.min(1, 0.6 + (d.heelRatio - c.heelFrom));
    const ctx = f.context;
    if (ctx?.timeToContact !== undefined && ctx.timeToContact < c.closeQuarters.timeToContact && !ctx.aground) factors.close_quarters = c.closeQuarters.load;
    if (this.approaching) factors.approach = c.approach;
    if (ctx?.aground) factors.aground = c.aground;
    if (f.t <= Math.max(this.gustUntil, this.shiftUntil)) factors.gust_or_shift = c.gustOrShift;
    if (d.controlActivity > c.busyHands.activity) factors.busy_hands = c.busyHands.load;
    if (d.luffing > c.luffing.above) factors.luffing = c.luffing.load;
    if (ctx?.timeLeft !== undefined && ctx.timeLeft > 0 && ctx.timeLeft <= this.config.timerWarningSeconds) factors.time_pressure = c.timePressure;
    const rawLoad = Math.max(0, ...Object.values(factors));
    return { rawLoad, factors };
  }
}

/** Signed smallest difference b - a, degrees, in (-180, 180]. */
export function angleDiff(a: number, b: number): number {
  let d = (b - a) % 360;
  if (d > 180) d -= 360;
  if (d <= -180) d += 360;
  return d;
}

const round = (x: number) => Math.round(x * 100) / 100;
