#include <stdio.h> // printf
#include <stdlib.h> // malloc free
#include <unistd.h> // write, usleep
#include <stdbool.h>
#include <pthread.h> // mutex: init destrou lock unlock 
                    // threads: create join detach
#include <sys/time.h> //gettimeofday
#include <limits.h> // INT_MAX

// *** structures ***

//code more readable
typedef pthread_mutex_t t_mtx;
// DONGLE

typedef struct s_dongle
{
    t_mtx dongle;
    int dongle_id;
}       t_dongle;

// CODER

typedef struct s_coder
{
    int id;
    long number_compiles;
    bool bournout;
    long last_compile_time; // time passed from last compile
    t_dongle *left_dongle;
    t_dongle *right_dongle; // coder is a thread
    pthread_t thread_id; 
}             t_coder;


// Container of the data

typedef struct s_network
{
    long    number_of_coders;
    long    time_to_burnout;
    long    time_to_compile;
    long    time_to_debug;
    long    time_to_refactor;
    long    number_of_compiles_required; // [5] | FLAG if -1
    long    dongle_cooldown;
    long    start_simulation; //
    bool    end_simulation; // a coder boutnout
    t_dongle    *dongles; // attay dongles
    t_coder     *coders; // array
}               t_network;