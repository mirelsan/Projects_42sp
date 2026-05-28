/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstiter.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/28 02:23:15 by codespace         #+#    #+#             */
/*   Updated: 2026/05/28 02:23:38 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

    
#include "libft.h"

void        ft_lstiter(t_list *lst, void (*f)(void *))
{
    if(lst == NULL)
        return ;
        
    t_list *tmp;
    
    tmp = lst;
    while(tmp != NULL)
    {
        f(tmp->content);
        tmp = tmp->next;
    }
}

    
