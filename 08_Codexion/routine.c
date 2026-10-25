#include "coders.h"

// Aqui vão o ciclo de pegar, compilar, soltar, depurar e refatorar.

void *coder_routine(void *arg)
{
    t_coder     *coder;
    t_workspace *ws;

    coder = (t_coder *)arg;
    ws = coder->workspace;
    safe_mutex_handle(&coder->first_dongle->dongle, LOCK);
    log_event(coder, TAKE_DONGLE);
    safe_mutex_handle(&coder->second_dongle->dongle, LOCK);
    log_event(coder, TAKE_DONGLE);
    log_event(coder, COMPILING);
    usleep(ws->time_to_compile * 1000);
    safe_mutex_handle(&coder->second_dongle->dongle, UNLOCK);
    safe_mutex_handle(&coder->first_dongle->dongle, UNLOCK);
    return (NULL);
}

int main(void)
{
    pthread_t   thread;
    t_dongle    
}