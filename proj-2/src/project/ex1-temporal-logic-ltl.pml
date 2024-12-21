/*
 * (Need to put an extra X due to the system starting with a transition to
 * decide the initial state)
*/

/*
 * i. F G c
*/
ltl p1 { X <>([]c) }

/*
 * ii. G F c
*/
ltl p2 { X [](<>c) }

/*
 * iii. (X ¬c) -> (X X c)
*/
ltl p3 { X ((X (!c)) -> (X X c)) }

/*
 * iv. G a
*/
ltl p4 { X [](a) }

/*
 * v. a U G(b v c)
*/
ltl p5 { X (a U [](b || c)) }
