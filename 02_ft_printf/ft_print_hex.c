/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_hex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelsan <mirelsan@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/05 18:31:09 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/06/06 15:20:19 by mirelsan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "printf.h"

int ft_print_hex(int n, int base)
{
    int i;
    char *symbols;

    i = 0;
    symbols = "0123456789abcdef";

    if(n < 0)
    {
        write(1, "-", 1);
        return ft_print_hex(-n, base) + 1;
    }
    else if (n < base)
    {
        print_char(symbols[n]);
    }
    else
    {
        i = ft_print_hex(n / base, base);
        return i + ft_print_hex(n % base, base);
    }
}