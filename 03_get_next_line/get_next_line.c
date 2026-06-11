/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 23:15:13 by username          #+#    #+#             */
/*   Updated: 2026/06/11 14:34:08 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*get_next_line(int fd)
{
	static char	*stash;
    char    *next_line;
    size_t len_before;
    size_t len_after;

    if(fd < 0)
        return(NULL);

    while(ft_verify_stash(stash) != 1 )
    {
        if(stash == NULL)
            len_before = 0;
        else
            len_before = ft_strlen(stash);
        stash = ft_append_stash(stash, fd);

        if(stash == NULL)
            return(NULL);
            
        len_after = ft_strlen(stash);
        if(len_before == len_after)
            break ;    
    }
    next_line = ft_fetch_line(&stash);
    return(next_line);
}
