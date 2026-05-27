/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 02:07:57 by codespace         #+#    #+#             */
/*   Updated: 2026/05/27 02:18:07 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char));
{
    size_t = length;
    char *new_str;

    if(!s)
        return(NULL);

     length = ft_strlen(s);
     
     new_str = (char *)malloc(sizeof(char *) length + 1);

     if(!new_str)
        return(NULL);
    
        new_str = '\0';
}

