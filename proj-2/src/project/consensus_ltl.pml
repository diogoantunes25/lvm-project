/*
 *     EXERCISE 3
 *  Consensus Protocol LTL properties
 *
 * G08 (ist199240, ist198973, ist199210)
*/

// (for reliable only) memory limit set to 8000 and -O2 -DNFAIR=3 -DCOLLAPSE as compiler flags
ltl agreement { [] (done -> sameOutputs)}

// (for reliable only) memory limit set to 8000 and -O2 -DNFAIR=3 -DCOLLAPSE as compiler flags
ltl validity { [] ((done && sameInputs) -> sameOutputs) }

ltl validity_strong { [] ((sameInputs && started) -> (sameVs && (done -> sameOutputs))) }

ltl termination { <>done }