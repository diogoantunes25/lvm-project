/*
 * ROAD WORKS CONTROLLER
 * == LTL properties ==
 * Logic and Model Checking
 * Fall 2021
 */

/*
 * Required properties
 */

// safety (passes)
ltl pA { []!(W_LIGHT && E_LIGHT) }

// liveness (?) (passes)
ltl pB { []((W_LIGHT -> (<>(! W_LIGHT))) && (E_LIGHT -> (<>(! E_LIGHT)))) }

// liveness (?) (passes)
ltl pC { [](on_lane -> <>(!on_lane)) }

// safety (passes)
// ltl pD { []((W_LIGHT && on_lane) -> !E_LIGHT) }

ltl pD { []((W_LIGHT && on_lane) -> (!E_LIGHT W !on_lane)) }

// combination (fails)
ltl pE { [](at_w -> <> W_LIGHT) }

/* Trace:



*/

/*
 * Additional optional properties
 */
