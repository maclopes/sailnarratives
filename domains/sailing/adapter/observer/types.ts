// What the observer reads each step (a Frame) and what it reports (an Observation).
// Game-agnostic: fromSim() in adapter.ts builds a Frame from fragateiro's simulator.

/** Mission facts the physics does not know (all optional). */
export interface FrameContext {
  aground?: boolean;
  /** True on the step a collision happens. */
  collision?: boolean;
  /** Distance to the mission's current target (port, buoy, boat, whale), m. */
  distanceToTarget?: number;
  /** Distance under which the mission counts as an approach, m. */
  approachDistance?: number;
  /** Seconds to the nearest land, boat or target at the current closing speed. */
  timeToContact?: number;
  /** Seconds left on a timed task. */
  timeLeft?: number;
  /** Mission goal reached on this step. */
  arrived?: boolean;
  /** Mission-specific events raised by the game on this step (e.g. whale_close, catch). */
  events?: string[];
}

export interface Frame {
  /** Game time, s. */
  t: number;
  /** Compass heading, rad. */
  heading: number;
  /** Forward and sideways speed through the water, m/s. */
  u: number;
  v: number;
  /** Yaw rate, rad/s. */
  r: number;
  /** Heel, rad. */
  heel: number;
  /** -1..1 */
  rudder: number;
  /** Sheet per sail group, 0 hauled in .. 1 eased. */
  sheets: Record<string, number>;
  /** Ideal sheet per group (fragateiro: SailboatSim.bestSheets()). */
  bestSheets?: Record<string, number>;
  /** True wind angle off the bow, deg (+ = from starboard). */
  twaDeg: number;
  /** Apparent wind angle off the bow, deg, and speed, m/s. */
  awaDeg: number;
  aws: number;
  /** True wind: direction it blows from (deg, compass) and speed (m/s). */
  windFromDeg: number;
  windSpeed: number;
  /** Share of active sails that are luffing, 0..1. */
  luffing: number;
  mode: string;
  boat: string;
  context?: FrameContext;
}

export type PointOfSail = 'in_irons' | 'close_hauled' | 'close_reach' | 'beam_reach' | 'broad_reach' | 'running';

export interface Derived {
  speedKn: number;
  pointOfSail: PointOfSail;
  /** +1 starboard tack (wind from starboard), -1 port tack. */
  tackSide: 1 | -1;
  luffing: number;
  /** Mean |sheet - best sheet| over groups, 0 = ideal; undefined without bestSheets. */
  trimError?: number;
  heelRatio: number;
  leewayDeg: number;
  vmgUpwind: number;
  steerage: boolean;
  /** Rudder and sheet movement per second, smoothed. */
  controlActivity: number;
}

export interface ObserverEvent {
  type: string;
  t: number;
  /** Small facts about the event, e.g. { sheet: 0.9 } for a gybe. */
  data?: Record<string, number | string | boolean>;
}

export type ChallengeFactor =
  | 'manoeuvre' | 'in_irons' | 'heel' | 'close_quarters' | 'approach' | 'aground'
  | 'gust_or_shift' | 'busy_hands' | 'luffing' | 'time_pressure';

export interface Observation {
  t: number;
  derived: Derived;
  events: ObserverEvent[];
  /** Raw load this step (largest active factor), 0..1. */
  rawLoad: number;
  /** Load after the slow decay: what the scheduler uses. */
  load: number;
  factors: Partial<Record<ChallengeFactor, number>>;
  /** In a calm window: load low for long enough on a steady heading. */
  calm: boolean;
  /** Seconds the current calm window has lasted (0 when not calm). */
  calmFor: number;
}
