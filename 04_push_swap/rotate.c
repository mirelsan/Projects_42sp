/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   rotate.c                                          :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/18 15:57:23 by username         #+#    #+#              */
/*   Updated: 2026/06/30 14:59:20 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rotate(t_stack *stack)
{
	t_node	*first;

	if (!stack || !stack->head || !stack->head->next)
		return ;
	first = stack->head;
	stack->head = first->next;
	first->next = NULL;
	if (stack->tail)
		stack->tail->next = first;
	stack->tail = first;
}

void	ra(t_stack *a, t_options *opt)
{
	rotate(a);
	write(1, "ra\n", 3);
	opt->counts[RA]++;
}

void	rb(t_stack *b, t_options *opt)
{
	rotate(b);
	write(1, "rb\n", 3);
	opt->counts[RB]++;
}

void	rr(t_stack *a, t_stack *b, t_options *opt)
{
	rotate(a);
	rotate(b);
	write(1, "rr\n", 3);
	opt->counts[RR]++;
}
