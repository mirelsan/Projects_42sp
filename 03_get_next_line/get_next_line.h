/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 23:15:15 by codespace         #+#    #+#             */
/*   Updated: 2026/06/10 15:09:49 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H

#ifndef BUFFER_SIZE
#define BUFFER_SIZE 3
#endif

#include <unistd.h>
#include <stdlib.h>

char *get_next_line(int fd);
int ft_verify_stash(char *stash);
char *ft_append_stash(char *stash, int fd);
char *ft_fetch_line(char *stash, int fd);

#endif