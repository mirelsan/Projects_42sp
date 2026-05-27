/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 14:35:43 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/05/27 14:50:55 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "libft.h"

void	ft_putstr_fd(char *s, int fd)
{
    int i;
    i = 0;

    if(!s)
        return ;

        write(fd, s, ft_strlen(s));
}
