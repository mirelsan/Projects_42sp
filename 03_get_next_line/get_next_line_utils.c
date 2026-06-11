/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   get_next_line_utils.c                             :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/09 23:15:11 by username         #+#    #+#              */
/*   Updated: 2026/06/11 14:56:25 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

//1. stash has \n? Yes -> fetch and return
//No -> continue to read the file

//2. Read something? append to the stash and go back to 1
// in function read() -> returned 0? -> return what the stash has, (or NULL
//if it's empty)

#include "get_next_line.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	size_t	len_s1;
	size_t	len_s2;
	char	*str_result;

	if (s1 == NULL)
		len_s1 = 0;
	else
		len_s1 = ft_strlen(s1);
	len_s2 = ft_strlen(s2);
	str_result = malloc(len_s1 + len_s2 + 1);
	if (!str_result)
		return (NULL);
	if (s1 != NULL)
		ft_memcpy(str_result, s1, len_s1);
	ft_memcpy(str_result + len_s1, s2, len_s2);
	str_result[len_s1 + len_s2] = '\0';
	return (str_result);
}

char	*ft_strchr(const char *s, int c)
{
	int				i;
	unsigned char	ch;

	i = 0;
	ch = c;
	if (ch == '\0')
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

size_t	ft_strlen(const char *s)
{
	size_t	i;

	i = 0;
	while (s[i] != '\0')
		i++;
	return (i);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*substr;
	size_t	s_len;

	if (!s)
		return (NULL);
	s_len = ft_strlen(s);
	if (s_len < start)
	{
		substr = ((char *) malloc(sizeof(char) * 1));
		if (!substr)
			return (NULL);
		substr[0] = '\0';
		return (substr);
	}
	if (len > s_len - start)
		len = s_len - start;
	substr = malloc(len + 1);
	if (!substr)
		return (NULL);
	ft_memcpy(substr, s + start, len);
	substr[len] = '\0';
	return (substr);
}

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	size_t	i;

	i = 0;
	if (dest == NULL && src == NULL)
		return (NULL);
	while (i < n)
	{
		((char *) dest)[i] = ((char *) src)[i];
		i++;
	}
	return (dest);
}
