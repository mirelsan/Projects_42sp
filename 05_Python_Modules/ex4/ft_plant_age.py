# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_plant_age.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: codespace <codespace@student.42.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/06 00:48:40 by codespace         #+#    #+#              #
#    Updated: 2026/07/06 00:53:32 by codespace        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_plant_age():
    x = int(input("Enter plant age in days: "))
    if x > 60:
        print("Plant is ready to harvest!")
    else:
        print("Plant needs more time to grow")