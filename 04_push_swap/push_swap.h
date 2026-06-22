/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adedias- <adedias-@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/15 02:10:09 by username          #+#    #+#             */
/*   Updated: 2026/06/22 10:41:25 by adedias-         ###   ########.fr       */
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
void 		swap(t_stack  *stack);
void 		sa(t_stack *a);
void 		sb(t_stack  *b);
void 		ss(t_stack  *a, t_stack  *b);
void 		push(t_stack *from, t_stack *to);
void 		pa(t_stack *a, t_stack *b);
void 		pb(t_stack *a, t_stack *b);
void 		rotate(t_stack *stack);
void 		ra(t_stack *a);
void 		rb(t_stack *b);
void 		rr(t_stack *a, t_stack *b);
void 		reverse(t_stack *stack);
void 		rra(t_stack *a);
void 		rrb(t_stack *b);
void 		rrr(t_stack *a, t_stack *b);

#endif
