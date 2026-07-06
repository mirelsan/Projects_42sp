# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_harvest_total.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: codespace <codespace@student.42.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/06 00:42:11 by codespace         #+#    #+#              #
#    Updated: 2026/07/06 00:47:17 by codespace        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_harvest_total():
    one = int(input("Day 1 harvest: "))
    two = int(input("Day 2 harvest: "))
    three =int(input("Day 3 harvest: "))
    result = one + two + three
    print("Total harvest: ", result)