/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   push_swap.h                                       :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/15 02:10:09 by username         #+#    #+#              */
/*   Updated: 2026/06/30 14:59:07 by username        ###   ########.fr        */
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
}	t_mode;

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
}	t_operations;

typedef struct s_options
{
	int		bench;
	int		start_index;
	int		counts[11];
	int		min;
	int		width;
	double	disorder_value;
	t_mode	mode;
}	t_options;

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
void		sort_radix(t_stack *a, t_stack *b, t_options *opt);
void		process_bit(t_stack *a, t_stack *b, int bit, t_options *opt);
int			has_bit(int n, int bit);
int			max_bits(t_stack *a);
int			is_sorted(t_stack *stack);
void		sort_3(t_stack *a, t_options *opt);
void		extract_top(t_stack *a, t_options *opt);
void		sort_n2(t_stack *a, t_stack *b, t_options *opt);
double		disorder(t_stack *stack);
int			ft_min(t_stack *a);
int			ft_max(t_stack *a);
int			ft_sqrt(int n);
int			width_range(t_stack *a, int num_chunks);
int			ft_chunk(int min, int width_range, int value);
void		ft_set_index(t_stack *a);
void		sort_chunk(t_stack *a, t_stack *b, t_options *opt);
int			ft_strncmp(const char *s1, const char *s2, size_t n);
void		sort_adaptative(t_stack *a, t_stack *b, t_options *opt);
int			parse_options(int argc, char **argv, t_options *opt);
int			is_valid_flag(char *arg);
t_stack		*select_and_sort(t_stack *a, t_stack *b, t_options *opt);
size_t		ft_strlen(const char *s);
void		print_total_ops(t_options *opt);
void		print_opt_counts(t_options *opt);
void		print_opt_counts2(t_options *opt);
void		rotate_direction(t_stack *a, t_options *opt, int target_pos, t_node *node);
int			apply_flag(char **argv, t_options *opt, int i);
void		ft_putnbr_fd(int n, int fd);
void		print_disorder(double disorder_value);
void		print_strategy(int mode);
void		print_bench(t_options *opt);
void		ft_add_tail(t_stack *stack, t_node *new);
t_stack		*ignore_flags(char **argv, int start_index, t_stack *stack);
int			execution(t_options *opt, t_stack *stack_a, t_stack *stack_b);
int			ft_max(t_stack *a);
void		process_chunk(t_stack *a, t_stack *b, int chunk_idx, t_options *opt);
void		extract_max_to_top_b(t_stack *b, t_options *opt);
int			find_max_pos_b(t_stack *b);
int			find_closest_in_chunk(t_stack *a, int chunk_idx, t_options *opt);

#endif
