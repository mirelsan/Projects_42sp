/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_strjoin.c                                      :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/24 13:18:14 by username         #+#    #+#              */
/*   Updated: 2026/05/25 12:32:39 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	size_t	len_s1;
	size_t	len_s2;
	char	*str_result;

	if (!s1 || !s2)
		return (NULL);
	len_s1 = ft_strlen(s1);
	len_s2 = ft_strlen(s2);
	str_result = malloc(len_s1 + len_s2 + 1);
	if (!str_result)
		return (NULL);
	ft_memcpy(str_result, s1, len_s1);
	ft_memcpy(str_result + len_s1, s2, len_s2);
	str_result[len_s1 + len_s2] = '\0';
	return (str_result);
}
