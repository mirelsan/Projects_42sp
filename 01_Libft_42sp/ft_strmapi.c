/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_strmapi.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/27 02:07:57 by username         #+#    #+#              */
/*   Updated: 2026/05/28 14:22:36 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	size_t	length;
	char	*new_str;
	int		i;

	if (!s || !f)
		return (NULL);
	length = ft_strlen(s);
	new_str = (char *) malloc(sizeof(char) * (length + 1));
	if (!new_str)
		return (NULL);
	i = 0;
	while (length > '0')
	{
		new_str[i] = f(i, new_str[i]);
		i++;
	}
	new_str = '\0';
	return (new_str);
}
