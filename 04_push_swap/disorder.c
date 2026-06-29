/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   disorder.c                                        :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/22 15:14:11 by username         #+#    #+#              */
/*   Updated: 2026/06/29 01:07:18 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

double	disorder(t_stack *stack)
{
	double	mistakes;
	double	total;
	t_node	*outer;
	t_node	*inner;

	mistakes = 0;
	total = 0;
	outer = stack->head;
	while (outer != NULL && outer->next != NULL)
	{
		inner = outer->next;
		while (inner != NULL)
		{
			total += 1;
			if (outer->data > inner->data)
			{
				mistakes += 1;
			}
			inner = inner->next;
		}
		outer = outer->next;
	}
	return (mistakes / total);
}

static void	print_disorder(double disorder_value)
{
	int	total;
	int	part1;
	int	part2;

	total = disorder_value * 10000 + 0.5;
	part1 = total / 100;
	part2 = total % 100;
	write(2, "[bench] disorder: ", 18);
	ft_putnbr_fd(part1, 2);
	write(2, ".", 1);
	if (part2 < 10)
		write(2, "0", 1);
	ft_putnbr_fd(part2, 2);
	write(2, "%\n", 2);
}
