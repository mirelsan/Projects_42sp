/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_memmove.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/23 02:06:54 by username         #+#    #+#              */
/*   Updated: 2026/05/25 12:34:46 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	char	*tmp;
	char	*dst;

	*tmp = (char *) src;
	*dst = (char *) dest;
	if (tmp < dst)
	{
		while (n--)
		{
			dest[n] = tmp[n];
		}
	}
	else
		ft_memmove(dest, tmp, n);
	return (dest);
}
