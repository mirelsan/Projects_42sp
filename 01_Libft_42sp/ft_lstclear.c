/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstclear.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/28 02:13:03 by codespace         #+#    #+#             */
/*   Updated: 2026/05/28 02:22:06 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstclear(t_list **lst, void (*del)(void *))
{
    if(*lst == NULL)
        return ;

    t_list *ptr;
    
    while(*lst)
    {
        ptr = (*lst)->next;
        ft_lstdelone(lst, del);
        lst = ptr;

    }
    *lst == NULL;
}
