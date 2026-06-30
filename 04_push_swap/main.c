/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:05:06 by username          #+#    #+#             */
/*   Updated: 2026/06/30 01:03:25 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include "./libft/libft.h"
int	main(int argc, char **argv)
{
	t_stack		*stack_a;
	t_stack		*stack_b;
	t_options	opt;
	
	if (argc < 2)
		return (0);
	stack_b = ft_new_stack();
	ft_bzero(&opt, sizeof(t_options));
	if (parse_options(argc, argv, &opt) == -1)
	{
		write(2, "Error\n", 6);
		return (1);
	}
	stack_a = ft_parse_args(argv, opt.start_index);
	if (!stack_a)
	{
		write(2, "Error\n", 6);
		return (1);
	}
	if (execution(&opt, stack_a, stack_b) == 0)
		return (0);
	else
		return (1);
}

int	execution(t_options *opt, t_stack *stack_a, t_stack *stack_b)
{
	opt->disorder_value = disorder(stack_a);
	stack_a = select_and_sort(stack_a, stack_b, opt);
	if (!stack_a)
	{
		write(2, "Error\n", 6);
		return (1);
	}
	if (opt->bench == 1)
	{
		print_bench(opt);
	}
	return (0);
}

t_stack	*select_and_sort(t_stack *a, t_stack *b, t_options *opt)
{
	if(a->size <= 5)
		sort_n2(a, b, opt);
	else
		sort_chunk(a, b, opt);		
	return (a);
}

	//if (opt->mode == SIMPLE)
	//	sort_n2(a, b, opt);
	//else if (opt->mode == MEDIUM)
	//	sort_chunk(a, b, opt);
	//else if (opt->mode == COMPLEX)
	//	sort_radix(a, b, opt);
	//else if (opt->mode == ADAPTIVE)
	//	sort_adaptative(a, b, opt);