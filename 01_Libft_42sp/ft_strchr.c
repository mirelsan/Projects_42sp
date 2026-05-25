/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_strchr.c                                       :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/23 18:33:17 by username         #+#    #+#              */
/*   Updated: 2026/05/25 12:34:32 by username        ###   ########.fr        */
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
		return ((char *) s + i++);
	}
	while (s[i])
	{
		if (s[i] == ch)
			return ((char *) s + i);
		i++;
	}
	return (NULL);
}
