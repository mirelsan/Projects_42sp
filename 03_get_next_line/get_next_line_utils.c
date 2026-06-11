/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 23:15:11 by username          #+#    #+#             */
/*   Updated: 2026/06/11 14:38:20 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//1. stash has \n? Yes -> fetch and return
//No -> continue to read the file

//2. Read something? append to the stash and go back to 1
// in function read() -> returned 0? -> return what the stash has, (or NULL
//if it's empty)

#include "get_next_line.h"

int	ft_verify_stash(char *stash)
{
	if (stash == NULL)
		return (2);
	while (*stash != '\n' && *stash != '\0')
	{
		++stash;
	}
	if (*stash == '\n')
		return (1);
	return (0);
}

char	*ft_append_stash(char *stash, int fd)
{
	int		bytes;
	char	*buffer;
	char	*result;

	buffer = malloc(BUFFER_SIZE + 1);
	while (1)
	{
		bytes = read(fd, buffer, BUFFER_SIZE);
        buffer[bytes] = '\0';
		if (bytes == -1)
		{
			free(buffer);
			return (NULL);
		}
		if (bytes == 0)
		{
			free(buffer);
			return (stash);
		}
		result = ft_strjoin(stash, buffer);
		free(stash);
		stash = result;
		if (ft_strchr(stash, '\n') != NULL)
		{
			free(buffer);
			return (stash);
		}
	}
	free(buffer);
}

char	*ft_fetch_line(char **stash)
{
	int		i;
	char	*new_strline;
	char	*the_rest;

	i = 0;
	while ((*stash)[i] != '\n' && (*stash)[i] != '\0')
	{
		++i;
	}
	if ((*stash)[i] == '\n')
		++i;
	new_strline = ft_substr(*stash, 0, i);
	the_rest = ft_substr(*stash, i, ft_strlen(*stash + i));
	free(*stash);
	*stash = the_rest;
	return (new_strline);
}
char    *ft_strjoin(char const *s1, char const *s2)
{
    size_t    len_s1;
    size_t    len_s2;
    char    *str_result;
    if (s1 == NULL)
         len_s1 = 0;
    else
    len_s1 = ft_strlen(s1);
    len_s2 = ft_strlen(s2);
    str_result = malloc(len_s1 + len_s2 + 1);
    if (!str_result)
        return (NULL);
    if(s1 != NULL)
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