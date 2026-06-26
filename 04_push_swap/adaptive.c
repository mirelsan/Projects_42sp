/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   adaptive.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 01:54:17 by codespace         #+#    #+#             */
/*   Updated: 2026/06/25 23:52:05 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void sort_adaptative(t_stack *a, t_stack *b, t_options *opt)
{
	double d;

	if (!a || !b)
		return ;
	d = disorder(a);
	if (d < 0.2)
		sort_n2(a, b, opt);
	else if (d < 0.5)
		sort_chunk(a, b, opt);
	else
		sort_radix(a, b, opt);
}
