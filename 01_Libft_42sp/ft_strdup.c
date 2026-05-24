/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 12:03:37 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/05/24 12:11:02 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


char        *ft_strdup(const char *s)
{
     char *dest;
     int i;
     int s_len;
     
     
     s_len = ft_strlen(s);
     dest = malloc(s_len + 1);
     
     if(dest == NULL)
         return (NULL);
     i = 0;
     while(i < s_len)
     {
         dest[i] = s[i];
         i++;
     }
     dest[i] = '\0';
     return(dest);
}