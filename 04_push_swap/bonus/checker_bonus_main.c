/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_bonus_main.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 02:35:33 by username          #+#    #+#             */
/*   Updated: 2026/07/03 02:43:33 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../push_swap.h"
#include "checker_bonus.h"

static int	is_stack_sorted(t_stack *stack)
{
	t_node	*current;

	if (!stack || !stack->head)
		return (1);
	current = stack->head;
	while (current->next)
	{
		if (current->data > current->next->data)
			return (0);
		current = current->next;
	}
	return (1);
}

int	main(int argc, char **argv)
{
	t_stack	*a;
	t_stack	*b;
	int		success;

	if (argc < 2)
		return (0);
	a = ft_parse_args(argv, 1);
	if (!a)
		return (print_error_message());
	b = ft_new_stack();
	if (!b)
	{
		free_stack(a);
		return (print_error_message());
	}
	return (run_checker(a, b));
}

int	run_checker(t_stack *a, t_stack *b)
{
	if (!read_and_apply(a, b))
	{
		free_stack(a);
		free_stack(b);
		return (print_error_message());
	}
	if (is_stack_sorted(a) && b->size == 0)
		write(1, "OK\n", 3);
	else
		write(1, "KO\n", 3);
	free_stack(a);
	free_stack(b);
	return (0);
}
