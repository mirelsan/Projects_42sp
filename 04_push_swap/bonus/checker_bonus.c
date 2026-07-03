/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_bonus.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 02:51:48 by username          #+#    #+#             */
/*   Updated: 2026/07/03 03:20:31 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"
#include "../push_swap.h"
#include "../libft/libft.h"

int	is_valid_instruction(const char *instr)
{
	return (!ft_strncmp(instr, "sa", 2) && instr[2] == '\0')
	|| (!ft_strncmp(instr, "sb", 2) && instr[2] == '\0')
	|| (!ft_strncmp(instr, "ss", 2) && instr[2] == '\0')
	|| (!ft_strncmp(instr, "pa", 2) && instr[2] == '\0')
	|| (!ft_strncmp(instr, "pb", 2) && instr[2] == '\0')
	|| (!ft_strncmp(instr, "ra", 2) && instr[2] == '\0')
	|| (!ft_strncmp(instr, "rb", 2) && instr[2] == '\0')
	|| (!ft_strncmp(instr, "rr", 2) && instr[2] == '\0')
	|| (!ft_strncmp(instr, "rra", 3) && instr[3] == '\0')
	|| (!ft_strncmp(instr, "rrb", 3) && instr[3] == '\0')
	|| (!ft_strncmp(instr, "rrr", 3) && instr[3] == '\0');
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
