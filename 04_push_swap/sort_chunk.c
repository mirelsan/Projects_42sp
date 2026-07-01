/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_chunk.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 22:07:15 by username          #+#    #+#             */
/*   Updated: 2026/07/01 01:46:34 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_chunk(t_stack *a, t_stack *b, t_options *opt)
{
	int	num_chunks;
	int	i;

	if (is_sorted(a))
		return ;
	ft_set_index(a);
	num_chunks = 5;
	if (a->size > 100)
		num_chunks = 11;
	opt->width = a->size / num_chunks;
	i = 0;
	while (i < num_chunks)
	{
		proc_chunk(a, b, i, opt);
		i++;
	}
	while (b->size > 0)
	{
		extract_max_to_top_b(b, opt);
		pa(a, b, opt);
	}
}

void	proc_chunk(t_stack *a, t_stack *b, int chunk_idx, t_options *opt)
{
	int	target_pos;
	int	chunk_mid;

	chunk_mid = (chunk_idx * opt->width) + (opt->width / 2);
	while (1)
	{
		target_pos = find_closest_in_chunk(a, chunk_idx, opt);
		if (target_pos == -1)
			break ;
		if (target_pos <= a->size / 2)
		{
			while (target_pos--)
				ra(a, opt);
		}
		else
		{
			target_pos = a->size - target_pos;
			while (target_pos--)
				rra(a, opt);
		}
		pb(a, b, opt);
		if (b->size > 1 && b->head->index < chunk_mid)
			rb(b, opt);
	}
}

void	extract_max_to_top_b(t_stack *b, t_options *opt)
{
	int	max_pos;

	max_pos = find_max_pos_b(b);
	if (max_pos <= b->size / 2)
	{
		while (max_pos--)
			rb(b, opt);
	}
	else
	{
		max_pos = b->size - max_pos;
		while (max_pos--)
			rrb(b, opt);
	}
}

int	find_max_pos_b(t_stack *b)
{
	t_node	*current;
	t_node	*max_node;
	int		max_pos;
	int		curr_pos;

	current = b->head;
	max_node = current;
	max_pos = 0;
	curr_pos = 0;
	while (current != NULL)
	{
		if (current->data > max_node->data)
		{
			max_node = current;
			max_pos = curr_pos;
		}
		current = current->next;
		curr_pos++;
	}
	return (max_pos);
}

int	find_closest_in_chunk(t_stack *a, int chunk_idx, t_options *opt)
{
	t_node	*curr;
	int		curr_pos;
	int		bot_pos;
	int		top_pos;
	int		max_chunks;

	max_chunks = configure_max_chunks(a);
	curr = a->head;
	curr_pos = 0;
	bot_pos = -1;
	top_pos = -1;
	while (curr != NULL)
	{
		if ((curr->index / opt->width) == chunk_idx
			|| (chunk_idx == (max_chunks - 1)
				&& (curr->index / opt->width) >= chunk_idx))
		{
			if (top_pos == -1)
				top_pos = curr_pos;
			bot_pos = curr_pos;
		}
		curr = curr->next;
		curr_pos++;
	}
	return (decide_position(top_pos, bot_pos, a->size));
}
