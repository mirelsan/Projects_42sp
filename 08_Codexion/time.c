/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   time.c                                            :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/10/26 21:26:33 by username         #+#    #+#              */
/*   Updated: 2026/10/26 21:33:54 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

// É usado por todo mundo (coder, monitor, logger)

// Function of absolute time

long	get_time_ms(void)
{
	struct timeval	tv;

	if (gettimeofday(&tv, NULL) == -1)
	{
		error_exit("Impossible to read the time");
		return (-1);
	}
	return ((tv.tv_sec * 1000) + (tv.tv_usec / 1000));
}

// Function of elapsed time

long	get_elapsed_time(long start_simulation)
{
	return (get_time_ms() - start_simulation);
}
