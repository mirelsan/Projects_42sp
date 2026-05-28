/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstlast.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/28 01:44:15 by codespace         #+#    #+#             */
/*   Updated: 2026/05/28 01:52:15 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstlast(t_list *lst)
{
    int i;
    i = 0;

    if(lst == NULL)
        return(NULL);

    t_list *tmp;
    tmp = lst;

    while(tmp->next != NULL)
    {
        tmp = tmp->next;
    }
    return(tmp);
}
