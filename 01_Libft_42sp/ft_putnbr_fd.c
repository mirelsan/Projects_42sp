/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_putnbr_fd.c                                    :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/27 15:02:01 by username         #+#    #+#              */
/*   Updated: 2026/05/29 12:47:10 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

void	ft_putnbr_fd(int n, int fd)
{
	long int	long_int;

	long_int = n;
	if (n < 0)
		ft_putchar_fd('-', 1);
	long_int *= -1;
	if (n > 9)
	{
		ft_putnbr_fd(long_int / 10, fd);
		ft_putchar_fd(long_int % 10 + '0', fd);
	}
}
