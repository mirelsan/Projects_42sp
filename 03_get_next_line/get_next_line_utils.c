/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 23:15:11 by codespace         #+#    #+#             */
/*   Updated: 2026/06/10 15:55:23 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


//1. stash has \n? Yes -> fetch and return
                   //No -> continue to read the file

//2. Read something? append to the stash and go back to 1
// in function read() -> returned 0? -> return what the stash has, (or NULL 
//if it's empty)                  

#include "get_next_line.h"

int ft_verify_stash(char *stash)
{
    int i;
    i = 0;
    
    while(*stash)
    {
        if(*stash != '\n')
        {
            ++stash;
        }
    }
    return(1);
}

char *ft_append_stash(char *stash, int fd)
{
        
}

char *ft_fetch_line(char *stash, int fd)
{
    
}

