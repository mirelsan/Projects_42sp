#include "coders.h"

void    release_dongle(t_dongle *dongle, long cooldown)
{
    safe_mutex_handle(&dongle->dongle, LOCK);
    dongle->in_use = false;
    dongle->available_at = get_time_ms() + cooldown;
    pthread_cond_broadcast(&dongle->cond);
    safe_mutex_handle(&dongle->dongle, UNLOCK);
}

bool   take_dongle(t_dongle *dongle, t_workspace *ws)
{
    long now;
    long wait;

    safe_mutex_handle(&dongle->dongle, LOCK);
    now = get_time_ms();
    while (!simulation(ws)
        && (dongle->in_use || now < dongle->available_at))
    {
        if (dongle->in_use)
            pthread_cond_wait(&dongle->cond, &dongle->dongle);
        else
        {
            wait = dongle->available_at - now;
            safe_mutex_handle(&dongle->dongle, UNLOCK);
            usleep(wait * 1000);
            safe_mutex_handle(&dongle->dongle, LOCK);
        }
        now = get_time_ms();
    }
    if (simulation_over(ws))
    {
        safe_mutex_handle(&dongle->dongle, UNLOCK);
        return (false);
    }
    dongle->in_use = true;
    safe_mutex_handle(&dongle->dongle, UNLOCK);
    return (true)
}