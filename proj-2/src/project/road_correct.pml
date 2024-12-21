/*
 *     EXERCISE 2
 *  Road Works Controller corrected
 *
 * G08 (ist199240, ist198973, ist199210)
*/

#define TIME_LIMIT 3
#define time_out (time == TIME_LIMIT)

#define W_LIGHT (state == w1 || state == w2)
#define E_LIGHT (state == e1 || state == e2)

mtype = {all_stop1, all_stop2, w1, w2, e1, e2}

chan reset = [0] of {bit};
chan start = [0] of {bit};
byte time = 0;
bool at_w = false, at_e = false;
bool on_lane = false;
bool westWasLast = 0; // give priority
mtype state = all_stop1;

/*
 *     == Sensors and timer ==
 *
 * These processes should not be modified
 */

proctype w_sensor () {

// put someone at the intersection and wait for start of movement
end: do
     :: do
        :: atomic{ at_w = true; break }
        :: true -> skip
        od;
        atomic{ W_LIGHT; at_w = false }
     od
}

proctype e_sensor () {

// put someone at the intersection and wait for start of movement
end: do
     :: do
        :: atomic{ at_e = true; break }
        :: true -> skip
        od;
        atomic{ E_LIGHT;  at_e = false }
     od
}

proctype l_sensor () {

end: do
     :: // wait for a light to turn on and move to the lane
        atomic{(W_LIGHT || E_LIGHT); on_lane = true};
        // wait for one of the following
        // (1) lights go off (probably due to timeout)
        // (2) person no longer at intersection and remove person from lane
        atomic{(!W_LIGHT && !E_LIGHT) || (W_LIGHT && !at_w) || (E_LIGHT && !at_e);  on_lane = false}
     od
}

proctype timer() {
    bool running = false;

end: do
     :: reset ? 0 -> d_step{ time = 0; running = false}
     :: start ? 0 -> running = true
     :: running && time < TIME_LIMIT -> time++
     od
}

/*
 *      == Controller ==
 *
 * This is the only process that can be modified.
 */
proctype controler () {

end: do
   // if system is stopped and there someone in the side, start time and start the movement of that person (turning on the ligth)
   :: state == all_stop1 && at_w && (!at_e || !westWasLast) -> atomic{ state = w1; start ! 0; westWasLast = true; printf("started movement of west\n") }
   :: state == all_stop1 && at_e && (!at_w || westWasLast ) -> atomic{ state = e1; start ! 0; westWasLast = false; printf("started movement of east\n") }

   // if it's on progress, but timed out, stop everything
   :: state == w1 && time_out -> atomic { state = all_stop2; printf("movement of west timed out\n") }
   :: state == e1 && time_out -> atomic { state = all_stop2; printf("movement of east timed out\n") }

   // once the lane is cleared after the stop, reset
   :: state == all_stop2 && !on_lane -> atomic{ state = all_stop1; reset ! 0; printf("resetting\n") }

   // puts person on lane
   :: state == w1 && on_lane -> atomic { state = w2; printf("putting west on lane\n") }
   :: state == e1 && on_lane -> atomic { state = e2; printf("putting east on lane\n") }

   // stops once timeout or if the person went through the shared lane
   :: state == w2 && (!on_lane || time_out) -> atomic { state = all_stop2; printf("done with movement of west\n") }
   :: state == e2 && (!on_lane || time_out) -> atomic { state = all_stop2; printf("done with movement of east\n") }

   od
}

init {
    atomic { run timer(); run controler(); run w_sensor(); run e_sensor(); run l_sensor() }
}

/**

started movement of east
movement of east timed out
resetting
started movement of east
putting east on lane
done with movement of west
resetting
started movement of east
putting east on lane
done with movement of west
resetting
started movement of east
putting east on lane
done with movement of west
resetting
started movement of east
putting east on lane
done with movement of west
resetting
started movement of east
putting east on lane
done with movement of west
<<<<<START OF CYCLE>>>>>
resetting
started movement of east
movement of east timed out
resetting
started movement of east
putting east on lane
done with movement of east
resetting
started movement of east
putting east on lane
done with movement of east
resetting
started movement of east
putting east on lane
done with movement of east
resetting
started movement of east
putting east on lane
done with movement of east
**/

/*
 *  == LTL properties ==
 */

#include "road_ltl.pml"
