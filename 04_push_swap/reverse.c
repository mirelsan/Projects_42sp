/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   reverse.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/18 15:55:20 by username         #+#    #+#              */
/*   Updated: 2026/06/22 15:10:26 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	reverse(t_stack *stack)
{
	t_node	*last;
	t_node	*prev;

	if (!stack || !stack->head || !stack->head->next)
		return ;
	prev = stack->head;
	while (prev->next->next)
		prev = prev->next;
	last = prev->next;
	prev->next = NULL;
	last->next = stack->head;
	stack->head = last;
	stack->tail = prev;
}

void	rra(t_stack *a)
{
	reverse(a);
	write(1, "rra\n", 4);
}

void	rrb(t_stack *b)
{
	reverse(b);
	write(1, "rrb\n", 4);
}

void	rrr(t_stack *a, t_stack *b)
{
	reverse(a);
	reverse(b);
	write(1, "rrr\n", 4);
}
