/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap_bonus.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/28 14:29:24 by username          #+#    #+#             */
/*   Updated: 2026/05/30 19:25:09 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*new_lst;
	t_list	*new_node;

	if (lst == NULL)
		return (NULL);
	new_node = ft_lstnew((*f)(lst->content));
	if (new_node == NULL)
	{
		return (NULL);
	}
	new_lst = new_node;
	lst = lst->next;
	while (lst)
	{
		new_node->next = ft_lstnew((*f)(lst->content));
		if (new_node->next == NULL)
		{
			ft_lstclear(&new_lst, del);
			return (NULL);
		}
		new_node = new_node->next;
		lst = lst->next;
	}
	return (new_lst);
}
