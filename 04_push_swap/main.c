/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:05:06 by username          #+#    #+#             */
/*   Updated: 2026/06/26 02:26:16 by codespace        ###   ########.fr       */
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
	stack_a = ft_parse_args(argv, 1);
	opt.disorder_value = disorder(stack_a);
	stack_a = select_and_sort(stack_a, stack_b, &opt);
	if (!stack_a)
	{
		write(2, "Error\n", 6);
		return (1);
	}
	if(opt.bench == 1)
	{
		print_bench(&opt);
	}
	return (0);
}

t_stack *select_and_sort(t_stack *a, t_stack *b, t_options *opt)
{

	if(opt->mode == SIMPLE)
		sort_n2(a, b, opt);
	else if(opt->mode == MEDIUM)
		sort_chunk(a, b, opt);
	else if(opt->mode == COMPLEX)
		sort_radix(a, b, opt);
	else if(opt->mode == ADAPTIVE)
		sort_adaptative(a, b, opt);
	return(a);
}
void print_bench(t_options *opt)
{
	int total;
	int part1;
	int part2;
	char *str;

	total = opt->disorder_value * 10000;
	part1 = total / 100;
	part2 = total % 100;
	str = ft_itoa(part1);
	write(2, "[bench] disorder: ", 18);
	write(2, str, ft_strlen(str));
	write(2, ".", 1);
	free(str);
	str = ft_itoa(part2);
	write(2, str, ft_strlen(str));
	write(2, "%\n", 2);
	free(str);
}
