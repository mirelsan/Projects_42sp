/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   parsing_utils2.c                                  :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/29 00:08:31 by username         #+#    #+#              */
/*   Updated: 2026/06/30 14:58:58 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	ft_add_tail(t_stack *stack, t_node *new)
{
	new->next = NULL;
	if (stack->head == NULL)
		stack->head = new;
	else
		stack->tail->next = new;
	stack->tail = new;
	stack->size++;
}
