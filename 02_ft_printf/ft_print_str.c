/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_str.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelsan <mirelsan@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/05 18:30:57 by username          #+#    #+#             */
/*   Updated: 2026/06/08 15:52:51 by mirelsan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_str(const char *str)
{
	int	i;

	i = 0;
	if (str == NULL)
		str = "(null)";
	while (*str)
	{
		print_char((int) * str);
		i++;
		str++;
	}
	return (i);
}
