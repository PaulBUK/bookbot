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
	except Exception as e:
		print(f"Error: an error occurred while opening '{file_path}': {e}")
		return None


import sys

from stats import get_num_words, char_frequencies, sort_char_counts


def main():
	# Expect the book path as the second command-line argument
	if len(sys.argv) != 2:
		print("Usage: python3 main.py <path_to_book>")
		sys.exit(1)

	book_path = sys.argv[1]
	text = get_book_text(book_path)
	if text is None:
		return
	count = get_num_words(text)
	#print(f"Found {count} total words")

	chars = char_frequencies(text)
	sorted_chars = sort_char_counts(chars)

	# Print the formatted report
	print("============ BOOKBOT ============")
	print(f"Analyzing book found at {book_path}...")
	print("----------- Word Count ----------")
	print(f"Found {count} total words")
	print("--------- Character Count -------")
	# sorted_chars is list of dicts {"char": c, "num": n}
	for entry in sorted_chars:
		ch = entry["char"]
		n = entry["num"]
		print(f"{ch}: {n}")
	print("============= END ===============")


# ...count_words moved to stats.py as get_num_words


if __name__ == "__main__":
	main()

