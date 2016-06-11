# -*- coding:utf-8 -*-
import os
import re
import sys
# local
from main_page import main_page
from content_page import content_page

download_queue = list()


def main():
	outer_str = ''
	while(1):
		os.system('clear')
		if outer_str:
			print outer_str
		query_key = raw_input('(C) - Check download queue\n(Q) - Quit and will not download anything\nOr Input Query Key Now : ')
		if query_key == 'Q' or query_key == 'q' or query_key == 'quit' or query_key == 'Quit':
			leave_fun()
		elif query_key == 'C' or query_key == 'c' or query_key == 'Check' or query_key == 'check':
			outer_str = check_download_queue()
			continue

		query_key = delete_mega_from_query(query_key)
		choice = None
		m = main_page(query_key=query_key)
		warning_str = ''

		while True:
			os.system('clear')
			m.show_page_list()
			print "(S) - Select\n(N) - Next page\n(C) - Check download queue\n(D) - Download files in download queue\n(Q) - Quit the query this time\n"

			if warning_str:
				print warning_str
				warning_str = ''
			else:
				pass


			choice = raw_input('Your choice : ')


			# Select
			if choice == 'S' or choice == 's':
				warning_str = select(m)

			# Next page
			elif choice == 'N' or choice == 'n':
				# There is a next page
				if m.next_main_page_link:
					m = main_page(url=m.next_main_page_link)
				# There is not
				else:
					warning_str = ornament("Sorry, this is the last page.")

			# Check download queue
			elif choice == 'C' or choice == 'c':
				check_download_queue()

			# Download files in download queue
			elif choice == 'D' or choice == 'd':
				for page in download_queue:
					directory_name = replace_bad_char(page['title'])+'/'
					info_file_name = 'info.txt'
					passwd = replace_bad_char(page['content_page'].passwd)

					# os.system("mkdir " + directory_name)
					print "mkdir " + directory_name
					# os.system("echo '" + passwd + "' > " + directory_name + info_file_name)
					print '"'+passwd+'"'
					print len(passwd)
					print 'echo ' + passwd + ' >> ' + directory_name + info_file_name
					for link in page['content_page'].links:
						# os.system("megadl " + directory_name + " '" + link + "' > /dev/null &")
						print("megadl --path " + directory_name + " '" + link + "' > /dev/null &")
				empty_download_queue()
				warning_str = ornament("Downloading files now and empty the download queue")

			# Quit the query this time
			elif choice == 'Q' or choice == 'q':
				break

			# Wrong input
			else:
				warning_str = ornament("[ERR] - Wrong Choice !")


def leave_fun():
	print "See you next time."
	sys.exit(1)


def delete_mega_from_query(query_key):
	return re.sub("[Mm][Ee][Gg][Aa]", "", query_key)


def replace_bad_char(bad_str):
	for ch in ['&', '[', ']', '(', ')', '-', '#', '!', '@', '\n', ' ', '/', '`', '~']:
		bad_str = bad_str.replace(ch, '')
	return bad_str


def check_download_queue():
	while True:
		os.system('clear')
		if len(download_queue) == 0:
			return ornament('No record in download queue')
		else:
			print 'No. Title'
			for i in range(len(download_queue)):
				print "%3d %s" % (i+1, download_queue[i]['title'])
			delete_from_queue = raw_input("Which link do you want to delete (ex: 1, All: A/a, Cancel: C/c ) : ")
			try:
				if delete_from_queue == 'C' or delete_from_queue == 'c' or delete_from_queue == 'Cancel' or delete_from_queue == 'cancel':
					break
				elif delete_from_queue == 'A' or delete_from_queue == 'a':
					confirm = raw_input("Are you sure ? (Please type 'Yes' to delete) : ")
					if confirm == 'Yes':
						empty_download_queue()
					else:
						continue
				else:
					delete_from_queue = int(delete_from_queue)-1
					download_queue[delete_from_queue]['inqueue'] = 0
					del(download_queue[delete_from_queue])
			except ValueError:
				print ornament("[ERR] - Wrong input")
			except IndexError:
				print ornament("[ERR] - Out of range")


def select(m_page):
	try:
		page_choice = input("Which number do you want to select (ex: 1) : ")
		page_choice = int(page_choice)
	except ValueError:
		return ornament("[ERR] - You enter WRONG number")
	except NameError:
		return ornament("[ERR] - You enter WRONG number")

	try:
		page = m_page.inner_page[page_choice-1]
		if page:
			page['read'] = 1
			if page['inqueue'] == 1:
				page_choice = raw_input("(S) - Show image\n(D) - Delete from download queue\n(C) - Cancel\nYour choice : ")
			else:
				page_choice = raw_input("(S) - Show image\n(A) - Add to download queue\n(C) - Cancel\nYour choice : ")
			if page_choice == 'S' or page_choice == 's':
				return ornament(page['content_page'].show_image())
			elif page_choice == 'D' or page_choice == 'd':
				page['inqueue'] = 0
				download_queue.remove(page)
				return ornament("Delete success")
			elif page_choice == 'A' or page_choice == 'a':
				if page['content_page'].links:
					page['inqueue'] = 1
					download_queue.append(page)
					return ornament("Add success")
				else:
					return ornament("[ERR] - Add fail, " + str(page_choice) + " has no mega link")
			elif page_choice == 'C' or page_choice == 'c':
				pass
			else:
				return ornament("[ERR] - Wrong choice")
		else:
			return ornament("[ERR] - This page occured some error")
	except IndexError:
		return ornament("[ERR] - #" + str(page_choice) + " Out of range")

def empty_download_queue():
	download_queue = list()


def ornament(input_str):
	if input_str == '':
		return ''
	else:
		rtn_str = ('*'*(len(input_str)+4)) + '\n* ' + input_str + ' *\n' + ('*'*(len(input_str)+4))
		return rtn_str




if __name__ == '__main__':
	main()