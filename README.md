# About

## Setup
```shell
cp .env.example .env
sudo apt install -y python3.9 python3-pip python3.9-dev mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 libc6-dev build-essential nkf tk fonts-migmix libboost-dev cmake
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
bash mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -a -y
```

Default Python3.9
```shell
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
sudo update-alternatives --config python
```


```shell
python -m pip install pipenv
pipenv install --dev
```

* Place the API key for the GCP service CloudNaturalLanguage in .env 
  GOOGLE_NLP_API_KEY, the App Annie API key in APP_ANNIE_API_KEY, and the GCP service account json PATH in GOOGLE_APPLICATION_CREDENTIALS.
  
local
```shell
pipenv run python ./src/app.py
```
You can connect with `localhost:5000`.

If you want to search Doc2Vec, 
you need to create a Model in advance, 
so create a Model according to the procedure of `src/README.md`.
