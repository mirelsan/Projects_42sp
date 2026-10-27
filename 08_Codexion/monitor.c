/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:25:23 by mirelsan          #+#    #+#             */
/*   Updated: 2026/10/26 21:25:27 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h" 

static long read_last_start(t_coder *coder)
{
    long    last;
    safe_mutex_handle(&coder->progress_mutex, LOCK);
    last = coder->last_compile_time;
    safe_mutex_handle(&coder->progress_mutex, UNLOCK);
    return (last);
}

static bool coder_done(t_workspace *ws, t_coder *coder)
{
    bool    done;
    safe_mutex_handle(&coder->progress_mutex, LOCK);
    done = coder->number_compiles >= ws->number_of_compiles_required;
    safe_mutex_handle(&coder->progress_mutex, UNLOCK);
    return (done);
}

bool    simulation_over(t_workspace *ws)
{
    bool    over;

    safe_mutex_handle(&ws->end_mutex, LOCK);
    over = ws->end_simulation;
    safe_mutex_handle(&ws->end_mutex, UNLOCK);
    return (over);
}
void   stop_simulation(t_workspace *ws)
{
    int i;

    safe_mutex_handle(&ws->end_mutex, LOCK);
    ws->end_simulation = true;
    safe_mutex_handle(&ws->end_mutex, UNLOCK);
    i = 0;
    while (i < ws->number_of_coders)
    {
        safe_mutex_handle(&ws->dongles[i].dongle, LOCK);
        pthread_cond_broadcast(&ws->dongles[i].cond);
        safe_mutex_handle(&ws->dongles[i].dongle, UNLOCK);
        i++;
    }
}

void    *monitor_routine(void *arg)
{
    t_workspace *ws;
    int         i;
    bool        all_finished;

    ws = (t_workspace *)arg;

    while(!simulation_over(ws))
    {
        all_finished = true;
        i = 0;
        while (i < ws->number_of_coders)
        {
            if (!coder_done(ws, &ws->coders[i]))
            {
                all_finished = false;
                if (get_time_ms() - read_last_start(&ws->coders[i])
                    > ws->time_to_burnout)
                {
                    stop_simulation(ws);
                    log_event(&ws->coders[i], BURNOUT);
                    return (NULL);
                }
            }
            i++;
        }
        if (all_finished)
        {
            stop_simulation(ws);
            return (NULL);
        }
        usleep(1000);
    }
    return (NULL);
}

