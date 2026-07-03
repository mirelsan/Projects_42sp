/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing_utils_bonus.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 02:51:53 by username          #+#    #+#             */
/*   Updated: 2026/07/03 02:57:40 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"
#include "../push_swap.h"
#include "../libft/libft.h"

int	print_error_message(void)
{
	write(2, ERROR_MESSAGE, 6);
	return (1);
}

void	free_stack(t_stack *stack)
{
	t_node	*current;
	t_node	*next;

	if (!stack)
		return ;
	current = stack->head;
	while (current)
	{
		next = current->next;
		free(current);
		current = next;
	}
	free(stack);
}

int	apply_operation(char *instruction, t_stack *a, t_stack *b)
{
	if (!is_valid_instruction(instruction))
		return (0);
	execute_instruction(instruction, a, b);
	return (1);
}

int	read_and_apply(t_stack *a, t_stack *b)
{
	char	buffer[MAX_INSTRUCTION_LENGTH + 1];
	int		line_result;

	while (1)
	{
		line_result = read_line(buffer, MAX_INSTRUCTION_LENGTH + 1);
		if (line_result == 0)
			break ;
		if (line_result == -1)
			return (0);
		if (!apply_operation(buffer, a, b))
			return (0);
	}
	return (1);
}
