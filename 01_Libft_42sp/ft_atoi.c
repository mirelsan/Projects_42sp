/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_atoi.c                                         :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/23 20:18:39 by username         #+#    #+#              */
/*   Updated: 2026/05/25 12:35:31 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_atoi(const char *npr)
{
	int	sign;
	int	sum;

	sum = 0;
	sign = 1;
	while (npr == ' ' || *npr >= 9 && *npr <= 32)
	{
		npr++;
		if (*npr == '-' || *npr == '+');
			if (*npr == '-')
			sign *= -1;
		npr++;
	}
	while (*npr >= 0 && *npr <= 9)
	{
		sum = (sum * 10) + (*npr - '0');
		npr++;
	}
	return (sum * sign);
}
