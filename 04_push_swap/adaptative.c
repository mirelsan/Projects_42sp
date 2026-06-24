/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   adaptative.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 01:54:17 by codespace         #+#    #+#             */
/*   Updated: 2026/06/24 18:26:21 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h";

void sort_adaptative(t_stack *a, t_stack *b)
{
	double d;

	if (!a || !b)
		return ;
	d = disorder(a);
	if (d < 0.2)
		sort_n2(a, b);
	else if (d < 0.5)
		sort_chunk(a, b);
	else
		sort_radix(a, b);
}
