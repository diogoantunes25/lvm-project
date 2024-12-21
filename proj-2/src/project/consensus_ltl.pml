#define done (outputs[0] != 2 && outputs[1] != 2 && outputs[2] != 2 && outputs[3] != 2)

#define sameInVector(vec) (vec[0] == vec[1] && vec[1] == vec[2] && vec[2] == vec[3])
#define sameOutputs sameInVector(outputs)
#define sameInputs sameInVector(inputs)
#define sameVs sameInVector(v)

// (for reliable only) memory limit set to 8000 and -O2 -DNFAIR=3 -DCOLLAPSE as compiler flags
ltl agreement { [] (done -> sameOutputs)}

// (for reliable only) memory limit set to 8000 and -O2 -DNFAIR=3 -DCOLLAPSE as compiler flags
ltl validity { [] ((done && sameInputs) -> sameOutputs) }

ltl validity_strong { [] ((sameInputs && started) -> (sameVs && (done -> sameOutputs))) }

ltl termination { <>done }
