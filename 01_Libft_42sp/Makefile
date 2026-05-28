NAME = libft.a

all: $(NAME)

$(NAME): $(OBJECTS)
		ar rcs $(NAME) $(OBJECTS)

SOURCE = $(wildcard ft_*.c)

CC = gcc

FLAGS = -Wall -Wextra -Werror

OBJECTS = $(SOURCE:.c=.o)

%.o: %.c
	$(CC) $(FLAGS) -c $< -o $@

clean: 
	rm -f $(OBJECTS)

fclean: clean
	rm -f $(NAME) 

re: fclean all

.PHONY: all clean fclean re