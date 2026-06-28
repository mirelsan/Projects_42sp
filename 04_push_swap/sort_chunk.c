/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_chunk.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 22:07:15 by codespace         #+#    #+#             */
/*   Updated: 2026/06/28 20:49:25 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void sort_chunk(t_stack *a, t_stack *b, t_options *opt)
{
    int min;
    int num_chunks;
    int width;
    int i;
    int pos;
    t_node *node;

    min = ft_min(a);
    num_chunks = ft_sqrt(a->size);
    width = width_range(a, num_chunks);
    i = 0;
    
    while(i < num_chunks)
    {
        node = find_min_in_chunk(a, min, width, i);
        while(node != NULL)
        {
            pos = get_position(a, node);
            if(pos <= a->size / 2)
            {
                while(a->head != node)
                    ra(a, opt);
            }
            else
            {
                while(a->head != node)
                    rra(a, opt);
            }
            pb(a, b, opt);
            node = find_min_in_chunk(a, min, width, i);
        }
        i++;
    }
    while(b->size > 0)
    pa(a, b, opt);    
}

t_node *find_min_in_chunk(t_stack *a, int min, int width, int chunk_idx)
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
            if(node == NULL || curr->data < node->data)
            {
                node = curr;
            }
        }
        curr = curr->next;
    }
    return(node);
}
int get_position(t_stack *a, t_node *target)
{
    t_node *curr;
    int pos;
    
    curr = a->head;
    pos = 0;

    while(curr != target)
    {
       ++pos; 
       curr = curr->next;
    }
    return(pos);
}
