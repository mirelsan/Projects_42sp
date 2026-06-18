/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_memmove.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/23 02:06:54 by username         #+#    #+#              */
/*   Updated: 2026/06/01 14:15:09 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	char	*tmp;
	char	*dst;

	tmp = (char *) src;
	dst = (char *) dest;
	if (dest == NULL && src == NULL)
		return (dest);
	if (tmp < dst)
	{
		while (n--)
		{
			dst[n] = tmp[n];
		}
	}
	else
	{
		while (n--)
		{
			*dst = *tmp;
			dst++;
			tmp++;
		}
	}
	return (dest);
}
