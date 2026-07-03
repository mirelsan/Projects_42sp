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

#endif
