/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adedias- <adedias-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:55:20 by username          #+#    #+#             */
/*   Updated: 2026/06/22 10:46:13 by adedias-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//Reverse Rotate(rra, rrb, rrr) : Shift all elements of the stack down by 1 position(the last element becomes the first).

#include "push_swap.h"

void reverse(t_stack *stack)
{
	t_node *last;
	t_node *prev;
	
	prev = stack->head;
	while (prev->next->next)
		prev = prev->next;
	last = prev->next;
	prev->next = NULL;
	last->next = stack->head;
	stack->head = last;
	stack->tail = prev;
}

void rra(t_stack *a)
{
	reverse(a);
	write(1, "rra\n", 4);
}

void rrb(t_stack *b)
{
	reverse(b);
	write(1, "rrb\n", 4);
}

void rrr(t_stack *a, t_stack *b)
{
	reverse(a);
	reverse(b);
	write(1, "rrr\n", 4);
}
