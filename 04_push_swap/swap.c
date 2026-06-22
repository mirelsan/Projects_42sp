/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adedias- <adedias-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:56:24 by username          #+#    #+#             */
/*   Updated: 2026/06/22 10:43:53 by adedias-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//Swap(sa, sb, ss) : Swap the first 2 elements at the top of the stack.

#include "push_swap.h"

void swap(t_stack  *stack)
{
	int tmp;

	if (!stack || !stack->head || !stack->head->next)
		return ;
	tmp = stack->head->data;
	stack->head->data = stack->head->next->data;
	stack->head->next->data = tmp;
}
void sa(t_stack *a)
{
	swap(a);
	write(1, "sa\n", 3);
}

void sb(t_stack  *b)
{
	swap(b);
	write(1, "sb\n", 3);
}
void ss(t_stack  *a, t_stack  *b)
{
	t_node *tmp;

	swap(a);
	swap(b);
	write(1, "ss\n", 3);
}
