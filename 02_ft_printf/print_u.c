/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   print_u.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/07 23:38:30 by username         #+#    #+#              */
/*   Updated: 2026/06/08 15:42:46 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	print_u(unsigned int number)
{
	int	count;

	count = 0;
	if (number >= DECIMAL_BASE)
		count += print_u(number / DECIMAL_BASE);
	count += print_char((number % DECIMAL_BASE) + '0');
	return (count);
}
