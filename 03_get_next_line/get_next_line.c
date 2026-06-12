/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   get_next_line.c                                   :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/06/09 23:15:13 by username         #+#    #+#              */
/*   Updated: 2026/06/12 12:39:38 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*get_next_line(int fd)
{
	static char	*stash;
	char		*next_line;

	if (fd < 0)
		return (NULL);
	stash = ft_read_stash(stash, fd);
	if (!stash || *stash == '\0')
	{
		free(stash);
		return (NULL);
	}
	next_line = ft_fetch_line(&stash);
	return (next_line);
}

char	*ft_read_stash(char *stash, int fd)
{
	size_t	len_before;
	size_t	len_after;

	while (ft_verify_stash(stash) != 1)
	{
		if (stash == NULL)
			len_before = 0;
		else
			len_before = ft_strlen(stash);
		stash = ft_append_stash(stash, fd);
		if (stash == NULL)
			return (NULL);
		len_after = ft_strlen(stash);
		if (len_before == len_after)
		{
			if (!stash || *stash == '\0')
			{
				free(stash);
				stash = NULL;
				return (NULL);
			}
			break ;
		}
	}
	return (stash);
}

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
		if (bytes <= 0)
		{
			free(buffer);
			if (bytes == -1)
				return (free(stash), NULL);
			return (stash);
		}
		buffer[bytes] = '\0';
		result = ft_strjoin(stash, buffer);
		free(stash);
		stash = result;
		if (ft_strchr(stash, '\n') != NULL)
		{
			free(buffer);
			return (stash);
		}
	}
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
