NAME = push_swap
CC = cc
FLAGS = -Wall -Wextra -Werror
RM = rm -f

SOURCE = parsing.c \
         validation.c

LIBFT = libft/libft.a

OBJ = $(SOURCE:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(FLAGS) -o $(NAME) $(OBJ) $(LIBFT)

%.o: %.c
	$(CC) $(FLAGS) -c $< -o $@

clean: 
	make clean -C libft
	$(RM) $(OBJ)

fclean: clean
	make fclean -C libft
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re