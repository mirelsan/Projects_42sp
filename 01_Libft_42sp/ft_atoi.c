/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 20:18:39 by username          #+#    #+#             */
/*   Updated: 2026/05/29 12:59:46 by mirelapitt       ###   ########.fr       */
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
		if (*npr == '-' || *npr == '+')
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
