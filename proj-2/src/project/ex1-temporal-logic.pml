/*
 *     EXERCISE 1
 *  Temporal Logic
 *
 * G08 (ist199240, ist198973, ist199210)
*/

// States can be identitied by propositional symbols that are true (in this case)
bit a = 1, b = 0, c = 0;
bit started = 0;

// to avoid problems with next
bit f = 0;

// Check state
#define s1 (a == 1 && b == 0 && c == 0)
#define s2 (a == 0 && b == 0 && c == 1)
#define s3 (a == 0 && b == 1 && c == 1)
#define s4 (a == 0 && b == 1 && c == 0)
#define s5 (a == 1 && b == 1 && c == 1)

// Change state
#define m1 atomic {a = 1 ; b = 0 ; c = 0 ; printf("moving to 1\n"); f = !f}
#define m2 atomic {a = 0 ; b = 0 ; c = 1 ; printf("moving to 2\n"); f = !f}
#define m3 atomic {a = 0 ; b = 1 ; c = 1 ; printf("moving to 3\n"); f = !f}
#define m4 atomic {a = 0 ; b = 1 ; c = 0 ; printf("moving to 4\n"); f = !f}
#define m5 atomic {a = 1 ; b = 1 ; c = 1 ; printf("moving to 5\n"); f = !f}

#define moved ( (f && !(X(f))) || (!f && (X(f))) )

ltl pi        { !started U (started && <>[]c) }
ltl pii       { !started U (started && []<>c) }
ltl piii         { !started U (started && ((X(!c) && moved && X(moved)) -> (X(X(c))))) }
ltl piv          { !started U (started && []a) }
ltl pv           { !started U (started && (a U [](b || c))) }

active proctype TransitionSystem() {

  // Pick initial state
  if
  :: true -> m1
  :: true -> m2
  fi;

  printf("starting\n");
  started = 1;

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
