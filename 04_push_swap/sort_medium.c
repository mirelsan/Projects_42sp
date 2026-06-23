/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_medium.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 22:07:15 by codespace         #+#    #+#             */
/*   Updated: 2026/06/23 22:35:48 by codespace        ###   ########.fr       */
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

    i = 0;
    min = ft_min(a);
    max = ft_max(a);
    num_chunks = ft_sqrt(a->size);
    width = width_range(a, num_chunks);
}