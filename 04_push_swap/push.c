/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   push.c                                            :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/18 15:53:51 by username         #+#    #+#              */
/*   Updated: 2026/06/22 14:55:33 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

//Push(pa, pb) : Move the top element from one stack to the top of the other.

#include "push_swap.h"

void	push(t_stack *from, t_stack *to)
{
	t_node	*node;

	if (!from || !from->head || !to)
		return ;
	node = from->head;
	from->head = node->next;
	if (!from->head)
		from->tail = NULL;
	from->size--;
	ft_add_head(to, node);
}

void	pa(t_stack *a, t_stack *b)
{
	push(b, a);
	write(1, "pa\n", 3);
}

void	pb(t_stack *a, t_stack *b)
{
	push(a, b);
	write(1, "pb\n", 3);
}
