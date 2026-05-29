/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_itoa.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/26 23:49:44 by username         #+#    #+#              */
/*   Updated: 2026/05/28 14:20:06 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_is_negative(int n)
{
	if (n < 0)
		return (1);
	else
		return (0);
}

size_t	ft_count_digits(size_t n)
{
	size_t	i;

	if (n == 0)
		return (1);
	i = 0;
	while (n > 0)
	{
		n /= 10;
		i++;
	}
	return (i);
}

char	*ft_itoa(int n)
{
	char			*str;
	unsigned int	i;
	long int		number;
	unsigned int	count_digits;
	int				is_neg;

	i = 0;
	is_neg = ft_is_negative(n);
	number = n;
	if (is_neg)
		number *= -1;
	count_digits = ft_count_digits(n);
	str = (malloc(count_digits + is_neg + 1));
	if (!str)
		return (NULL);
	if (i == 1)
		str[0] = '-';
	str[count_digits + i] = '\0';
	while (count_digits > 0)
	{
		str[(count_digits - 1) + i] = (number % 10) + '0';
		number /= 10;
		count_digits--;
	}
	return (str);
}
