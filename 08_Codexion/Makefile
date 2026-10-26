NAME = codexion

CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread

RM = rm -f

SRCS = main.c \
		parsing.c \
		utils.c \
		safe_functions.c \
		init.c \
		time.c \
		safe_cond.c \
		dongle.c


OBJS = $(SRCS:.c=.o)

HEADER = coders.h

all: $(NAME)

$(NAME): $(OBJS)
		$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c $(HEADER)
		$(CC) $(CFLAGS) -c $< -o $@

clean:
		$(RM) $(OBJS)

fclean: clean
		$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
