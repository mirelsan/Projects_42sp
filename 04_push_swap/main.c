/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:05:06 by username          #+#    #+#             */
/*   Updated: 2026/06/24 23:54:11 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;

	if (argc < 2)
		return (0);
	stack_b = ft_new_stack();
	stack_a = select_and_sort(argc, argv, stack_b);
	if (!stack_a)
	{
		write(2, "Error\n", 6);
		return (1);
	}
	return (0);
}

t_stack *select_and_sort(int argc, char **argv, t_stack *b)
{
	t_stack *a;
	int start_index;

	if(ft_strncmp(argv[1], "--simple", 9) == 0)
	{
		start_index = 2;
		a = ft_parse_args(argv, start_index);
		sort_n2(a, b);
	}
	else if(ft_strncmp(argv[1], "--medium", 9) == 0)
	{
		start_index = 2;
		a = ft_parse_args(argv, start_index);
		sort_chunk(a, b);
	}
	else if(ft_strncmp(argv[1], "--complex", 10) == 0)
	{
		start_index = 2;
		a = ft_parse_args(argv, start_index);
		sort_radix(a, b);
	}
	else if(ft_strncmp(argv[1], "--adaptive", 11) == 0)
	{
		start_index = 2;
		a = ft_parse_args(argv, start_index);
		sort_adaptative(a, b);
	}
	else 
	{
		start_index = 1;
		a = ft_parse_args(argv, start_index);
		sort_adaptative(a, b);
	}
	return(a);
}
