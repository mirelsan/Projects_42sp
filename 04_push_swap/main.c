/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:05:06 by username          #+#    #+#             */
/*   Updated: 2026/06/25 22:50:56 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	t_options	opt;

	if (argc < 2)
		return (0);
	stack_b = ft_new_stack();
	if(parse_options(argc, argv, &opt) == -1)
	{
		write(2, "Error\n", 6);
		return (1);
	}
	stack_a = select_and_sort(argv, stack_b, &opt);
	if (!stack_a)
	{
		write(2, "Error\n", 6);
		return (1);
	}
	return (0);
}

t_stack *select_and_sort(char **argv, t_stack *b, t_options *opt)
{
	t_stack *a;
	
	a = ft_parse_args(argv, opt->start_index);
	if(!a)
		return(NULL);
	if(opt->mode == SIMPLE)
		sort_n2(a, b);
	else if(opt->mode == MEDIUM)
		sort_chunk(a, b);
	else if(opt->mode == COMPLEX)
		sort_radix(a, b);
	else if(opt->mode == ADAPTIVE)
		sort_adaptative(a, b);
	return(a);
}
