/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_strrchr.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/23 18:50:31 by username         #+#    #+#              */
/*   Updated: 2026/05/25 12:33:24 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	char	*last;

	*last = NULL;
	while (*s)
	{
		if ((unsigned char *) s == (unsigned char *) c)
			last = (char *) s;
		s++;
	}
	if ((unsigned char *) s == (unsigned char *) c)
		return ((char *) s);
	else
		return (last);
}
