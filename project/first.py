from tika import parser
import re
import string
def tika_function(file):
	pdf=parser.from_file(file)["content"]
	#print(pdf)
	"""
	pun=string.punctuation
	pdf=re.sub(r" {2}","",pdf)
	pdf=re.sub(r"\n{2,4}"," ",pdf)
	pdf=re.sub(r"\n","",pdf)
	pdf=re.sub(r"\_{8,100}","",pdf)
	"""
	pdf=re.sub(r" {2}","",pdf)

	pdf=re.sub(r"\n{2}","\n",pdf)
	#print(pdf)
	pdf=re.sub(r"\n"," ",pdf)
	#print(pdf)
	pattern1=r"\d\. .*? [a-z]\) .*? [a-z]\) .*? [a-z]\) .*? [a-z]\) .*? Answer: .*?\s+"
	pattern=r"\d\.( .*)? [a-z]\) (.*)? [a-z]\) (.*)? [a-z]\) (.*)? [a-z]\) (.*)? Answer: (.*)?\s+"
	pdf=re.findall(pattern1,pdf) 
	lis={"questions":[],"answers":[]}
	for qp in pdf:
	        match=re.match(pattern,qp)
	        res=match.groups()
	        lis["questions"].append(res[0])
	        n=len(res)
	        ans=[]
	        for i in range(1,n-1):
	        	ans.append(res[i])
	        answer=res[n-1]
	        answer=answer.split(";")
	        ans1=""
	        for each in answer:
	        	ans1+=each+";"
	        ans.append(ans1)
	        lis["answers"].append(ans)
	return lis

#print(tika_function("os1.pdf"))