from SetlistModule import *

mylib = load_from_file()

search_result = mylib.search_library("Skunk Funk")
search_result.open_pdf()
