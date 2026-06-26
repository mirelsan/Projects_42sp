/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:55:20 by username          #+#    #+#             */
/*   Updated: 2026/06/25 23:23:53 by codespace        ###   ########.fr       */
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

void	rra(t_stack *a, t_options *opt)
{
	reverse(a);
	write(1, "rra\n", 4);
	opt->counts[RRA]++;
}

void	rrb(t_stack *b, t_options *opt)
{
	reverse(b);
	write(1, "rrb\n", 4);
	opt->counts[RRB]++;
}

void	rrr(t_stack *a, t_stack *b, t_options *opt)
{
	reverse(a);
	reverse(b);
	write(1, "rrr\n", 4);
	opt->counts[RRR]++;
}
