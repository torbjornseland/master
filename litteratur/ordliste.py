
import sys
import random as random

f = open("grammer.txt","r+")

engelsk = []
norsk = []

for line in f.readlines():
	words = line.split()
	if(len(words)>=2):
		engelsk.append(words[0])
		norsk.append(words[1:])

valg = 0

while(valg != 4):
	print("---Meny---")
	print("1.Sett inn ord")
	print("2.Ordquiz")
	print("3.Se ordliste")
	print("4.Avslutt")
	valg = int(raw_input("valg: "))
	if (valg == 1):
		eng_word = raw_input("engelsk: ")
		engelsk.append(eng_word)
		nor_word = raw_input("norsk: ")
		norsk.append([nor_word])
		f.write("%s	%s\n" % (eng_word,nor_word)) 
	elif(valg == 2):
		corr = 0
		corr_ans = []
		numb = int(raw_input("De siste nr: "))
		if numb == 0:
			start = 0
			numb = len(engelsk)
		else:
			start = len(engelsk)-1-numb
		quest = int(raw_input("Antall spm: "))
		for i in range(quest):
			true_ans = False
			ok = True
			while ok:
				ra_num = random.randint(start,len(engelsk)-1)
				ok = False
				for k in corr_ans:
					if(ra_num == k):
						ok = True
			print "engelsk: ",engelsk[ra_num]
			nor_ans= raw_input("norsk: ")
			for j in norsk[ra_num]:
				if(j == nor_ans):
					true_ans = True
			if true_ans:
				corr_ans.append(ra_num)
				corr += 1
				print "bra! %i av %i riktige" % (corr,i+1)
			else:
				print "Feil! riktig svar er %s" % norsk[ra_num][0]
			if(len(corr_ans)== numb):
				print "Du har klart alle!"
				break
	elif(valg == 3):
		print "------ Ordliste--------"
		word_dict = {}
		for i in range(len(engelsk)):
			word_dict[engelsk[i]]= norsk[i]
		for j in word_dict:
			print j,word_dict[j]
		for i in range(len(engelsk)):
			#print ("%s %30s" % (engelsk[i],norsk[i][:]))
			if(len(norsk[i])==2):
				print "{0:<20s} {1},{2}".format(engelsk[i],norsk[i][0],norsk[i][1])
			else:
				print "{0:<20s} {1}".format(engelsk[i],norsk[i][0])

f.close()
