# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_water_reminder.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: codespace <codespace@student.42.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/06 01:05:01 by codespace         #+#    #+#              #
#    Updated: 2026/07/06 01:07:59 by codespace        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_water_reminder():
    x = int(input("Days since last watering: "))
    if x > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")