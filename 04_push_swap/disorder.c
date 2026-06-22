/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   disorder.c                                        :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/22 15:14:11 by username         #+#    #+#              */
/*   Updated: 2026/06/22 16:31:43 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

double	disorder(t_stack *stack)
{
	int		mistakes;
	int		total;
	t_node	*outer;
	t_node	*inner;

	mistakes = 0;
	total = 0;
	t_node	outer = *stack->head;

	while (outer != NULL && outer->next != NULL)
	{
		t_node	*inner = outer->next;

		while (inner != NULL)
		{
			inner = inner->next;
		}
		outer = outer->next;
		total += 1;
		if (outer > inner)
			mistakes += 1;
		return (mistakes / total);
	}
}
