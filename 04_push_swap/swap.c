/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 15:56:24 by username          #+#    #+#             */
/*   Updated: 2026/06/25 23:18:51 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//Swap(sa, sb, ss) : Swap the first 2 elements at the top of the stack.

#include "push_swap.h"

void	swap(t_stack *stack)
{
	int	tmp;

	if (!stack || !stack->head || !stack->head->next)
		return ;
	tmp = stack->head->data;
	stack->head->data = stack->head->next->data;
	stack->head->next->data = tmp;
}

void	sa(t_stack *a, t_options *opt)
{
	swap(a);
	write(1, "sa\n", 3);
	opt->counts[SA]++;
}

void	sb(t_stack *b, t_options *opt)
{
	swap(b);
	write(1, "sb\n", 3);
	opt->counts[SB]++;
}

void	ss(t_stack *a, t_stack *b, t_options *opt)
{
	swap(a);
	swap(b);
	write(1, "ss\n", 3);
	opt->counts[SS]++;
}
