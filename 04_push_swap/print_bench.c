/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   print_bench.c                                     :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/29 00:08:31 by username         #+#    #+#              */
/*   Updated: 2026/06/29 01:51:11 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	print_strategy(int mode)
{
	if (mode == SIMPLE)
		write(2, "[bench] strategy: Simple /O(n^2)\n", 33);
	else if (mode == MEDIUM)
		write(2, "[bench] strategy: Medium /O(n*sqrt(n))\n", 39);
	else if (mode == COMPLEX)
		write(2, "[bench] strategy: Complex /O(n log n)\n", 38);
	else
		write(2, "[bench] strategy: Adaptive /O(n*sqrt(n))\n", 41);
}

void	print_bench(t_options *opt)
{
	if (!opt)
		return ;
	print_disorder(opt->disorder_value);
	print_strategy(opt->mode);
	print_total_ops(opt);
	print_opt_counts(opt);
	print_opt_counts2(opt);
}

void	print_total_ops(t_options *opt)
{
	int	total_opt;
	int	i;

	i = 0;
	total_opt = 0;
	while (i < 11)
	{
		total_opt += opt->counts[i];
		i++;
	}
	write(2, "[bench] total_ops: ", 19);
	ft_putnbr_fd(total_opt, 2);
	write(2, "\n", 1);
}

void	print_opt_counts(t_options *opt)
{
	write(2, "[bench] sa: ", 12);
	ft_putnbr_fd(opt->counts[SA], 2);
	write(2, " sb: ", 5);
	ft_putnbr_fd(opt->counts[SB], 2);
	write(2, " ss: ", 5);
	ft_putnbr_fd(opt->counts[SS], 2);
	write(2, " pa: ", 5);
	ft_putnbr_fd(opt->counts[PA], 2);
	write(2, " pb: ", 5);
	ft_putnbr_fd(opt->counts[PB], 2);
	write(2, "\n", 1);
}

void	print_opt_counts2(t_options *opt)
{
	write(2, "[bench] ra: ", 12);
	ft_putnbr_fd(opt->counts[RA], 2);
	write(2, " rb: ", 5);
	ft_putnbr_fd(opt->counts[RB], 2);
	write(2, " rr: ", 5);
	ft_putnbr_fd(opt->counts[RR], 2);
	write(2, " rra: ", 6);
	ft_putnbr_fd(opt->counts[RRA], 2);
	write(2, " rrb: ", 6);
	ft_putnbr_fd(opt->counts[RRB], 2);
	write(2, " rrr: ", 6);
	ft_putnbr_fd(opt->counts[RRR], 2);
	write(2, "\n", 1);
}
