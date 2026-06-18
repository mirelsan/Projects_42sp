/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_d.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelsan <mirelsan@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/07 23:17:20 by username          #+#    #+#             */
/*   Updated: 2026/06/08 15:53:29 by mirelsan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	print_d(long int number)
{
	long int	i;

	i = 0;
	if (number < 0)
	{
		write(1, "-", 1);
		i++;
		i += ft_putnbr_fd(-number);
	}
	if (number > 0)
		i += ft_putnbr_fd(number);
	if (number == 0)
		i += print_char('0');
	return (i);
}

int	ft_putnbr_fd(unsigned long int n)
{
	unsigned long int	i;

	i = 0;
	if (n < DECIMAL_BASE)
		i += print_char(n + '0');
	if (n >= DECIMAL_BASE)
	{
		i += ft_putnbr_fd(n / DECIMAL_BASE);
		i += print_char((n % DECIMAL_BASE) + '0');
	}
	return (i);
}
