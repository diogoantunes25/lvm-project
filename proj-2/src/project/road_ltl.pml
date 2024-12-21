/*
 *     EXERCISE 2
 *  Road Works Controller LTL properties
 *
 * G08 (ist199240, ist198973, ist199210)
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
// ltl pD { []((W_LIGHT && on_lane) -> ((!E_LIGHT) U !on_lane )) } -> WRONG, as it states that there won't be cars in the lane (making this a liveness property)
// ltl pD { []((W_LIGHT && on_lane) -> (on_lane -> !E_LIGHT)) }
ltl pD { []((W_LIGHT && on_lane) -> !E_LIGHT) }
// equivalent to
// ltl pD { []((W_LIGHT && on_lane) -> !E_LIGHT }

// combination (fails)
ltl pE { [](at_w -> <> W_LIGHT) }

/* Trace:



*/

/*
 * Additional optional properties
 */
