from BeautifulSoup import BeautifulSoup
import urllib
import re
from collections import defaultdict
import numpy as np


def fav_dict(html):
	soup = BeautifulSoup(html)
	
	table = soup.findAll('table')
	table.pop()# get rid of junk at the end
	results = table[9:]
	
	favs = {}
	for item in results:
		l = [re.sub(r"<[^>]*>", "", x.renderContents()) for x in item.findAll('b')]
		favs[l[0]] = l[1:]
		
	return favs 

def matching_lists(A, B):
	s = 0
	for i in A:
		if i in B:
			s += 1
	return s

def taste_matrix(movie_dict):
	authors = movie_dict.keys()
	m = np.zeros((len(authors),len(authors)))
	for i,a in enumerate(authors):
		for j, b in enumerate(authors):
			if a == b:
				m[i,j] = 1
			else:
				m[i,j] = matching_lists(movie_dict[a], movie_dict[b])
	return m

def movie_ranks(movie_list):
	fav = defaultdict(int)

	for sub_list in movie_list:
		for m in sub_list:
			fav[m] +=1

	return fav


if __name__ == "__main__":
	f = urllib.urlopen("http://www.combustiblecelluloid.com/faves.shtml")
	html = f.read()
	results = fav_dict(html)
	#favourite
	print "Top 5 movies (number of times mentioned)"
	for m in sorted(movie_ranks(results.values()).items(), key=lambda x: x[1], reverse=True)[:6]:
		print m[0], m[1]

	print
	print "People with most similar taste (number of matching selections)"
	mm = taste_matrix(results)
	#most alike
	x,y = np.where(mm == mm.max())
	for j in zip(x,y):
		if j[0] < j[1]:
			print "%s // %s %d" %(results.keys()[j[0]], results.keys()[j[1]], mm[j])

	print
	x,y = np.where(mm == mm.max()-1)
	for j in zip(x,y):
		if j[0] < j[1]:
			print "%s // %s %d" %(results.keys()[j[0]], results.keys()[j[1]], mm[j])

	print
	print "People with most normal taste (scored high matching values with most people)"
	#most normal, most eclectic
	s = mm.sum(axis=1)
	for n in np.where(s == s.max())[0]:
		print "most normal %s %d" % (results.keys()[n], s[n])
	print
	print "People with least normal taste (scored low matching values with most people)"
	for e in np.where(s == s.min())[0]:
		print "most different %s %d" % (results.keys()[e], s[e])
