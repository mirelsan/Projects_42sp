# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_count_harvest_recursive.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: codespace <codespace@student.42.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/06 01:09:12 by codespace         #+#    #+#              #
#    Updated: 2026/07/06 01:27:39 by codespace        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_count_harvest_recursive():
    x = int(input("Days until harvest: "))
    helper(1, x)

def helper(i, x):    
    if i > x:
        print("Harvest time!")
        return
    print("Day", i)
    helper(i + 1, x)