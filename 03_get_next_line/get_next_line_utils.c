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
    if(stash == NULL)
        return(2);

    while(*stash != '\n' && *stash != '\0')
    {
        ++stash;
    }
    if(*stash == '\n')
        return(1);
    return(0);
}

char *ft_append_stash(char *stash, int fd)
{
    int   bytes;
    char *buffer;
    char  *result;
  
    buffer = malloc(BUFFER_SIZE + 1);

    while(1)
      {
        bytes = read(fd, buffer, BUFFER_SIZE);
        if(bytes == -1)
       {
         free(buffer);
         return(NULL);
       }
        
      if(bytes == 0)
       {
         free(buffer);
         return(stash);
       }      
        result = ft_strjoin(stash, buffer);
        free(stash);
        stash = result;
        if (ft_strchr(stash, '\n') != NULL)
         { 
          free(buffer);
          return(stash);
         }
      }
      free(buffer);
}

char *ft_fetch_line(char **stash, int fd)
{    
    int i;
    char *new_strline;
    char *the_rest;
    
    i = 0;
    
    while((*stash)[i] != '\n' && (*stash)[i] != '\0')
    {
        ++i;
    }
    if((*stash)[i] == '\n')
        ++i;
    new_strline = ft_substr(*stash, 0, i);
    the_rest = ft_substr(*stash, i, ft_strlen(*stash + i));
    free(*stash);
    *stash = the_rest;
    return(new_strline);
}