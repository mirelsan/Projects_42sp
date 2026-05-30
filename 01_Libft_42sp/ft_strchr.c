/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 18:33:17 by username          #+#    #+#             */
/*   Updated: 2026/05/30 15:53:11 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strchr(const char *s, int c)
{
	int				i;
	unsigned char	ch;

	i = 0;
	ch = c;
	if (c == '\0')
	{
		i = ft_strlen(s);
		return ((char *) s + i);
	}
	while (s[i])
	{
		if (s[i] == ch)
			return ((char *) s + i);
		i++;
	}
	return (NULL);
}
