/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 20:18:39 by username          #+#    #+#             */
/*   Updated: 2026/05/29 13:14:30 by mirelapitt       ###   ########.fr       */
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
		npr++;
		if (*npr == '-' || *npr == '+')
			if (*npr == '-')
				sign *= -1;
		npr++;
	}
	while (npr[i] >= '0' && npr[i] <= '9')
	{
		sum = (npr[i] - '0') + (sum * 10);
		i++;
	}
	return (sum * sign);
}
