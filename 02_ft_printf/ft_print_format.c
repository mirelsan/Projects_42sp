/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_format.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 23:30:19 by codespace         #+#    #+#             */
/*   Updated: 2026/06/07 01:36:12 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int ft_print_format(char specifier, va_list)
{
    int count;
    va_list ap;

    count = 0;

    if(specifier == 'c')
        count += print_char(va_arg(ap, int));
    if(specifier == 's')
        count += ft_print_str(va_arg(ap, char *));
    if(specifier == 'd')
        count += ft_print_hex(va_arg(ap, int), 10);
    if(specifier == 'x')
        count += ft_print_hex(va_arg(ap, unsigned int), 16);
    else
        count += write(1, &specifier, 1);
    return count;        
}