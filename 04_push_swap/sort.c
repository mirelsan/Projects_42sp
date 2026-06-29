/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   sort.c                                            :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/22 11:15:08 by username         #+#    #+#              */
/*   Updated: 2026/06/29 01:05:26 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sorted(t_stack *stack)
{
	t_node	*current;

	current = stack->head;
	while (current && current->next)
	{
		if (current->data > current->next->data)
			return (0);
		current = current->next;
	}
	return (1);
}

void	sort_3(t_stack *a, t_options *opt)
{
	int	first;
	int	second;
	int	third;

	first = a->head->data;
	second = a->head->next->data;
	third = a->tail->data;
	if (first < second && second < third)
		return ;
	else if (first > second && second < third && first < third)
		sa(a, opt);
	else if (first > second && second > third)
	{
		sa(a, opt);
		rra(a, opt);
	}
	else if (first > second && second < third && first > third)
		ra(a, opt);
	else if (first < second && second > third && first < third)
	{
		sa(a, opt);
		ra(a, opt);
	}
	else if (first < second && second > third && first > third)
		rra(a, opt);
}

void	extract_top(t_stack *a, t_options *opt)
{
	t_node	*curr;
	t_node	*node;
	int		pos;
	int		target_pos;

	pos = 0;
	target_pos = 0;
	if (!a || !a->head)
		return ;
	curr = a->head;
	node = curr;
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
	rotate_direction(a, opt, target_pos, node);
}

void	sort_n2(t_stack *a, t_stack *b, t_options *opt)
{
	if (is_sorted(a))
		return ;
	while (a->size > 3)
	{
		extract_top(a, opt);
		pb(a, b, opt);
	}
	sort_3(a, opt);
	while (b->size > 0)
		pa(a, b, opt);
}

void	rotate_direction(t_stack *a, t_options *opt, int target_pos, t_node *node)
{
	if (target_pos <= a->size / 2)
		while (a->head != node)
		ra(a, opt);
	else
		while (a->head != node)
		rra(a, opt);
}
