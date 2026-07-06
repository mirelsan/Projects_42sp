# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_count_harvest_iterative.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: codespace <codespace@student.42.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/06 01:09:06 by codespace         #+#    #+#              #
#    Updated: 2026/07/06 01:25:33 by codespace        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_count_harvest_iterative():
    x = int(input("Days until harvest: "))
    i = 1
    while i <= x:
        print("Day", i)
        i += 1
    print("Harvest time!") 