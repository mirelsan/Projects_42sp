/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing_utils2.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adedias- <adedias-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 00:08:31 by username          #+#    #+#             */
/*   Updated: 2026/07/02 14:00:55 by adedias-         ###   ########.fr       */
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

void	ft_free_stack(t_stack *stack)
{
	t_node	*tmp;

	if ((!stack))
		return ;
	while (stack->head)
	{
		tmp = stack->head;
		stack->head = stack->head->next;
		free(tmp);
	}
	free(stack);
}

void	ft_free_split(char **split)
{
	int	i;

	if (!split)
		return ;
	i = 0;
	while (split[i])
	{
		free(split[i]);
		i++;
	}
	free(split);
}

void	free_append(t_stack *stack, char **str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		if (!ft_create_and_append(stack, str[i]))
		{
			ft_free_split(str);
			ft_free_stack(stack);
			return ;
		}
		i++;
	}
}
