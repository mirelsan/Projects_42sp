/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 02:07:57 by codespace         #+#    #+#             */
/*   Updated: 2026/05/29 13:49:55 by mirelapitt       ###   ########.fr       */
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
