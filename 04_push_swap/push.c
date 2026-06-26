/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:53:51 by username          #+#    #+#             */
/*   Updated: 2026/06/25 23:22:08 by codespace        ###   ########.fr       */
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

void	pa(t_stack *a, t_stack *b, t_options *opt)
{
	push(b, a);
	write(1, "pa\n", 3);
	opt->counts[PA]++;
}

void	pb(t_stack *a, t_stack *b, t_options *opt)
{
	push(a, b);
	write(1, "pb\n", 3);
	opt->counts[PB]++;
}
