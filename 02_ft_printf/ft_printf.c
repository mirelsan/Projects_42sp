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
    int chara_print;
    char c;
    char *str;

    chara_print = 0;
    
    va_list list_of_args;
    
    if(format == NULL)
    return (-1);
    
    va_start(list_of_args, format);

    while(*format)
    {
        if(*format != '%')
        {
            write(1, format, 1);
            chara_print++;
        }
        else
        {
            format++;
            if(*format == '\0')
                break;
        
            if(*format == '%')
            {
                write(1, format, 1);
                chara_print++;
            }
            else if(*format == 'c')
            {   
                c = va_arg(list_of_args, int);
                write(1, &c, 1);
                chara_print++;
            }
            else if(*format == 's')
            {
                *str = va_arg(list_of_args, char*);
                int str_len;

                str_len = 0;
                while(str[str_len] != '\0')
                str_len++;

                write(1, str, str_len);
                chara_print +- str_len;
            }
        }  
        format++;     
    }

    va_end(list_of_args);
}