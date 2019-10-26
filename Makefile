NAME	=	 pbrain-gomoku-ai

$(NAME):
	ln -s src/gomoku.py $(NAME)

all: $(NAME)

clean:
	rm -rf **/__pycache__

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
