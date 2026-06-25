/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   options.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 16:16:55 by pc2               #+#    #+#             */
/*   Updated: 2026/06/25 22:22:10 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"


int parse_options(int argc, char **argv, t_options *opt)
{
	int i;
	
	opt->bench = 0;
	opt->mode = ADAPTIVE;
	i = 1;
	while (i < argc)
	{
		if (ft_strncmp(argv[i],  "--bench", 8) == 0)
			opt->bench = 1;
		else if (ft_strncmp(argv[i],  "--simple", 9) == 0)
			opt->mode = SIMPLE;
		else if (ft_strncmp(argv[i],  "--medium", 9) == 0)
			opt->mode = MEDIUM;
		else if (ft_strncmp(argv[i],  "--complex", 10) == 0)
			opt->mode = COMPLEX;
		else if (ft_strncmp(argv[i],  "--adaptive", 11) == 0)
			opt->mode = ADAPTIVE;
		else if (ft_strncmp(argv[i],  "--", 2) == 0)
		{
			if (is_valid_flag(argv[i]) != 0)
				return (-1);
		}
		else
			break ;
		i++;
	}
	opt->start_index = i;
	return (0);
}

int	is_valid_flag(char *arg)
{
	if (ft_strncmp(arg, "--", 2) == 0)
		if (ft_strncmp(arg,  "--simple", 9) == 0 ||
			(ft_strncmp(arg,  "--medium", 9) == 0) ||
			(ft_strncmp(arg,  "--complex", 10) == 0) ||
			(ft_strncmp(arg,  "--adaptive", 11) == 0) ||
			(ft_strncmp(arg,  "--bench", 8) == 0))
				return (0);
	return (-1);
}
