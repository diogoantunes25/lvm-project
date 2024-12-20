// States can be identitied by propositional symbols that are true (in this case)
bit a = 1, b = 0, c = 0; // default to state 1, but it's not correct

// Check state
#define s1 (a == 1 && b == 0 && c == 0)
#define s2 (a == 0 && b == 0 && c == 1)
#define s3 (a == 0 && b == 1 && c == 1)
#define s4 (a == 0 && b == 1 && c == 0)
#define s5 (a == 1 && b == 1 && c == 1)

// Change state
#define m1 d_step {a = 1 ; b = 0 ; c = 0}
#define m2 d_step {a = 0 ; b = 0 ; c = 1}
#define m3 d_step {a = 0 ; b = 1 ; c = 1}
#define m4 d_step {a = 0 ; b = 1 ; c = 0}
#define m5 d_step {a = 1 ; b = 1 ; c = 1}

// ltl pi        { <>[]c }
// ltl pii       { []<>c }

// FIXME:
// ltl piii         { (X(!c)) -> (X(X(c))) }

// ltl piv          { []a }
// ltl pv           { a U [](b || c) }

active proctype TransitionSystem() {

  // Pick initial state
  if
  :: true -> m1
  :: true -> m2
  fi

  do
  :: s1 ->
    if
    :: true -> m3
    :: true -> m4
    fi
  :: s2 -> m4
  :: s3 -> m4
  :: s4 ->
    if
    :: true -> m2
    :: true -> m3
    :: true -> m5
    fi
  :: s5 ->
    if
    :: true -> m4
    :: true -> m5
    fi
  od
}
