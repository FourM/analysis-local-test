# Doc2Vec

## Create model
* Prepare the characters and sentences to be searched in a text file or csv file.
```text
file name is "original-data.txt" or "original-data.csv"
```

---
* In the case of csv, the text you want to extract is output to a txt file once.
```shell
pipenv run python3 doc2vec/csv_split_word.py (folder_name) (csv_column_name)
```
---

* Execute the following command to divide it.

-b (input buffer size) is set large value.
```shell
mecab -b 131072 -Owakati (folder_name)/original-data.txt -o (folder_name)/split-word.txt
nkf -w --overwrite split-word.txt
```

* Create a learning model.
```shell
pipenv run python3 doc2vec/create_model.py (folder_name)
```

At this point, you can search and calculate.

* Search for synonyms from the learning model.
```shell
pipenv run python3 doc2vec/use_model.py (folder_name) (search_word)
ex) pipenv run python3 doc2vec/use_model.py App_Annie "日本" 
```

* Operate words from the learning model.
```shell
pipenv run python3 doc2vec/use_model.py (folder_name) (word_calc)
ex) pipenv run python3 doc2vec/use_model.py App_Annie "イチロー-野球+サッカー"
```

* Output the plot to a file.
```shell
pipenv run python3 doc2vec/output_plot.py (folder_name) (word)
ex) pipenv run python3 doc2vec/output_plot.py App_Annie "アップデート"
```
