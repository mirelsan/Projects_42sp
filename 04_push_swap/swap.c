/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adedias- <adedias-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:56:24 by username          #+#    #+#             */
/*   Updated: 2026/06/18 17:10:46 by adedias-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//Swap(sa, sb, ss) : Swap the first 2 elements at the top of the stack.

#include "push_swap.h"

void swap(t_stack  *stack)
{
	t_node *tmp;

	tmp->data = stack->head->data;
	stack->head->data = stack->head->next->data;
	stack->head->next->data = tmp->data;
}
