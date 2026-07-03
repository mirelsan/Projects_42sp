NAME = push_swap
CHECKER = checker
CC = cc
FLAGS = -Wall -Wextra -Werror
RM = rm -f

SOURCE =	parsing_utils.c \
			validation.c \
			push.c \
			reverse.c \
			rotate.c \
			swap.c \
			sort.c \
			radix.c \
			chunk_utils.c \
			adaptive.c \
			sort_chunk.c \
			options.c \
			disorder.c \
			print_bench.c\
			parsing_utils2.c\
			sort_chunk_utils.c\
			main.c

BONUS_SOURCE = bonus/checker_bonus.c \
			bonus/checker_bonus_main.c \
			bonus/parsing_utils_bonus.c

LIBFT = ./libft/libft.a

OBJ = $(SOURCE:.c=.o)
BONUS_OBJ = $(BONUS_SOURCE:.c=.o)
OBJ_NO_MAIN = $(filter-out main.o, $(OBJ))

all: $(NAME)

libft:
	make -C ./libft

$(NAME): $(OBJ) libft
	$(CC) $(FLAGS) -o $(NAME) $(OBJ) $(LIBFT)

$(CHECKER): $(OBJ_NO_MAIN) $(BONUS_OBJ) libft
	$(CC) $(FLAGS) -o $(CHECKER) $(OBJ_NO_MAIN) $(BONUS_OBJ) $(LIBFT)

bonus: $(CHECKER)

%.o: %.c
	$(CC) $(FLAGS) -c $< -o $@

clean:
	make clean -C ./libft
	$(RM) $(OBJ) $(BONUS_OBJ)

fclean: clean
	make fclean -C ./libft
	$(RM) $(NAME) $(CHECKER)

re: fclean all

test: all
		@if [ -f "tester.sh" ]; then \
				bash tester.sh; \
		else \
				echo "Error: script tester.sh not found in root."; \
		fi

.PHONY: all clean fclean re libft test