/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:24:19 by mirelsan          #+#    #+#             */
/*   Updated: 2026/10/26 21:24:24 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

// FIFO = key is the order of arrive
// EDF = the key is the deadline, last_compile_time + time_to_burnout.

static t_request    make_request(t_coder *coder, t_dongle *dongle,
        t_workspace *ws)
{
    t_request   req;

    req.coder = coder;
    req.seq = dongle->next_seq;
    dongle->next_seq++;
    req.key = req.seq;
    if (ws->scheduler == SCHEDULER_EDF)
    {
        safe_mutex_handle(&coder->progress_mutex, LOCK);
        req.key = coder->last_compile_time + ws->time_to_burnout;
        safe_mutex_handle(&coder->progress_mutex, UNLOCK);
    }
    return (req);
}
static bool is_top(t_coder *coder, t_dongle *dongle)
{
    return (heap_peek(&dongle->queue).coder == coder);
}

static bool my_turn(t_coder *coder, t_dongle *dongle, long now)
{
    bool    is_free;
    bool    cooldown_over;
    bool    top;

    is_free = !dongle->in_use;
    cooldown_over = now >= dongle->available_at;
    top = is_top(coder, dongle);
    return (is_free && cooldown_over && top);
}

static void wait_for_turn(t_coder *coder, t_dongle *dongle, t_workspace *ws)
{
    long now;
    long wait;

    now = get_time_ms();
    while(!simulation_over(ws) && !my_turn(coder, dongle, now))
    {
        if (!dongle->in_use && is_top(coder, dongle))
        {
            wait = dongle->available_at - now;
            safe_mutex_handle(&dongle->dongle, UNLOCK);
            usleep(wait * 1000);
            safe_mutex_handle(&dongle->dongle, LOCK);
        }
        else
            pthread_cond_wait(&dongle->cond, &dongle->dongle);
        now = get_time_ms();
    }
}

void    release_dongle(t_dongle *dongle, long cooldown)
{
    safe_mutex_handle(&dongle->dongle, LOCK);
    dongle->in_use = false;
    dongle->available_at = get_time_ms() + cooldown;
    pthread_cond_broadcast(&dongle->cond);
    safe_mutex_handle(&dongle->dongle, UNLOCK);
}

bool   take_dongle(t_coder *coder, t_dongle *dongle)
{
    t_workspace *ws;

    ws = coder->workspace;
    safe_mutex_handle(&dongle->dongle, LOCK);
    heap_push(&dongle->queue, make_request(coder, dongle, ws));
    wait_for_turn(coder, dongle, ws);

    if (simulation_over(ws))
    {
        safe_mutex_handle(&dongle->dongle, UNLOCK);
        return (false);
    }
    heap_pop(&dongle->queue);
    dongle->in_use = true;
    safe_mutex_handle(&dongle->dongle, UNLOCK);
    return (true);
}
