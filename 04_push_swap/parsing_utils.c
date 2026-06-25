/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing_utils.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/15 02:09:35 by username          #+#    #+#             */
/*   Updated: 2026/06/25 01:49:04 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//1.parsing 2 cases: multi argvs -> already separated
//                   argv with spaces -> ft_split first to kill spaces
//then ft_atoi to convert string to int.

#include "push_swap.h"

t_stack	*ft_new_stack(void)
{
	t_stack	*ptr;

	ptr = malloc(sizeof(t_stack));
	if (!ptr)
		return (NULL);
	ptr->head = NULL;
	ptr->tail = NULL;
	ptr->size = 0;
	return (ptr);
}

void	ft_add_head(t_stack *stack, t_node *new)
{
	if ((stack)->head == NULL)
		(stack)->tail = new;
	new->next = (stack)->head;
	(stack)->head = new;
	(stack)->size++;
}

t_node	*ft_new_node(int data)
{
	t_node	*new_node;

	new_node = malloc(sizeof(t_node));
	if (!new_node)
		return (NULL);
	new_node->data = data;
	new_node->index = 0;
	new_node->next = NULL;
	return (new_node);
}

t_stack	*ft_parse_args(char **argv, int start_index)
{
	t_stack	*stack;
	char	**str;
	int		i;

	i = start_index;
	stack = ft_new_stack();
	if (!stack)
		return (NULL);
	if (ft_strchr(argv[i], ' '))
	{
		str = ft_split(argv[i], ' ');
		if (!str)
			return (NULL);
		while (*str)
			if (!ft_create_and_append(stack, *str++))
			return (NULL);
	}
	else
		while (argv[i])
		{
			if(ft_strncmp(argv[i], "--", 2) == 0)
			{
				i++;
			}
			else if (!ft_create_and_append(stack, argv[i]))
				return (NULL);
			i++;
		}
	return (stack);
}
