/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_split.c                                        :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/25 01:31:23 by username         #+#    #+#              */
/*   Updated: 2026/05/25 13:08:34 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_c_split(char const *s, char c)
{
	int	i;
	int	words;

	i = 0;
	words = 0;
	while (s[i])
	{
		if (s[i] != 'c')
		{
			words++;
			while (s[i] && s[i] != 'c')
				i++ :
		}
		else
			i++;
	}
	return (words);
}

static int	ft_splitter(void)
