/*
 * ROAD WORKS CONTROLLER
 * == LTL properties ==
 * 
 * Logic and Model Checking
 * Fall 2021
 */
 
/* 
 * Required properties
 */
 
ltl pA { [](!(W_LIGHT && E_LIGHT)) }
 
ltl pB { [](
			(W_LIGHT -> (<>(!W_LIGHT))) &&
			(E_LIGHT -> (<>(!E_LIGHT)))) }

ltl pC { [](on_lane ->(<>(!on_lane))) }

ltl pD { []((W_LIGHT && on_lane) -> (!E_LIGHT)U(!on_lane) }

ltl pE { [](at_w -> <>(W_LIGHT) }

/*
 * Additional optional properties
 */