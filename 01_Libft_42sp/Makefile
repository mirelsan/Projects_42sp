NAME = libft.a
CC = gcc
FLAGS = -Wall -Wextra -Werror
SOURCE = $(filter-out %_bonus.c, $(wildcard ft_*.c))
OBJECTS = $(SOURCE:.c=.o)

BONUS_SOURCE = $(wildcard *_bonus.c)
BONUS_OBJECTS = $(BONUS_SOURCE:.c=.o)

all: $(NAME)

$(NAME): $(OBJECTS)
	ar rcs $(NAME) $(OBJECTS)

bonus: $(NAME) $(BONUS_OBJECTS)
	ar rcs $(NAME) $(BONUS_OBJECTS)

%.o: %.c
	$(CC) $(FLAGS) -c $< -o $@

clean: 
	rm -f $(OBJECTS) $(BONUS_OBJECTS)

fclean: clean
	rm -f $(NAME) 

re: fclean all

.PHONY: all clean fclean re bonus