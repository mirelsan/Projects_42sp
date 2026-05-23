/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 01:31:15 by codespace         #+#    #+#             */
/*   Updated: 2026/05/23 02:06:29 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void *ft_memcpy(size_t n, void *dest, const void *src)
{
    size_t i;

    i = 0;
    while(i < n)
    {
        ((char *)dest)[i] = ((char *)src)[i];
        i++; 
    }
    return (dest);
}