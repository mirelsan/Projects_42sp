/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   options.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/24 16:16:55 by username         #+#    #+#              */
/*   Updated: 2026/07/01 13:53:07 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	parse_options(int argc, char **argv, t_options *opt)
{
	int	i;
	int	success;

	opt->bench = 0;
	opt->mode = ADAPTIVE;
	i = 1;
	while (i < argc)
	{
		success = apply_flag(argv, opt, i);
		if (success == 1)
			i++;
		else if (success == -1)
			return (-1);
		else if (success == 0)
			break ;
	}
	opt->start_index = i;
	return (0);
}

int	apply_flag(char **argv, t_options *opt, int i)
{
	if (ft_strncmp(argv[i], "--bench", 8) == 0)
		opt->bench = 1;
	else if (ft_strncmp(argv[i], "--simple", 9) == 0)
		opt->mode = SIMPLE;
	else if (ft_strncmp(argv[i], "--medium", 9) == 0)
		opt->mode = MEDIUM;
	else if (ft_strncmp(argv[i], "--complex", 10) == 0)
		opt->mode = COMPLEX;
	else if (ft_strncmp(argv[i], "--adaptive", 11) == 0)
		opt->mode = ADAPTIVE;
	else if (ft_strncmp(argv[i], "--", 2) == 0)
	{
		return (-1);
	}
	else
	{
		return (0);
	}
	return (1);
}
