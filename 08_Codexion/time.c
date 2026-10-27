/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:26:33 by mirelsan          #+#    #+#             */
/*   Updated: 2026/10/26 21:26:34 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "coders.h"

// É usado por todo mundo (coder, monitor, logger)

// Function of absolute time
long    get_time_ms(void)
{
    struct timeval  tv;

    if (gettimeofday(&tv, NULL) == -1)
    {
        error_exit("Impossible to read the time");
        return (-1);
    }
    return ((tv.tv_sec * 1000) + (tv.tv_usec / 1000));
}

// Function of elapsed time

long get_elapsed_time(long start_simulation)
{
    return (get_time_ms() - start_simulation);
}