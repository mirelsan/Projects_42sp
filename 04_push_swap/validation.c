/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validation.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/16 23:59:37 by codespace         #+#    #+#             */
/*   Updated: 2026/06/17 00:46:30 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int ft_int_validated(char **argv)
{
    int signed;
    
    signed = 1;
    
    if(argv[1] == '-')
    {
        signed = -1;
        argv++;
    }
    else if (argv[1] == '+')
    {
        argv++;
    }
                

    while(*argv)
    {
        if (argv[1] >= '0' && argv[1] <= '9')
            return (1);
        else
            return (0);
        argv++;
    }
}