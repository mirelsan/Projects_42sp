/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 20:18:39 by username          #+#    #+#             */
/*   Updated: 2026/05/30 18:32:26 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_atoi(const char *npr)
{
	int			sign;
	long int	sum;
	int			i;

	sum = 0;
	sign = 1;
	i = 0;
	while (npr[i] == ' ' || (npr[i] >= 9 && npr[i] <= 13))
	{
		i++;
	}
	if (npr[i] == '-')
	{
		sign *= -1;
		i++;
	}
	else if (npr[i] == '+')
		i++;
	while (npr[i] >= '0' && npr[i] <= '9')
	{
		sum = (npr[i] - '0') + (sum * 10);
		i++;
	}
	return ((long)sum * sign);
}
