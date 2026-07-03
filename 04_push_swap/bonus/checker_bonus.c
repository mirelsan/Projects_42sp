/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   checker_bonus.c                                   :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/03 02:51:48 by username         #+#    #+#              */
/*   Updated: 2026/07/03 11:57:55 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"
#include "../push_swap.h"
#include "../libft/libft.h"

int	is_valid_instruction(const char *instr)
{
	if (!ft_strncmp(instr, "sa", 3) || !ft_strncmp(instr, "sb\0", 3))
		return (1);
	if (!ft_strncmp(instr, "ss", 3) || !ft_strncmp(instr, "pa\0", 3))
		return (1);
	if (!ft_strncmp(instr, "pb", 3) || !ft_strncmp(instr, "ra\0", 3))
		return (1);
	if (!ft_strncmp(instr, "rb", 3) || !ft_strncmp(instr, "rr\0", 3))
		return (1);
	if (!ft_strncmp(instr, "rra", 4) || !ft_strncmp(instr, "rrb\0", 4))
		return (1);
	if (!ft_strncmp(instr, "rrr", 4))
		return (1);
	return (0);
}

void	execute_double(const char *instr, t_stack *a, t_stack *b)
{
	if (!ft_strncmp(instr, "ss", 2) && instr[2] == '\0')
	{
		swap(a);
		swap(b);
	}
	else if (!ft_strncmp(instr, "rr", 2) && instr[2] == '\0')
	{
		rotate(a);
		rotate(b);
	}
	else if (!ft_strncmp(instr, "rrr", 3) && instr[3] == '\0')
	{
		reverse(a);
		reverse(b);
	}
}

void	execute_instruction(const char *instr, t_stack *a, t_stack *b)
{
	if (!ft_strncmp(instr, "sa", 2) && instr[2] == '\0')
		swap(a);
	else if (!ft_strncmp(instr, "sb", 2) && instr[2] == '\0')
		swap(b);
	else if (!ft_strncmp(instr, "pa", 2) && instr[2] == '\0')
		push(b, a);
	else if (!ft_strncmp(instr, "pb", 2) && instr[2] == '\0')
		push(a, b);
	else if (!ft_strncmp(instr, "ra", 2) && instr[2] == '\0')
		rotate(a);
	else if (!ft_strncmp(instr, "rb", 2) && instr[2] == '\0')
		rotate(b);
	else if (!ft_strncmp(instr, "rra", 3) && instr[3] == '\0')
		reverse(a);
	else if (!ft_strncmp(instr, "rrb", 3) && instr[3] == '\0')
		reverse(b);
	else
		execute_double(instr, a, b);
}

int	read_line(char *buffer, int max_len)
{
	int		index;
	char	c;
	int		too_long;

	index = 0;
	too_long = 0;
	c = '\0';
	while (read(0, &c, 1) > 0)
	{
		if (c == '\n')
			break ;
		if (index < max_len - 1)
			buffer[index++] = c;
		else
			too_long = 1;
	}
	if (index < max_len)
		buffer[index] = '\0';
	else
		buffer[max_len - 1] = '\0';
	if (too_long)
		return (-1);
	if (index == 0 && c != '\n')
		return (0);
	return (1);
}
