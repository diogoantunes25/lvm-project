bool a, b, c;

ltl p1 { <>([]c) }
ltl p2 { [](<>c) }
ltl p3 { (X (!c)) -> (X X c) }
ltl p4 { [](a) }
ltl p5 { a U [](b || c) }

proctype P(){
	atomic{
		if
		:: true -> goto s1
		:: true -> goto s2
		fi
	};
s1: atomic{
		a = true;  b = false; c = false;
		if
		:: true -> goto s3
		:: true -> goto s4
		fi
	};
s2: atomic{
		a = false; b = false; c = true;
		goto s4
	};
s3: atomic{
		a = false; b = true;  c = true;
		goto s4
	};
s4: atomic{
		a = false; b = true;  c = false;
		if
		:: true -> goto s2
		:: true -> goto s3
		:: true -> goto s5
		fi
	};
s5: atomic{
		a = true;  b = true;  c = true;
		if
		:: true -> goto s4
		:: true -> goto s5
		fi
	}
}

init {
	run P()
}