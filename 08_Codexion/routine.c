/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:25:56 by mirelsan          #+#    #+#             */
/*   Updated: 2026/10/26 21:25:57 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "coders.h"
// Aqui vão o ciclo de pegar, compilar, soltar, depurar e refatorar.

static void mark_compile_start(t_coder *coder)
{
    safe_mutex_handle(&coder->progress_mutex, LOCK);
    coder->last_compile_time = get_time_ms();
    safe_mutex_handle(&coder->progress_mutex, UNLOCK);
}

static void count_compile(t_coder *coder)
{
    safe_mutex_handle(&coder->progress_mutex, LOCK);
    coder->number_compiles++;
    safe_mutex_handle(&coder->progress_mutex, UNLOCK);
}

static bool get_both_dongles(t_coder *coder)
{

    if (!take_dongle(coder, coder->first_dongle))
        return (false);
    log_event(coder, TAKE_DONGLE);
    if (!take_dongle(coder, coder->second_dongle))
    {
        release_dongle(coder->first_dongle, 0);
        return (false);
    }
    log_event(coder, TAKE_DONGLE);
    return (true);
}

static void do_compile(t_coder *coder)
{
    t_workspace *ws;

    ws = coder->workspace;
    mark_compile_start(coder);
    log_event(coder, COMPILING);
    usleep(ws->time_to_compile * 1000);
    count_compile(coder);
    release_dongle(coder->second_dongle, ws->dongle_cooldown);
    release_dongle(coder->first_dongle, ws->dongle_cooldown);
}

void *coder_routine(void *arg)
{
    t_coder     *coder;
    t_workspace *ws;

    coder = (t_coder *)arg;
    ws = coder->workspace;

    while (!simulation_over(ws)
        && coder->number_compiles < ws->number_of_compiles_required)
    {

        if (!get_both_dongles(coder))
            break ;
        do_compile(coder);
        log_event(coder, DEBUGGING);
        usleep(ws->time_to_debug * 1000);
        log_event(coder, REFACTORING);
        usleep(ws->time_to_refactor * 1000);
    }
    return(NULL);
}
