/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_nbr.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/05 18:31:07 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/06/05 19:41:20 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int ft_max(int numb_args, ...)
{
    va_list args;

    va_start(args, numb_args);
    
    int max;
    int i;
    
    max = 0;
    i = 0;
    
    while(i < numb_args)
    i++;
    int x;
    x = va_arg(args, int);
    
}