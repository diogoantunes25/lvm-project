/*
 *     EXERCISE 1
 * = LTL properties =
 *
 * G08 (ist199240, istxxxxxx, istxxxxxx)
*/


/*
 * i. F G c
*/
ltl p1 { <>([]c) }

/*
 * ii. G F c
*/
ltl p2 { [](<>c) }

/*
 * iii. (X ¬c) -> (X X c)
*/
ltl p3 { (X (!c)) -> (X X c) }

/*
 * iv. G a
*/
ltl p4 { [](a) }

/*
 * v. a U G(b v c)
*/
ltl p5 { a U [](b || c) }