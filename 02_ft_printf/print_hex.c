/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_hex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/05 18:31:09 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/06/08 01:23:51 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int print_hex(unsigned long int number, char type)
{
    int i;
    char *symbols;

    i = 0;

    if(type == 'X')
        symbols = "0123456789ABCDEF";
    else
    symbols = "0123456789abcdef";

    if (number >= HEX_BASE)
        i += print_hex(number / HEX_BASE, type);
    i += print_char(symbols[number % HEX_BASE]);
    return (i);
}
