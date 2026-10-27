/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:24:35 by username          #+#    #+#             */
/*   Updated: 2026/10/27 02:40:38 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"

//EVEN ODD dongle assigment
// == to position
// DEADLOCK

static void	assign_dongles(t_coder *coder, t_dongle *dongle, int coder_position)
{
	int	coder_nbr;

	coder_nbr = coder->workspace->number_of_coders;
	coder->first_dongle = &dongle[(coder_position + 1) % coder_nbr];
	coder->second_dongle = &dongle[(coder_position)];
	if (coder->id % 2)
	{
		coder->first_dongle = &dongle[coder_position];
		coder->second_dongle = &dongle[(coder_position + 1) % coder_nbr];
	}
}

static void	coder_init(t_workspace *workspace)
{
	int		i;
	t_coder	*coder;

	i = -1;
	while (++i < workspace->number_of_coders)
	{
		coder = workspace->coders + i;
		coder->id = i + 1;
		coder->bournout = false;
		coder->number_compiles = 0;
		coder->workspace = workspace;
		coder->last_compile_time = workspace->start_simulation;
		safe_mutex_handle(&coder->progress_mutex, INIT);
		assign_dongles(coder, workspace->dongles, i);
	}
}

void	data_init(t_workspace *workspace)
{
	int	i;

	i = -1;
	workspace->end_simulation = false;
	safe_mutex_handle(&workspace->log_mutex, INIT);
	safe_mutex_handle(&workspace->end_mutex, INIT);
	workspace->coders = safe_malloc(sizeof(t_coder)
			*workspace->number_of_coders);
	workspace->dongles = safe_malloc(sizeof(t_dongle)
			*workspace->number_of_coders);
	while (++i < workspace->number_of_coders)
	{
		safe_mutex_handle(&workspace->dongles[i].dongle, INIT);
		workspace->dongles[i].dongle_id = i;
		workspace->dongles[i].in_use = false;
		workspace->dongles[i].available_at = 0;
		workspace->dongles[i].next_seq = 0;
		workspace->dongles[i].queue.size = 0;
		workspace->dongles[i].queue.items = safe_malloc(sizeof(t_request)
				*workspace->number_of_coders);
		safe_cond_handle(&workspace->dongles[i].cond, INIT);
	}
	coder_init(workspace);
}
// Função de liberação para podermos testar vazamentos no Valgrind

static void	free_dongles(t_workspace *ws)
{
	int	i;

	i = 0;
	while (i < ws->number_of_coders)
	{
		safe_mutex_handle(&ws->dongles[i].dongle, DESTROY);
		safe_cond_handle(&ws->dongles[i].cond, DESTROY);
		free(ws->dongles[i].queue.items);
		i++;
	}
	free(ws->dongles);
}

void	cleanup_data(t_workspace *ws)
{
	int	i;

	if (ws->dongles)
		free_dongles(ws);
	safe_mutex_handle(&ws->log_mutex, DESTROY);
	safe_mutex_handle(&ws->end_mutex, DESTROY);
	if (ws->coders)
	{
		i = 0;
		while (i < ws->number_of_coders)
		{
			safe_mutex_handle(&ws->coders[i].progress_mutex, DESTROY);
			i++;
		}
		free(ws->coders);
	}
}
