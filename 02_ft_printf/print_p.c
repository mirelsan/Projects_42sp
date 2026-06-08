/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   print_p.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/07 23:33:00 by username         #+#    #+#              */
/*   Updated: 2026/06/08 15:42:53 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	print_p(void *ptr)
{
	int	count;

	if (ptr == NULL)
		return (ft_print_str("(nil)"));
	count = 0;
	count += ft_print_str("0x");
	count += print_hex((unsigned long) ptr, 'x');
	return (count);
}
