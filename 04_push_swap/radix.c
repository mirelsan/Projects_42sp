/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 01:54:03 by codespace         #+#    #+#             */
/*   Updated: 2026/06/25 23:48:20 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int max_bits(t_stack *a)
{
	t_node *curr;
	int max;
	int i;

	if (!a || !a->head)
		return (0);
	curr = a->head;
	max = 0;
	while (curr)
	{
		if (curr->index > max)
			max = curr->index;
		curr = curr->next;
	}
	
	i = 0;
	while ((1 << i) <= max)
		i++;
	return (i);
}

int has_bit(int n, int bit)
{
	int shifed;
	
	shifed = (n >> bit);
	return ( shifed & 1);
}

void process_bit(t_stack *a, t_stack *b, int bit, t_options *opt)
{
	int bit_size;

	bit_size = a->size;
	while (bit_size--)
	{
		if (has_bit(a->head->index, bit))
			ra(a, opt);
		else
			pb(a, b, opt);
	}
	while (b->size > 0)
		pa(a, b, opt);
}

void ft_set_index(t_stack *a)
{
	t_node *outer;
    t_node *inner;
    int 	count;
	
    outer = a->head;
    while (outer)
    {
		count = 0;
		inner = a->head;
		while(inner)
		{
			if(inner->data < outer->data)
			count++;
			inner = inner->next;	
		}
		outer->index = count;
		outer = outer->next;
    }
}
void sort_radix(t_stack *a, t_stack *b, t_options *opt)
{
	int bits;
	int i;

	if (!a || a->size <= 1)
		return ;
	
	if (is_sorted(a))
		return ;
		
	ft_set_index(a);	
	bits = max_bits(a);
	i = 0;
	while (i < bits)
	{
		process_bit(a, b, i, opt);
		i++;
	}
}
