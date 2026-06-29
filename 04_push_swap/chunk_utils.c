/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   chunk_utils.c                                     :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/23 02:19:10 by username         #+#    #+#              */
/*   Updated: 2026/06/29 01:07:25 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ft_min(t_stack *a)
{
	t_node	*curr;
	t_node	*node;

	curr = a->head;
	node = curr;
	while (curr != NULL)
	{
		if (curr->data < node->data)
		{
			node = curr;
		}
		curr = curr->next;
	}
	return (node->data);
}

int	ft_sqrt(int n)
{
	int	i;

	i = 0;
	while (i * i < n)
	{
		i++;
	}
	return (i);
}

int	width_range(t_stack *a, int num_chunks)
{
	int	range;
	int	num;

	range = ft_max(a) - ft_min(a);
	num = (range + num_chunks - 1) / num_chunks;
	return (num);
}

int	ft_chunk(int min, int width_range, int value)
{
	int	index;

	index = (value - min) / width_range;
	return (index);
}
