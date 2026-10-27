/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   simulation.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/27 00:24:24 by username          #+#    #+#             */
/*   Updated: 2026/10/27 01:55:28 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

bool	simulation_over(t_workspace *ws)
{
	bool	over;

	safe_mutex_handle(&ws->end_mutex, LOCK);
	over = ws->end_simulation;
	safe_mutex_handle(&ws->end_mutex, UNLOCK);
	return (over);
}

void	stop_simulation(t_workspace *ws)
{
	int	i;

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
