/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_medium.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 22:07:15 by codespace         #+#    #+#             */
/*   Updated: 2026/06/24 00:18:36 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void sort_medium(t_stack *a, t_stack *b)
{
    int min;
    int max;
    int num_chunks;
    int width;
    int i;

    min = ft_min(a);
    max = ft_max(a);
    num_chunks = ft_sqrt(a->size);
    width = width_range(a, num_chunks);
    i = num_chunks - 1;

    while(i >= 0)
    {
        if()
    }
}

t_node *find_max_in_chunk(t_stack *a, int min, int width, int chunk_idx)
{
    t_node *curr;
    t_node *node;
    int     found;

    node = NULL;
    curr = a->head;

    while(curr != NULL)
    {
        found = ft_chunk(min, width, curr->data);

        if(chunk_idx == found)
        {
            if(node == NULL || curr->data > node->data)
            {
                node = curr;
            }
        }
        curr = curr->next;
    }
    return(node);
}
