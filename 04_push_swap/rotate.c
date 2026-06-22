/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adedias- <adedias-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:57:23 by username          #+#    #+#             */
/*   Updated: 2026/06/22 10:44:49 by adedias-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//Rotate(ra, rb, rr) : Shift all elements of the stack up by 1 position(the 1st element becomes the last).

#include "push_swap.h"

void rotate(t_stack *stack)
{
	t_node *first;
	
	if (!stack || !stack->head || !stack->head->next)
		return (NULL);
	first = stack->head;
	stack->head = first->next;
	first->next = NULL;
	if (stack->tail)
		stack->tail->next = NULL;
	stack->tail = first;	
}
void ra(t_stack *a)
{
	rotate(a);
	write(1, "ra\n", 3);
}

void rb(t_stack *b)
{
	rotate(b);
	write(1, "ra\n", 3);
}

void rr(t_stack *a, t_stack *b)
{
	rotate(a);
	rotate(b);
	write(1, "rr\n", 3);
}
