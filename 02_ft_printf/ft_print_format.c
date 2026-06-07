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

int ft_print_format(char specifier, va_list ap)
{
    int count;

    count = 0;

    if(specifier == 'c')
        count += print_char(va_arg(ap, int));
    else if(specifier == 's')
        count += ft_print_str(va_arg(ap, char *));
    else if(specifier == 'd' || specifier == 'i')
        count += print_d(va_arg(ap, int));
    else if(specifier == 'x' || specifier == 'X')
        count += ft_print_hex(va_arg(ap, unsigned int), specifier);
    else if(specifier == 'u')
        count += print_u(va_arg(ap, unsigned int));
    else if(specifier == 'p')
        count += print_p(va_arg(ap, void *));
    else
        count += write(1, &specifier, 1);
    return count;        
}