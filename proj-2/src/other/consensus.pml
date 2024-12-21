/*
 *     EXERCISE 3
 *  Consensus Protocol
 *
 * G08 (ist199240, ist198973, istxxxxxx)
*/

#define N 4        // Number of reliable processes
#define T 1        // Number of faulty processes

#define N_PROCESSES (N + T)    // Number of processes
#define N_ROUNDS (T + 1)       // Number of rounds

mtype = {phase1, phase2};      // Protocol phases

// Communication channels for messages =    {phase, round, value}
chan channels[N_PROCESSES] = [2 * N_PROCESSES] of {mtype, int, bit};

proctype process(int id) {
    int round = 1;              // Current round
    int round_read;             // To read messages content
    int channel = 0;            // Channels iterator
    int count[2];               // Received values counter
    bit v;                      // Current process value
    bit v_read;                 // To read messages content
    bit v_majority;             // Majority value
    bool is_faulty = (id > N);  // Indicates if process is faulty

    if // Randomly select a value
    :: true -> v = 0
    :: true -> v = 1
    fi;

    do
    :: (round <= N_ROUNDS) ->
        // Clear counter
        count[0] = 0;
        count[1] = 0;

        // Phase 1
        do // Send value to all processes
        :: (channel < N_PROCESSES) ->
            if // Faulty processes randomly change their value
            :: is_faulty ->
                if
                :: true -> v = 0
                :: true -> v = 1
                fi
            :: else -> skip   
            fi;
            atomic { channels[channel] ! phase1, round, v };
            channel++
        :: else -> break
        od;

        do // Receive values from all processes
        :: (channel > 0) ->
            channels[id-1] ? phase1, round_read, v_read;
            if
            :: round == round_read ->
                count[v_read]++;
                channel--
            :: else -> skip
            fi
        :: else -> break    
        od;

        // Phase 2
        if // Process with id equal to the round number sends majority value to all processes
        :: id == round ->
            v_majority = (count[0] > count[1] -> 0 : 1);
            do
            :: (channel < N_PROCESSES) ->
                atomic { channels[channel] ! phase2, round, v_majority };
                channel++
            :: else -> break    
            od
        :: else -> skip
        fi;

        if // Update value
        :: count[0] >= N -> v = 0
        :: count[1] >= N -> v = 1
        :: else ->
            channels[id-1] ? phase2, round_read, v_read;
            if
            :: round == round_read ->
                v = v_read
            :: else -> skip
            fi
        fi;

        round++
    :: else -> break    
    od
}

init {
    int i = 1;
    do
    :: (i <= N_PROCESSES) ->
        run process(i);
        i++
    :: else -> break    
    od
}