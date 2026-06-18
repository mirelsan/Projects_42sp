/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 15:02:01 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/05/30 16:54:59 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static void	ft_putnbr_recursive(long int n, int fd)
{
	if (n > 9)
	{
		ft_putnbr_fd(n / 10, fd);
		ft_putchar_fd(n % 10 + '0', fd);
	}
}

void	ft_putnbr_fd(int n, int fd)
{
	long int	long_int;

	long_int = n;
	if (long_int < 0)
	{
		ft_putchar_fd('-', fd);
		long_int *= -1;
	}
	if (long_int > 9)
	{
		ft_putnbr_recursive(long_int, fd);
	}
	else
		ft_putchar_fd(long_int % 10 + '0', fd);
}
