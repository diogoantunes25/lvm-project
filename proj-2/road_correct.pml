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

#define WEST 0
#define EAST 1

mtype = {all_stop1, all_stop2, w1, w2, e1, e2}

chan reset = [0] of {bit};
chan start = [0] of {bit}
byte time = 0;
bool at_w = false, at_e = false;
bool on_lane = false;
bool turn = WEST;
mtype state = all_stop1;

/* 
 *     == Sensors and timer ==
 *
 * These processes shouyld not be modified
 */
 
proctype w_sensor () {
end: do
     :: do    
        :: atomic{ at_w = true; break }
        :: true -> skip
        od; 
        atomic{ W_LIGHT; at_w = false }
     od    
}

proctype e_sensor () {

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
     :: atomic{(W_LIGHT || E_LIGHT); on_lane = true};
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
     :: state == all_stop1 && at_w && (turn = WEST || !at_e) -> atomic{ state = w1; turn = EAST; start ! 0 }
     :: state == w1 && on_lane -> state = w2
     :: state == w1 && time_out -> state = all_stop2 
     :: state == w2 && (!on_lane || time_out) -> atomic{ state = all_stop2 } 
     :: state == all_stop1 && at_e && (turn = EAST || !at_w) -> atomic{ state = e1; turn = WEST; start ! 0}
     :: state == e1 && on_lane -> state = e2
     :: state == e1 && time_out -> state = all_stop2 
     :: state == e2 && (!on_lane || time_out) -> state = all_stop2 
     :: state == all_stop2 && !on_lane -> atomic{state = all_stop1; reset ! 0}
     od
}

init {
    atomic { run timer(); run controler(); run w_sensor(); run e_sensor(); run l_sensor() }
}


/*
 *  == LTL properties ==
 */

#include "road_ltl.pml"