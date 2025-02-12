// #define N 4
#define N 3
#define T 1
#define c(i,j) _c[(i)*(N+T) + (j)]

// #include "consensus_ltl_n_3.pml"
#include "consensus_ltl_n_3.pml"


// c(i,j) is to send messages from i to j
// there's no point in sending values to byz
chan _c[(N+T)*(N+T)] = [T+2] of {bit};
bit inputs[N];
byte outputs[N];
byte rounds[N+T];
bit v[N];
bit started;

proctype reliable(int id) {
  bit ithMajority;
  byte zeros; // number of zeros received
  byte i;

  do
  :: rounds[id-1] > T + 1 -> break
  :: rounds[id-1] <= T + 1 ->

      // 1

      // 1.1 send its value to every other process
      d_step {
        i = 0;
        do
        :: i < N+T -> c(id-1,i) ! v[id-1]; i++;
        :: i == N+T -> break;
        od;

        i = 0;
        zeros = 0;
      };

      // 1.2 count received values
      // printf("[%d] counting received values\n", id);
      do
      :: i < N+T -> if
                    :: c(i,id-1) ? 0 -> d_step { zeros++; printf("[%d] received %d from %d\n", id, 0, i+1); i++ };
                    :: c(i,id-1) ? 1 -> d_step { printf("[%d] received %d from %d\n", id, 1, i+1); i++ };
                    fi;
      :: i == N+T -> break;
      od;

      // Part 2

      skip; // trick to avoid jumps into d_steps
      // 2.1 Node round send majority value it received
      d_step {
        i = 0;
        do
        :: i < N+T -> if
                      :: id == rounds[id-1] && (zeros > (N+T) - zeros)   -> c(id-1,i) ! 0;
                      :: id == rounds[id-1] && (zeros <= (N+T) - zeros)  -> c(id-1,i) ! 1;
                      :: else -> skip
                      fi;
                      i++
        :: i == N+T -> break;
        od;
      };

      atomic {
        // 2.2 Every node reads the sent value
        c(rounds[id-1]-1,id-1) ? ithMajority;

        d_step {
          printf("[%d] i-th majority is %d\n", id, ithMajority);

          // 2.3 If it found N with same value, then update v to that value else use ithMajority
          if
          :: zeros >= N -> v[id-1] = 0
          :: (N+T)-zeros >= N -> v[id-1] = 1
          :: else -> v[id-1] = ithMajority;
          fi;
          printf("[%d] setting v to %d\n", id, v[id-1]);
          printf("[%d] Just finished round %d\n", id, rounds[id-1]-1);
          rounds[id-1]++

          // reset variables
          ithMajority = 0;
          zeros = 0;
          i = 0;
        }
      }
  od;

  atomic {
    skip;
    d_step {
      printf("[%d] My value is %d\n", id, v[id-1]);
      outputs[id-1] = v[id-1];
    }
  }
}

proctype faulty(int id) {
  byte i;
  bit dummy;

  do
  :: rounds[id-1] > T + 1 -> break
  :: rounds[id-1]<= T + 1 ->
      // 1

      // 1.1 send some value to every other process
      atomic {
        i = 0;
        do
        :: i < N+T ->
          if
          :: true -> c(id-1,i) ! 0
          :: true -> c(id-1,i) ! 1
          fi;
          i++
        :: i == N+T -> break;
        od;
      }

      // 1.2 read values and ignore
      // nop
      do
      :: i < N+T -> atomic { c(i,id-1) ? dummy; i++ }
      :: i == N+T -> atomic { c(rounds[id-1]-1,id-1) ? dummy; rounds[id-1]++; i = 0; dummy =0; break; } // entire part 2
      od;

      // printf("[%d] Just finished round %d\n", id, round-1);
  od;

}

init {
  byte i;

  // Decide inputs for everyone
  atomic {
    i = 0;
    started = 0;
    do
    :: i < N ->  if
                  :: true -> inputs[i] = 0; printf("[%d] My input is 0\n", i+1)
                  :: true -> inputs[i] = 1; printf("[%d] My input is 1\n", i+1)
                  fi;
                  outputs[i] = 2; // some invalid output for termination
                  v[i] = inputs[i];
                  i++
    :: else -> break;
    od;


    // Start processes
    i = 1;
    do
    :: i <= N -> rounds[i-1] = 1 ; run reliable(i); i++
    :: i > N && i <= N+T -> rounds[i-1] = 1; run faulty(i); i++
    :: else -> break;
    od
    started = 1;
  };
}
