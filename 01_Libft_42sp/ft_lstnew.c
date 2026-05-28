/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 22:16:43 by codespace         #+#    #+#             */
/*   Updated: 2026/05/28 00:27:48 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstnew(void *content)
{
    t_list *new_item;

    new_item = malloc(sizeof(t_list));
    if(!new_item)
        return(NULL);
   
    new_item->content = content;
    new_item->next = NULL;    
  return(new_item);      
}
