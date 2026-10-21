#include <stdio.h> // printf
#include <stdlib.h> // malloc free
#include <unistd.h> // write, usleep
#include <stdbool.h>
#include <pthread.h> // mutex: init destrou lock unlock 
                    // threads: create join detach
#include <sys/time.h> //gettimeofday
#include <limits.h> // INT_MAX

// Reset code
#define RST "\033[0m"

// Bold Foreground Colors
#define BOLD_BLACK   "\033[1;30m"
#define BOLD_RED     "\033[1;31m"
#define BOLD_GREEN   "\033[1;32m"
#define BOLD_YELLOW  "\033[1;33m"
#define BOLD_BLUE    "\033[1;34m"
#define BOLD_MAGENTA "\033[1;35m"
#define BOLD_CYAN    "\033[1;36m"
#define BOLD_WHITE   "\033[1;37m"

// *** structures ***

//code more readable
typedef pthread_mutex_t t_mtx;

//IOU for compiler
typedef struct s_workspace t_workspace;

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
    t_workspace *workspace
}             t_coder;


// Container of the data
// ./coder 5 800 200 200 [5]
// WORKSPACE

typedef struct s_workspace
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
}               t_workspace;

// parsing
void parse_input(t_workspace *workspace, char **av);
