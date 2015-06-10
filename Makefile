index:
	./search/search_manager.py -i index_legislacja/ -c scheme.tsv 

index_documents:
	./search/search_manager.py -i index_legislacja/ -af ./input_corpus/input_corpus.txt -q

index_clear:
	rm -rf index_legislacja/
