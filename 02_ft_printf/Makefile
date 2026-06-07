NAME = libftprintf.a
CC = cc
FLAGS = -Wall -Wextra -Werror

SOURCE	= ft_printf.c\
ft_print_format.c\
ft_print_hex.c\
ft_print_str.c\
print_char.c\
print_f.c\
print_p.c\
print_u.c

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



