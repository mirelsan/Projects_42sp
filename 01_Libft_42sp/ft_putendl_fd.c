/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putendl_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/27 14:54:03 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/05/27 15:00:47 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "libft.h"

void	ft_putendl_fd(char *s, int fd)
{
    size_t len;
    
    len = ft_strlen(s);
    write(fd, s, len);
    write(fd, "\n", 1); 
}
