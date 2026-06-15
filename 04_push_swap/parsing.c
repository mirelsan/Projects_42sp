/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/15 02:09:35 by codespace         #+#    #+#             */
/*   Updated: 2026/06/15 02:22:21 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


//1.parsing 2 cases: multi argvs -> already separated
//                   argv with spaces -> ft_split first to kill spaces
//then ft_atoi to convert string to int.

#include "push_swap.h"

int main(int argc, char *argv[])
{

    if(argc < 2)
        return(0);
    return(1);    

    while(**argv != '\0')
    {
        if(**argv == ' ')
            ft_split(argv);
    }
}

