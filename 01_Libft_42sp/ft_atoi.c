/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 20:18:39 by username          #+#    #+#             */
/*   Updated: 2026/05/30 15:33:08 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_atoi(const char *npr)
{
	int	sign;
	int	sum;
	int	i;

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
	if (npr[i] == '+')
		i++;
	while (npr[i] >= '0' && npr[i] <= '9')
	{
		sum = (npr[i] - '0') + (sum * 10);
		i++;
	}
	return (sum * sign);
}
