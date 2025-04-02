# Backend 
python version greater than 3.13
## 1. install dependencies

```shell
pip install -r requirements.txt
```
## 2. set openai api key and trivia api key
set the following environment variables:
```shell
export OPENAI_API_KEY=your_openai_api_key
export TAVILY_API_KEY=your_trivia_api_key
```
or create an **.env** file in the backend root directory and add the following line:

```shell
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_trivia_api_key
```
## 3. start server

```shell
python run.py
```

# Frontend

## 1. install dependencies

```shell
npm install
```

## 2. start server

```shell
npm run dev
```