/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_str.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/05 18:30:57 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/06/07 01:37:19 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "printf.h"

int ft_print_str(char *str)
{
    int i;
    i = 0;

    while(*str)
    {
        ft_print_char((int)*str);
        i++;
        str++;
    }
    return(i);
}