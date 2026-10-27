/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:26:43 by mirelsan          #+#    #+#             */
/*   Updated: 2026/10/26 21:26:44 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "coders.h"
#include <stdio.h>
#include <stdlib.h>

void    error_exit(const char *error)
{
    printf("%s\n", error);
    exit(EXIT_FAILURE);
}

