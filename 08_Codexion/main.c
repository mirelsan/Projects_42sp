/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:25:04 by username          #+#    #+#             */
/*   Updated: 2026/10/27 02:41:42 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

static void	launch_coders(t_workspace *ws)
{
	int	i;

	i = 0;
	while (i < ws->number_of_coders)
	{
		safe_thread_handle(&ws->coders[i].thread_id, coder_routine,
			&ws->coders[i], CREATE);
		i++;
	}
}

static void	join_coders(t_workspace *ws)
{
	int	i;

	i = 0;
	while (i < ws->number_of_coders)
	{
		safe_thread_handle(&ws->coders[i].thread_id, NULL, NULL, JOIN);
		i++;
	}
}

int	main(int ac, char **av)
{
	t_workspace	ws;
	pthread_t	monitor;

	if (ac != 9)
	{
		printf("Usage: ./codexion <coders> <burnout> <compile> <debug> "
			"<refactor> <compiles> <cooldown> <fifo|edf|lifo>\n");
		return (1);
	}
	parse_input(&ws, av);
	ws.start_simulation = get_time_ms();
	data_init(&ws);
	launch_coders(&ws);
	safe_thread_handle(&monitor, monitor_routine, &ws, CREATE);
	join_coders(&ws);
	safe_thread_handle(&monitor, NULL, NULL, JOIN);
	cleanup_data(&ws);
	return (0);
}
