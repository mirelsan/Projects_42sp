/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_chunk_utils.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 01:39:10 by codespace         #+#    #+#             */
/*   Updated: 2026/07/01 01:52:19 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	configure_max_chunks(t_stack *a)
{
	if (a->size > 100)
		return (11);
	return (5);
}

int	decide_position(int top_pos, int bot_pos, int size)
{
	if (top_pos == -1)
		return (-1);
	if (top_pos <= (size - bot_pos))
		return (top_pos);
	return (bot_pos);
}
