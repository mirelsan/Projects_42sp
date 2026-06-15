/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   parsing.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/15 02:09:35 by username         #+#    #+#              */
/*   Updated: 2026/06/15 15:13:01 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

//1.parsing 2 cases: multi argvs -> already separated
//                   argv with spaces -> ft_split first to kill spaces
//then ft_atoi to convert string to int.

#include "push_swap.h"

int	main(int argc, char **argv)
{
	if (argc < 2)
		return (0);
	else
		(**argv == ' ');
	ft_split(argv);
}
