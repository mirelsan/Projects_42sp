/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstsize.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/28 01:22:34 by codespace         #+#    #+#             */
/*   Updated: 2026/05/28 01:42:00 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "libft.h"

int		ft_lstsize(t_list *lst)
{

    int i;
    t_list *tmp;
   
    i = 0;
    tmp = lst;
    
    while(tmp != NULL)
    {
        i++;
        tmp = tmp->next;
    }
    return(i);
}

