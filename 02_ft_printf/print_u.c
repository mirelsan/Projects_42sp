/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_u.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/07 23:38:30 by codespace         #+#    #+#             */
/*   Updated: 2026/06/07 23:39:15 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int print_u(unsigned int number)
{
    int count;

    count = 0;
    if (number >= DECIMAL_BASE)
        count += print_u(number / DECIMAL_BASE);
    count += print_char((number % DECIMAL_BASE) + '0');
    return (count);
}