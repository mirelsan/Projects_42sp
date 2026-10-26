#include "coders.h"

void    *monitor_routine(void *arg)
{
    t_coder     *coder;
    t_workspace *ws;

    coder = (t_coder *)arg;
    ws = coder->workspace;

    int     i;
    long    last;
    while(1)
    {
        i = 0;
        while (i < ws->number_of_coders)
        {
            last = read_last_start(&ws->coders[i]);
            if (get_time_ms() - last > ws->dongle_cooldown)
            {
                log_event(&ws->coders[i], LATE);
                return (NULL);
            }
            i++;
        }
        usleep(1000);
    }
}