/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:26:28 by username          #+#    #+#             */
/*   Updated: 2026/10/27 00:28:41 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

static bool	request_before(t_request *a, t_request *b)
{
	if (a->key != b->key)
		return (a->key < b->key);
	return (a->seq < b->seq);
}

static void	swap_requests(t_request *a, t_request *b)
{
	t_request	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

void	heap_push(t_heap *heap, t_request request)
{
	int	i;
	int	parent;

	heap->items[heap->size] = request;
	i = heap->size;
	heap->size++;
	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (!request_before(&heap->items[i], &heap->items[parent]))
			break ;
		swap_requests(&heap->items[i], &heap->items[parent]);
		i = parent;
	}
}

t_request	heap_pop(t_heap *heap)
{
	t_request	top;
	int			i;
	int			child;

	top = heap->items[0];
	heap->size--;
	heap->items[0] = heap->items[heap->size];
	i = 0;
	while (1)
	{
		child = 2 * i + 1;
		if (child >= heap->size)
			break ;
		if (child + 1 < heap->size
			&& request_before(&heap->items[child + 1], &heap->items[child]))
			child++;
		if (!request_before(&heap->items[child], &heap->items[i]))
			break ;
		swap_requests(&heap->items[i], &heap->items[child]);
		i = child;
	}
	return (top);
}

t_request	heap_peek(t_heap *heap)
{
	return (heap->items[0]);
}
