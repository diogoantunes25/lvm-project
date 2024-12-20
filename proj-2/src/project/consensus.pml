#define N 4
#define T 1
#define c(i,j) _c[(i)*(N+T) + (j)]

#define done (outputs[0] != 2 && outputs[1] != 2 && outputs[2] != 2 && outputs[3] != 2)

#define sameInVector(vec) (vec[0] == vec[1] && vec[1] == vec[2] && vec[2] == vec[3])
#define sameOutputs sameInVector(outputs)
#define sameInputs sameInVector(inputs)
#define sameVs sameInVector(v)

// (for reliable only) memory limit set to 8000 and -O2 -DNFAIR=3 -DCOLLAPSE as compiler flags
ltl agreement { [] (done -> sameOutputs)}

// (for reliable only) memory limit set to 8000 and -O2 -DNFAIR=3 -DCOLLAPSE as compiler flags
ltl validity { [] ((done && sameInputs) -> sameOutputs) }

ltl validity_strong { [] ((sameInputs && started) -> (sameVs && (done -> sameOutputs))) }

ltl termination { <>done }

// c(i,j) is to send messages from i to j
// there's no point in sending values to byz
// chan _c[(N+T)*(N+T)] = [1] of {bit};
// FIXME: get tighter bound
chan _c[(N+T)*(N+T)] = [(T+1)*2] of {bit};
bit inputs[N];
bit outputs[N];
bit v[N];
bit started = 0;

proctype reliable(int id) {
  v[id-1] = inputs[id-1];
  bit ithMajority;
  byte zeros; // number of zeros received
  byte i;
  printf("[%d] starting with value = %d\n", id, v[id-1])
  byte round = 1;
  do
  :: round > T + 1 -> break
  :: round <= T + 1 ->
      // printf("[%d] on round %d\n", id, round);

      // 1

      // 1.1 send its value to every other process
      atomic {
        i = 0;
        do
        :: i < N+T -> c(id-1,i) ! v[id-1]; i++;
        :: i == N+T -> break;
        od;
      };

      // 1.2 count received values
      // printf("[%d] counting received values\n", id);
      i = 0;
      zeros = 0;
      do
      :: i < N+T -> if
                    :: c(i,id-1) ? 0 -> zeros++; printf("[%d] received %d from %d\n", id, 0, i);
                    :: c(i,id-1) ? 1 -> skip; printf("[%d] received %d from %d\n", id, 1, i);
                    fi;
                    i++
      :: i == N+T -> break;
      od;
      // printf("[%d] got %d zeros and %d ones\n", id, zeros, N+T-zeros);

      // Part 2

      // 2.1 Node round send majority value it received
      atomic {
        i = 0;
        do
        :: i < N+T -> if
                      :: id == round && (zeros > (N+T) - zeros)   -> c(id-1,i) ! 0;
                      :: id == round && (zeros <= (N+T) - zeros)  -> c(id-1,i) ! 1;
                      :: else -> skip
                      fi;
                      i++
        :: i == N+T -> break;
        od;
      };

      atomic {
        // 2.2 Every node reads the sent value
        c(round-1,id-1) ? ithMajority;
        printf("[%d] i-th majority is %d\n", id, ithMajority);

        // 2.3 If it found N with same value, then update v to that value else use ithMajority
        if
        :: zeros >= N -> v[id-1] = 0
        :: (N+T)-zeros >= N -> v[id-1] = 1
        :: else -> v[id-1] = ithMajority;
        fi;
        printf("[%d] setting v to %d\n", id, v[id-1]);
        round++
      }
  od;

  atomic {
    printf("[%d] My value is %d\n", id, v[id-1]);
    outputs[id-1] = v[id-1];
  }
}

proctype faulty(int id) {
  byte round = 1;
  byte i;
  bit dummy;
  do
  :: round > T + 1 -> break
  :: round <= T + 1 ->
      // 1

      // 1.1 send some value to every other process
      atomic {
        i = 0;
        do
        :: i < N ->
          if
          :: true -> c(id-1,i) ! 0
          :: true -> c(id-1,i) ! 1
          fi;
          i++
        :: i == N -> break;
        od;

        i = 0
      };


        // 1.2 read values and ignore
        // nop
      do
      :: i < N+T -> atomic { c(i,id-1) ? dummy; i++ }
      :: i == N+T -> atomic { c(round-1,id-1) ? dummy; round++; break; } // entire part 2
      od;
  od;

}

init {
  byte i;

  // Decide inputs for everyone
  i = 0;
  do
  :: i < N ->  if
                :: true -> inputs[i] = 0; v[i] = 0; printf("[%d] My input is 0\n", i)
                :: true -> inputs[i] = 1; v[i] = 1; printf("[%d] My input is 1\n", i)
                fi;
                outputs[i] = 2; // some invalid output for termination
                i++
  :: else -> break;
  od;

  // Start processes
  atomic {
    i = 1;
    do
    :: i <= N -> run reliable(i); i++
    :: i > N && i <= N+T -> run faulty(i); i++
    :: else -> break;
    od
    started = 1;
  };
}
