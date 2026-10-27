/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:25:04 by mirelsan          #+#    #+#             */
/*   Updated: 2026/10/26 21:25:08 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "coders.h"


int main(int ac, char **av)
{
    t_workspace ws;
    pthread_t monitor;
    int         i;

    if (ac != 9)
    {
        printf("Usage: ./codexion <coders> <burnout> <compile> <debug> "
            "<refactor> <compiles> <cooldown> <fifo|edf>\n");
        return (1);
    }

    // 1. Parsing
    parse_input(&ws, av);
    ws.start_simulation = get_time_ms();

    // 2. Inicialização dos Dados e Mutexes
    data_init(&ws);
    i = 0;
    while (i < ws.number_of_coders)
    {
        safe_thread_handle(&ws.coders[i].thread_id, coder_routine, 
            &ws.coders[i], CREATE);
        i++;
    }
    safe_thread_handle(&monitor, monitor_routine, &ws, CREATE);
    i = 0;
    while (i < ws.number_of_coders)
    {
        safe_thread_handle(&ws.coders[i].thread_id, NULL, NULL, JOIN);
        i++;
    }
    // 3. Destruição e Liberação de Memória
    safe_thread_handle(&monitor, NULL, NULL, JOIN);
    cleanup_data(&ws);
    return (0);
}