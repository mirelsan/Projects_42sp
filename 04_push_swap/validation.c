/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   validation.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/16 23:59:37 by username         #+#    #+#              */
/*   Updated: 2026/06/18 14:44:35 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

//1. verify if int is valid
//2. verify if int is in the range
//3. verify duplicates

#include "push_swap.h"

int	ft_int_validated(char *str)
{
	if (*str == '\0')
		return (0);
	if (*str == '-' || *str == '+')
	{
		str++;
		if (*str == '\0')
			return (0);
	}
	while (*str)
	{
		if (*str < '0' || *str > '9')
		{
			return (0);
		}
		str++;
	}
	return (1);
}

int	ft_int_range(char *str)
{
	long int	str_long;

	str_long = ft_atoi_long(str);
	if (str_long >= INT_MIN && str_long <= INT_MAX)
		return (1);
	return (0);
}

long int	ft_atoi_long(const char *str)
{
	int			sign;
	long int	sum;
	int			i;

	sum = 0;
	sign = 1;
	i = 0;
	while (str[i] == ' ' || (str[i] >= 9 && str[i] <= 13))
	{
		i++;
	}
	if (str[i] == '-')
	{
		sign *= -1;
		i++;
	}
	else if (str[i] == '+')
		i++;
	while (str[i] >= '0' && str[i] <= '9')
	{
		sum = (str[i] - '0') + (sum * 10);
		i++;
	}
	return ((long) sum * sign);
}

int	ft_int_duplicate(t_stack *stack, int new_n)
{
	t_node	*current;

	current = stack->head;
	while (current != NULL)
	{
		if (current->data == new_n)
			return (1);
		current = current->next;
	}
	return (0);
}

int	ft_create_and_append(t_stack *stack, char *str)
{
	int		numbers;
	t_node	*node_numb;

	if (!ft_int_validated(str))
		return (0);
	if (!ft_int_range(str))
		return (0);
	numbers = ft_atoi_long(str);
	if (ft_int_duplicate(stack, numbers))
	{
		return (0);
	}
	node_numb = ft_new_node(numbers);
	if (!node_numb)
		return (0);
	ft_add_head(stack, node_numb);
	return (1);
}
