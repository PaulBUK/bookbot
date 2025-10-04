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
import os

from stats import get_num_words, char_frequencies, sort_char_counts


def main():
	# If a path is provided on the command line, use it. Otherwise launch
	# a simple interactive menu to pick a book from the `books/` folder.
	if len(sys.argv) == 2:
		book_path = sys.argv[1]
		run_report(book_path)
		return

	# No argument — interactive menu
	while True:
		sel, used_curses = select_book_menu('books')
		if sel is None:
			# user chose to exit
			print("Exiting.")
			return
		if used_curses:
			run_report_curses(sel)
		else:
			run_report(sel)
			try:
				input("\nPress Enter to return to the menu (or Ctrl-C to quit)...")
			except KeyboardInterrupt:
				print()
				return


def run_report(book_path):
	text = get_book_text(book_path)
	if text is None:
		return
	count = get_num_words(text)
	chars = char_frequencies(text)
	sorted_chars = sort_char_counts(chars)

	# Print the formatted report
	print("============ BOOKBOT ============")
	print(f"Analyzing book found at {book_path}...")
	print("----------- Word Count ----------")
	print(f"Found {count} total words")
	print("--------- Character Count -------")

	# Format into rows of 4 with aligned columns
	char_lines = format_char_rows(sorted_chars, per_row=4)
	for line in char_lines:
		print(line)

	print("============= END ===============")


def select_book_menu(book_dir='books'):
	"""Show an interactive menu of files under `book_dir` and return the
	selected path, or None if the user cancels/exits.
	"""
	try:
		entries = [f for f in os.listdir(book_dir) if os.path.isfile(os.path.join(book_dir, f))]
	except FileNotFoundError:
		print(f"No '{book_dir}' directory found.")
		return None

	entries.sort()
	if not entries:
		print(f"No book files found in '{book_dir}'.")
		return None

	options = entries + ['Exit']

	try:
		import curses

		def _menu(stdscr):
			curses.curs_set(0)
			selected = 0
			while True:
				stdscr.clear()
				h, w = stdscr.getmaxyx()
				stdscr.addstr(0, 0, "Select a book (Use arrows or j/k, Enter to select, Esc to exit):")
				for idx, opt in enumerate(options):
					y = idx + 2
					if y >= h - 1:
						break
					if idx == selected:
						stdscr.attron(curses.A_REVERSE)
						stdscr.addstr(y, 2, opt)
						stdscr.attroff(curses.A_REVERSE)
					else:
						stdscr.addstr(y, 2, opt)
				key = stdscr.getch()
				if key in (curses.KEY_UP, ord('k')):
					selected = (selected - 1) % len(options)
				elif key in (curses.KEY_DOWN, ord('j')):
					selected = (selected + 1) % len(options)
				elif key in (10, 13):  # Enter
					return selected
				elif key == 27:  # ESC
					return -1

		idx = curses.wrapper(_menu)
		used_curses = True
	except Exception:
		# If curses isn't available or fails, fallback to a simple numbered menu
		print("Interactive menu not available, falling back to numbered menu.")
		for i, name in enumerate(options, 1):
			print(f"{i}. {name}")
		try:
			choice = input("Enter number (or press Enter to cancel): ")
		except KeyboardInterrupt:
			return None
		if not choice.strip():
			return (None, False)
		try:
			idx = int(choice) - 1
		except ValueError:
			return (None, False)
	if idx == -1 or options[idx] == 'Exit':
		return (None, used_curses if 'used_curses' in locals() else False)
	return (os.path.join(book_dir, options[idx]), used_curses if 'used_curses' in locals() else False)


def run_report_curses(book_path):
	text = get_book_text(book_path)
	if text is None:
		return
	count = get_num_words(text)
	chars = char_frequencies(text)
	sorted_chars = sort_char_counts(chars)

	lines = []
	lines.append("============ BOOKBOT ============")
	lines.append(f"Analyzing book found at {book_path}...")
	lines.append("----------- Word Count ----------")
	lines.append(f"Found {count} total words")
	lines.append("--------- Character Count -------")

	# add formatted character rows
	lines.extend(format_char_rows(sorted_chars, per_row=4))
	lines.append("============= END ===============")

	try:
		import curses

		def _display(stdscr):
			curses.curs_set(0)
			h, w = stdscr.getmaxyx()
			start = 0
			while True:
				stdscr.clear()
				for i in range(h - 1):
					if start + i >= len(lines):
						break
					stdscr.addnstr(i, 0, lines[start + i], w - 1)
				stdscr.addnstr(h - 1, 0, "Up/Down/PageUp/PageDown to scroll, q or Esc to return", w - 1)
				key = stdscr.getch()
				if key in (ord('q'), 27):
					break
				elif key in (curses.KEY_UP, ord('k')):
					start = max(0, start - 1)
				elif key in (curses.KEY_DOWN, ord('j')):
					if start + (h - 1) < len(lines):
						start = start + 1
				elif key == curses.KEY_NPAGE:  # Page Down
					start = min(len(lines) - (h - 1), start + (h - 1))
				elif key == curses.KEY_PPAGE:  # Page Up
					start = max(0, start - (h - 1))

		curses.wrapper(_display)
	except Exception:
		# Fallback if curses fails — just print normally
		for line in lines:
			print(line)


def format_char_rows(sorted_chars, per_row=4, col_width=20):
	"""Return a list of formatted strings, each containing up to per_row
	character/count pairs aligned in columns of width col_width.
	sorted_chars is a list of dicts {"char": c, "num": n} sorted by num.
	"""
	pairs = [f"{entry['char']}: {entry['num']}" for entry in sorted_chars]
	lines = []
	for i in range(0, len(pairs), per_row):
		row = pairs[i:i+per_row]
		# pad each column to col_width and rstrip at the end
		padded = [s.ljust(col_width) for s in row]
		lines.append(''.join(padded).rstrip())
	return lines


# ...count_words moved to stats.py as get_num_words


if __name__ == "__main__":
	main()

