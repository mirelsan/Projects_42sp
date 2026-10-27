/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle_wait.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/27 00:24:24 by username          #+#    #+#             */
/*   Updated: 2026/10/27 01:55:15 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

static bool	is_top(t_coder *coder, t_dongle *dongle)
{
	return (heap_peek(&dongle->queue).coder == coder);
}

static bool	my_turn(t_coder *coder, t_dongle *dongle, long now)
{
	bool	is_free;
	bool	cooldown_over;
	bool	top;

	is_free = !dongle->in_use;
	cooldown_over = now >= dongle->available_at;
	top = is_top(coder, dongle);
	return (is_free && cooldown_over && top);
}

void	wait_for_turn(t_coder *coder, t_dongle *dongle, t_workspace *ws)
{
	long	now;
	long	wait;

	now = get_time_ms();
	while (!simulation_over(ws) && !my_turn(coder, dongle, now))
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
