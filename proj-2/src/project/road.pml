/*
 *   ROAD WORKS CONTROLLER
 *
 * Logic and Model Checking
 * Fall 2021
 */

#define TIME_LIMIT 3
#define time_out (time == TIME_LIMIT)

#define W_LIGHT (state == w1 || state == w2)
#define E_LIGHT (state == e1 || state == e2)

mtype = {all_stop1, all_stop2, w1, w2, e1, e2}

chan reset = [0] of {bit};
chan start = [0] of {bit}
byte time = 0;
bool at_w = false, at_e = false;
bool on_lane = false;
mtype state = all_stop1;

/*
 *     == Sensors and timer ==
 *
 * These processes shouyld not be modified
 */

proctype w_sensor () {
end: do
     :: do
        :: atomic{ at_w = true; printf("[dsastep] Someone at west\n"); break }
        :: true -> skip
        od;
        atomic{ W_LIGHT; at_w = false; printf("[dsastep] No one at west\n"); }
     od
}

proctype e_sensor () {

end: do
     :: do
        :: atomic{ at_e = true; printf("[dsastep] Someone at east\n"); break }
        :: true -> skip
        od;
        atomic{ E_LIGHT;  at_e = false; printf("[dsastep] No one at east\n"); }
     od
}

proctype l_sensor () {

end: do
     :: atomic{(W_LIGHT || E_LIGHT); on_lane = true; printf("[dsastep] someone at lane\n")};
        atomic{(!W_LIGHT && !E_LIGHT) || (W_LIGHT && !at_w) || (E_LIGHT && !at_e); on_lane = false; printf("[dsastep] no one at lane\n"); }
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
     :: state == all_stop1 && at_w -> atomic{ state = w1;start ! 0; printf("[dsastep] controller 1\n"); }
     :: state == w1 && on_lane -> atomic { state = w2; printf("[dsastep] controller 2\n"); }
     :: state == w1 && time_out -> atomic { state = all_stop2; printf("[dsastep] controller 3\n"); }
     :: state == w2 && (!on_lane || time_out) -> atomic{ state = all_stop2; printf("[dsastep] controller 4\n"); }
     :: state == all_stop1 && at_e -> atomic{ state = e1; start ! 0; printf("[dsastep] controller 5\n"); }
     :: state == e1 && on_lane -> atomic { state = e2; printf("[dsastep] controller 6\n"); }
     :: state == e1 && time_out -> atomic{ state = all_stop2; printf("[dsastep] controller 7\n"); }
     :: state == e2 && (!on_lane || time_out) -> atomic { state = all_stop2; printf("[dsastep] controller 8\n"); }
     :: state == all_stop2 && !on_lane -> atomic{state = all_stop1; reset ! 0; printf("[dsastep] controller 9\n"); }
     od
}

init {
    atomic { run timer(); run controler(); run w_sensor(); run e_sensor(); run l_sensor() }
}


/*
 *  == LTL properties ==
 */

#include "road_ltl.pml"
