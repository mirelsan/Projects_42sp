#include "coders.h"

// Aqui vão o ciclo de pegar, compilar, soltar, depurar e refatorar.

void *coder_routine(void *arg)
{
    t_coder     *coder;
    t_workspace *ws;

    while (coder->number_compiles < ws->number_of_compiles_required)
    {
        coder = (t_coder *)arg;
        ws = coder->workspace;
        safe_mutex_handle(&coder->first_dongle->dongle, LOCK);
        log_event(coder, TAKE_DONGLE);
        safe_mutex_handle(&coder->second_dongle->dongle, LOCK);
        log_event(coder, TAKE_DONGLE);
        log_event(coder, COMPILING);
        usleep(ws->time_to_compile * 1000);
        coder->number_compiles++;
        safe_mutex_handle(&coder->second_dongle->dongle, UNLOCK);
        safe_mutex_handle(&coder->first_dongle->dongle, UNLOCK);
        log_event(coder, DEBUGGING);
        usleep(ws->time_to_debug * 1000);
        log_event(coder, REFACTORING);
        usleep(ws->time_to_refactor * 1000);
    }
    return(NULL);
}
