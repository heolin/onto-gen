all:
	./pdf2txt.sh
	./clearTxt.sh
	./lemmatize.sh
	cat lem/* | sort -u | shuf > final/final.txt

clean:
	rm txt/* -rf
	rm cleared/* -rf
	rm lem/* -rf
