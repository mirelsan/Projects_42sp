/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/28 01:54:21 by codespace         #+#    #+#             */
/*   Updated: 2026/05/28 02:04:34 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_back(t_list **lst, t_list *new)
{
    t_list *last;
    
    if(*lst == NULL)
        *lst = new;
    else
    {
        last = ft_lstlast(*lst);
        last->next = new; 
   
        new->next = NULL;
    }
}
