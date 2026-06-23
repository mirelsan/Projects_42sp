/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 11:15:08 by adedias-          #+#    #+#             */
/*   Updated: 2026/06/23 20:46:36 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int is_sorted(t_stack *stack)
{
	t_node *current;
	
	current = stack->head;
	while (current && current->next)
	{
		if (current->data > current->next->data)
			return (0);
		current = current->next;
	}
	return (1);
}
void sort_3(t_stack *a)
{
	int first;
	int second;
	int third;
	
	first = a->head->data;
	second = a->head->next->data;
	third = a->tail->data;
	if(first < second && second < third)
		return ;
	else if (first > second && second < third && first < third)
		sa(a);
	else if (first > second && second > third)
	{
		sa(a);
		rra(a);
	}
	else if (first > second && second < third && first > third)
		ra(a);
	else if (first < second && second > third && first < third)
	{
		sa(a);
		ra(a);
	}
	else if (first < second && second > third && first > third)
		rra(a);
}
void extract_top(t_stack *a)
{
	t_node *curr;
	t_node *node;
	int pos;
	int target_pos;

	curr = a->head;
	node = curr;
	pos = 0;
	target_pos = 0;

	if (!a || !a->head)
		return ;
	
	while (curr)
	{
		if (curr->data < node->data)
		{
			node = curr;
			target_pos = pos;
		}
		pos++;
		curr = curr->next;
	}
	if (target_pos <= a->size / 2)
		while (a->head != node)
			ra(a);
	else		
		while (a->head != node)
			rra(a);
}


void sort_n2(t_stack *a, t_stack *b)
{
	if (is_sorted(a))
		return ;
	while (a->size > 3)
	{
		extract_top(a);
		pb(a, b);
	}
	sort_3(a);
	while (b->size > 0)
		pa(a, b);
}