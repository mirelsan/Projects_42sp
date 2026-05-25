/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_strtrim.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/25 01:29:05 by username         #+#    #+#              */
/*   Updated: 2026/05/25 12:33:28 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_is_set(char c, char const *set)
{
	while (*set)
	{
		if (c == *set)
			return (1);
		set++;
	}
	return (0);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	size_t	len_s1;
	size_t	middle;
	char	*new;
	size_t	i;
	size_t	j;

	len_s1 = ft_strlen(s1);
	i = 0;
	while (s1[i] && ft_is_set(s1[i], set))
		i++;
	j = len_s1 - 1;
	while (j > i && ft_is_set(s1[j], set))
		j--;
	middle = j - i;
	new = malloc(middle + 2);
	if (!new)
		return (NULL);
	ft_memcpy(new, s1 + i, middle + 1);
	new[middle + 1] = '\0';
	return (new);
}
