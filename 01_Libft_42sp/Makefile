NAME = libft.a
CC = gcc
FLAGS = -Wall -Wextra -Werror
SOURCE = $(wildcard ft_*.c)
OBJECTS = $(SOURCE:.c=.o)

all: $(NAME)

$(NAME): $(OBJECTS)
	ar rcs $(NAME) $(OBJECTS)

%.o: %.c
	$(CC) $(FLAGS) -c $< -o $@

clean: 
	rm -f $(OBJECTS)

fclean: clean
	rm -f $(NAME) 

re: fclean all

.PHONY: all clean fclean re