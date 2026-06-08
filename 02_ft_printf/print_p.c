/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_p.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/07 23:33:00 by codespace         #+#    #+#             */
/*   Updated: 2026/06/08 01:12:36 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int print_p(void *ptr)
{
    int count;

    count = 0;
    count += ft_print_str("0x");
    count += print_hex((unsigned long)ptr, 'x');
    return (count);
}