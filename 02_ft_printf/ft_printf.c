/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelsan <mirelsan@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/31 13:26:40 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/06/06 16:01:46 by mirelsan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int ft_printf(const char *format, ...)
{
   va_list ap;
   int     count;

    count = 0;

    va_start(ap, format);

    while(format != '\0')  
    {
        if(format == '%')
            count += ft_print_format(*(++format), ap);
        else
            count += write(1, format, 1);
        ++format;    
    }
    va_end(ap);
    return(count);
}