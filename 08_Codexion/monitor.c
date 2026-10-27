/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:25:23 by username          #+#    #+#             */
/*   Updated: 2026/10/27 02:37:19 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

static long	read_last_start(t_coder *coder)
{
	long	last;

	safe_mutex_handle(&coder->progress_mutex, LOCK);
	last = coder->last_compile_time;
	safe_mutex_handle(&coder->progress_mutex, UNLOCK);
	return (last);
}

static bool	coder_done(t_workspace *ws, t_coder *coder)
{
	bool	done;

	safe_mutex_handle(&coder->progress_mutex, LOCK);
	done = coder->number_compiles >= ws->number_of_compiles_required;
	safe_mutex_handle(&coder->progress_mutex, UNLOCK);
	return (done);
}

static int	find_burnout(t_workspace *ws, bool *all_finished)
{
	int	i;

	*all_finished = true;
	i = 0;
	while (i < ws->number_of_coders)
	{
		if (!coder_done(ws, &ws->coders[i]))
		{
			*all_finished = false;
			if (get_time_ms() - read_last_start(&ws->coders[i])
				> ws->time_to_burnout)
				return (i);
		}
		i++;
	}
	return (-1);
}

void	*monitor_routine(void *arg)
{
	t_workspace	*ws;
	int			burned;
	bool		all_finished;

	ws = (t_workspace *) arg;
	while (!simulation_over(ws))
	{
		burned = find_burnout(ws, &all_finished);
		if (burned >= 0)
		{
			stop_simulation(ws);
			log_event(&ws->coders[burned], BURNOUT);
			return (NULL);
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
