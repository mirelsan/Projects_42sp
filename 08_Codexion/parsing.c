/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:25:35 by username          #+#    #+#             */
/*   Updated: 2026/10/27 01:59:38 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

// ./coder 5    800     200     200 [5]
//        av[1] av[2]   av[3] ...
//1) actual numbers
//2)not > INT_MAX
//3) TIMESTAMPS > 60ms

static long	parse_scheduler(const char *str)
{
	if (strcmp(str, "fifo") == 0)
		return (SCHEDULER_FIFO);
	if (strcmp(str, "edf") == 0)
		return (SCHEDULER_EDF);
	error_exit("Invalid scheduler! Choose 'fifo' or 'edf'.");
	return (-1);
}

void	parse_input(t_workspace *workspace, char **av)
{
	workspace->number_of_coders = ft_atoi(av[1]);
	if (workspace->number_of_coders <= 0)
		error_exit("Number of coders must be greater than 0");
	workspace->time_to_burnout = ft_atoi(av[2]);
	workspace->time_to_compile = ft_atoi(av[3]);
	workspace->time_to_debug = ft_atoi(av[4]);
	workspace->time_to_refactor = ft_atoi(av[5]);
	workspace->dongle_cooldown = ft_atoi(av[7]);
	workspace->number_of_compiles_required = ft_atoi(av[6]);
	if (workspace->number_of_compiles_required <= 0)
		error_exit("Number of compiles required must be greater than 0");
	workspace->scheduler = parse_scheduler(av[8]);
}
