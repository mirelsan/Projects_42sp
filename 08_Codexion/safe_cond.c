/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   safe_cond.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/26 21:26:08 by mirelsan          #+#    #+#             */
/*   Updated: 2026/10/26 21:26:09 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "coders.h"

static void handle_cond_error(int status, t_opcode opcode)
{
    if (0 == status)
        return ;
    if (EAGAIN == status && INIT == opcode)
        error_exit("No resources to initialize the condition variable");
    else if (ENOMEM == status && INIT == opcode)
        error_exit("Not enough memory to initialize the condition variable.");
    else if (EBUSY == status && DESTROY == opcode)
        error_exit("Condition variable destroyed while threads wait on it.");
    else if (EINVAL == status)
        error_exit("Invalid condition variable or attribute.");
    else
        error_exit("Unexpected condition variable error.");
}

void  safe_cond_handle(pthread_cond_t *cond, t_opcode opcode)
{
    if (INIT == opcode)
        handle_cond_error(pthread_cond_init(cond, NULL), opcode);
    else if (DESTROY == opcode)
        handle_cond_error(pthread_cond_destroy(cond), opcode);
    else
        error_exit("Wrong opcode for cond handle");
}