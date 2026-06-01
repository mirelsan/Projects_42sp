NAME = libft.a
CC = cc
FLAGS = -Wall -Wextra -Werror
SOURCE = ft_substr.c\
ft_strmapi.c\
ft_striteri.c\
ft_putnbr_fd.c\
ft_memcpy.c\
ft_lstmap.c\
ft_lstadd_front.c\
ft_isascii.c\
ft_atoi.c\
ft_strtrim.c\
ft_strlen.c\
ft_strdup.c\
ft_putendl_fd.c\
ft_memcmp.c\
ft_lstlast.c\
ft_lstadd_back.c\
ft_isalpha.c\
ft_strrchr.c\
ft_strlcpy.c\
ft_strchr.c\
ft_putchar_fd.c\
ft_memchr.c\
ft_lstiter.c\
ft_itoa.c\
ft_isalnum.c\
ft_toupper.c\
ft_strnstr.c\
ft_strlcat.c\
ft_split.c\
ft_memset.c\
ft_lstsize.c\
ft_lstdelone.c\
ft_isprint.c\
ft_calloc.c\
ft_tolower.c\
ft_strncmp.c\
ft_strjoin.c\
ft_putstr_fd.c\
ft_memmove.c\
ft_lstnew.c\
ft_lstclear.c\
ft_isdigit.c\
ft_bzero.c

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