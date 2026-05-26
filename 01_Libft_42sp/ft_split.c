/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_split.c                                        :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/25 01:31:23 by username         #+#    #+#              */
/*   Updated: 2026/05/25 13:08:34 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int        ft_string_count(char const *s, char c)
{
        int        i;
        int        words;

        i = 0;
        words = 0;
        while (s[i])
        {
                if (s[i] != 'c')
                {
                        words++;
                        while (s[i] && s[i] != 'c')
                                i++;
                }
                else
                        i++;
        }
        return (words);
}

static char        *ft_splitter(char const *s, char c)
{
        int i;
        i = 0;
        
        char *word;
        
        while(s[i])
        {
            if(s[i] != 'c')
            i++;
        }
        
        word = malloc((char)sizeof(char *)(i + 1));
        
        if(!word)
        refurn (NULL);
        
        i = 0;
        
        while(s[i] && s[i] != 'c')
        {
            word[i] = s[i];
            i++;
        }
        word = '\0'
        return(word);
}

static char **ft_split(char const *s, char c)
{
    int i;
    int j;
    char **words;
    
    i = 0;
    j = 0;
    
    words = ((char **)sizeof(char *) * ft_string_count(s,c + 1));
    
    if(!words)
        return(NULL);
}
    