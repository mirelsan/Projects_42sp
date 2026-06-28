/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/15 02:10:09 by username          #+#    #+#             */
/*   Updated: 2026/06/28 22:33:43 by codespace        ###   ########.fr       */
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

typedef enum e_mode
{
	SIMPLE,
	MEDIUM, 
	COMPLEX, 
	ADAPTIVE
} t_mode;

typedef enum e_operations
{
	SA,
	SB,
	SS,
	PA,
	PB,
	RA,
	RB,
	RR,
	RRA,
	RRB,
	RRR
}t_operations;

typedef struct s_options
{
	int bench;
	int start_index;
	int counts[11];
	double disorder_value;
	t_mode mode;
}t_options;

t_stack		*ft_new_stack(void);
void		ft_add_head(t_stack *stack, t_node *new);
t_node		*ft_new_node(int data);
t_stack		*ft_parse_args(char **argv, int start_index);
int			main(int argc, char **argv);
int			ft_int_validated(char *str);
int			ft_int_range(char *str);
long int	ft_atoi_long(const char *str);
int			ft_int_duplicate(t_stack *stack, int new_n);
int			ft_create_and_append(t_stack *stack, char *str);
int			ft_atoi(const char *npr);
char		*ft_strchr(const char *s, int c);
char		**ft_split(char const *s, char c);
void		swap(t_stack *stack);
void		sa(t_stack *a, t_options *opt);
void		sb(t_stack *b, t_options *opt);
void		ss(t_stack *a, t_stack *b, t_options *opt);
void		push(t_stack *from, t_stack *to);
void		pa(t_stack *a, t_stack *b, t_options *opt);
void		pb(t_stack *a, t_stack *b, t_options *opt);
void		rotate(t_stack *stack);
void		ra(t_stack *a, t_options *opt);
void		rb(t_stack *b, t_options *opt);
void		rr(t_stack *a, t_stack *b, t_options *opt);
void		reverse(t_stack *stack);
void		rra(t_stack *a, t_options *opt);
void		rrb(t_stack *b, t_options *opt);
void		rrr(t_stack *a, t_stack *b, t_options *opt);
void 		sort_radix(t_stack *a, t_stack *b, t_options *opt);
void 		process_bit(t_stack *a, t_stack *b, int bit, t_options *opt);
int 		has_bit(int n, int bit);
int 		max_bits(t_stack *a);
int 		is_sorted(t_stack *stack);
void 		sort_3(t_stack *a, t_options *opt);
void 		extract_top(t_stack *a, t_options *opt);
void 		sort_n2(t_stack *a, t_stack *b, t_options *opt);
double		disorder(t_stack *stack);
int 		ft_min(t_stack *a);
int 		ft_max(t_stack *a);
int 		ft_sqrt(int n);
int 		width_range(t_stack *a, int num_chunks);
int 		ft_chunk(int min, int width_range, int value);
void 		ft_set_index(t_stack *a);
void 		sort_chunk(t_stack *a, t_stack *b, t_options *opt);
t_node 		*find_min_in_chunk(t_stack *a, int min, int width, int chunk_idx);
int 		get_position(t_stack *a, t_node *target);
int			ft_strncmp(const char *s1, const char *s2, size_t n);
void 		sort_adaptative(t_stack *a, t_stack *b, t_options *opt);
int 		parse_options(int argc, char **argv, t_options *opt);
int			is_valid_flag(char *arg);
t_stack 	*select_and_sort(t_stack *a, t_stack *b, t_options *opt);
char		*ft_itoa(int n);
size_t		ft_strlen(const char *s);
void 		print_bench(t_options *opt);
void 		print_total_ops(t_options *opt);
void 		print_opt_counts(t_options *opt);
void		print_opt_counts2(t_options *opt);
void 		rotate_direction(t_stack *a, t_options *opt, int target_pos, t_node *node);
void  		sort_rotate_push_b(t_stack *a, t_stack *b, t_options *opt, t_node *node);


#endif
