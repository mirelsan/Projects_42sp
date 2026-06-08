/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_str.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/05 18:30:57 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/06/08 00:59:48 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int ft_print_str(const char *str)
{
    int i;
    i = 0;

    if(str == NULL)
        str = "(null)";

    while(*str)
    {
        print_char((int)*str);
        i++;
        str++;
    }
    return(i);
}