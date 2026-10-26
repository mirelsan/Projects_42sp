#include "coders.h"

// Aqui vão o ciclo de pegar, compilar, soltar, depurar e refatorar.

void *coder_routine(void *arg)
{
    t_coder     *coder;
    t_workspace *ws;

    coder = (t_coder *)arg;
    ws = coder->workspace;

    while (coder->number_compiles < ws->number_of_compiles_required)
    {

        coder = (t_coder *)arg;
        ws = coder->workspace;
        take_dongle(coder->first_dongle);
        log_event(coder, TAKE_DONGLE);
        take_dongle(coder->second_dongle);
        log_event(coder, TAKE_DONGLE);
        mark_compile_start(coder);
        log_event(coder, COMPILING);
        usleep(ws->time_to_compile * 1000);
        count_compile(coder);
        release_dongle(coder->second_dongle, ws->dongle_cooldown);
        release_dongle(coder->first_dongle, ws->dongle_cooldown);
        log_event(coder, DEBUGGING);
        usleep(ws->time_to_debug * 1000);
        log_event(coder, REFACTORING);
        usleep(ws->time_to_refactor * 1000);
    }
    return(NULL);
}
static void mark_compile_start(t_coder *coder)
{
    safe_mutex_handle(&coder->progress_mutex, LOCK);
    coder->last_compile_time = get_time_ms();
    safe_mutex_handle(&coder->progress_mutex, UNLOCK);
}