NAME = libftprintf.a
CC = cc
FLAGS = -Wall -Wextra -Werror

SOURCE	= ft_printf.c\
ft_printf_char.c\
ft_printf_nbr.c\
ft_printf_str.c\
ft_printf_ptr.c\
ft_printf_hex.cc

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



