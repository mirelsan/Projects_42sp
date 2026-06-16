/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   parsing.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/15 02:09:35 by username         #+#    #+#              */
/*   Updated: 2026/06/16 15:14:24 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

//1.parsing 2 cases: multi argvs -> already separated
//                   argv with spaces -> ft_split first to kill spaces
//then ft_atoi to convert string to int.

#include "push_swap.h"

t_stack	*ft_new_stack(void)
{
	t_stack	*ptr = malloc(sizeof(t_stack));

	if (!ptr)
		return (NULL);
	ptr->head = NULL;
	ptr->tail = NULL;
	ptr->size = 0;
	return (ptr);
}

void	ft_add_front(t_stack **stack, t_node *new)
{
	new->next = (*stack)->head;
	(*stack)->head = new;
}

int	main(int argc, char **argv)
{
	if (argc < 2)
		return (0);
	else
		(**argv == ' ');
	ft_split(argv);
}
