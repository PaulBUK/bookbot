def get_book_text(file_path):
	"""Read the contents of a file and return as a string.

	On error, print a friendly message and return None.
	"""
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			return f.read()
	except FileNotFoundError:
		print(f"Error: the file '{file_path}' was not found. Check the path and try again.")
		return None
	except PermissionError:
		print(f"Error: permission denied when trying to open '{file_path}'. Check file permissions.")
		return None
	except UnicodeDecodeError:
		print(f"Error: failed to decode '{file_path}' as UTF-8. The file may be binary or use a different encoding.")
		return None
	except IsADirectoryError:
		print(f"Error: '{file_path}' is a directory, not a file. Provide a path to a file to read.")
		return None
	except OSError as e:
		print(f"Error: an OS error occurred while opening '{file_path}': {e}")
		return None


from stats import get_num_words


def main():
	book_path = "books/frankenstein.txt"
	text = get_book_text(book_path)
	if text is None:
		return
	count = get_num_words(text)
	print(f"Found {count} total words")


# ...count_words moved to stats.py as get_num_words


if __name__ == "__main__":
	main()

