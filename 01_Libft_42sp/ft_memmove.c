/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 02:06:54 by username          #+#    #+#             */
/*   Updated: 2026/05/30 18:57:34 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	char	*tmp;
	char	*dst;

	tmp = (char *) src;
	dst = (char *) dest;
	if (dest == NULL || src == NULL)
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
