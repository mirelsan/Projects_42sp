NAME = libft.a 

SOURCE = ft_*.c

CC = gcc

FLAGS = -Wall -Wextra -Werror

SOURCE := $(addprefix ./src/,$(SOURCE))
OBJECTS = $(SOURCE:./src/%.c=./obj/%.o)

all: $(NAME)

obj/%.o: src/%.c
	$(CC) $(FLAGS) -I ./include -c $< -o $@

clean: 
	rm -f $(OBJECTS)

fclean: clean
	rm -f $(NAME) 

re: fclean all

.PHONY: all clean fclean re