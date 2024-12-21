#include "ex1-temporal-logic-ltl.pml"

bool a, b, c;

/* We add the variable clock, which alternates from false to true in
states with connections to themselves to avoid unconditional self-loops.
To minimize the state explosion, when we are not in states with connections
to themselves, the clock is always false. */
bool clock = false;

#define L1 a = true ; b = false; c = false
#define L2 a = false; b = false; c = true
#define L3 a = false; b = true ; c = true
#define L4 a = false; b = true ; c = false
#define L5 a = true ; b = true ; c = true

active proctype P(){
	atomic{
		if
		:: true -> L1; goto s1
		:: true -> L2; goto s2
		fi
	};
s1: atomic{
		if
		:: true -> L3; goto s3
		:: true -> L4; goto s4
		fi
	};
s2: atomic{
		L4; goto s4
	};
s3: atomic{
		L4; goto s4
	};
s4: atomic{
		if
		:: true -> L2; goto s2
		:: true -> L3; goto s3
		:: true -> L5; goto s5
		fi
	};
s5: atomic{
		clock = !clock;
		if
		:: true -> L4; clock = false; goto s4
		:: true -> L5; goto s5
		fi
	}
}
