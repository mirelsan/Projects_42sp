/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_bonus.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 02:50:13 by username          #+#    #+#             */
/*   Updated: 2026/07/03 03:17:03 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CHECKER_BONUS_H
# define CHECKER_BONUS_H

# include "../push_swap.h"

# define ERROR_MESSAGE "Error\n"
# define MAX_INSTRUCTION_LENGTH 5

int		read_line(char *buffer, int max_len);
int		apply_operation(char *instruction, t_stack *a, t_stack *b);
int		read_and_apply(t_stack *a, t_stack *b);
void	free_stack(t_stack *stack);
int		print_error_message(void);
int		run_checker(t_stack *a, t_stack *b);
void	execute_instruction(const char *instr, t_stack *a, t_stack *b);
int		is_valid_instruction(const char *instr);

#endif
