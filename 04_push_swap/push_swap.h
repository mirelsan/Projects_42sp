/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   push_swap.h                                       :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/15 02:10:09 by username         #+#    #+#              */
/*   Updated: 2026/06/18 15:10:37 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>
# include <limits.h>

typedef struct t_node
{
	int				data;
	int				index;
	struct t_node	*next;
}	t_node;

typedef struct t_stack
{
	t_node	*head;
	t_node	*tail;
	int		size;
}	t_stack;

t_stack		*ft_new_stack(void);
void		ft_add_head(t_stack *stack, t_node *new);
t_node		*ft_new_node(int data);
t_stack		*ft_parse_args(char **argv);
int			main(int argc, char **argv);
int			ft_int_validated(char *str);
int			ft_int_range(char *str);
long int	ft_atoi_long(const char *str);
int			ft_int_duplicate(t_stack *stack, int new_n);
int			ft_create_and_append(t_stack *stack, char *str);
int			ft_atoi(const char *npr);
char		*ft_strchr(const char *s, int c);
char		**ft_split(char const *s, char c);

#endif
