/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/15 02:10:09 by codespace         #+#    #+#             */
/*   Updated: 2026/06/15 02:45:45 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

#include <unistd.h>
#include <stdlib.h>

typedef struct t_node {
    int data;
    int index;
    struct t_node *next;
} t_node;

typedef struct t_stack {
    t_node *head;
    t_node *tail;
    int size;
} t_stack;

#endif