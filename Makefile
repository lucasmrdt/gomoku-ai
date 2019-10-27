NAME	=	 pbrain-gomoku-ai

$(NAME):
	ln -s src/gomoku.py $(NAME)

all: $(NAME)

build:	$(NAME)
	pyinstaller.exe $(NAME) --onefile --name $(NAME).exe

clean:
	rm -rf **/__pycache__
	find . -name "*.pyc" -delete
	rm -rf build
	rm -rf dist

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
