# hackathon XP Open Finance B2B

![logo_projeto](Logo_hack.jpg)

<img src="Logo_hack.jpg" alt="logo_projeto" width="200"/>

## Repositório Grupo 11 - XP Insights

Este repositório compreende os códigos desenvolvidos pelo Grupo 11 durante o período de 18/02/2022 à 20/02/2022. Os arquivos criam a aplicação do XP Insights, plataforma pensada pela equipe com o objetivo de auxiliar assessores XP e autônomos no relacionamento com seus clientes. 

A aplicação foi desenvolvida majoritariamente utilizando a biblioteca ```streamlit```. Os dados utilizados na exemplificação são oriundos de APIs fornecidas pela própria XP, disponíveis [aqui](https://developer.xpinc.com/). 

## Instalação de programas e Execução

Para execurtar o programa, o primeiro passo seria instalar as bibliotecas requeridas, presentes no arquivo ´´´requirements.txt´´´, para realizar isso em uma linha em qualquer terminal (tendo o pacote ```pip``` já instalado), basta executar o comando abaixo. 

```pip install -r requirements.txt```

Por fim, após as instalações, para rodar a aplicação, basta executar o seguinte comando e acessar o link gerado no terminal

```streamlit run start_assessor.py``` 

E também 

```streamlit run start_person.py```

OBS: Para que seja possível acessar os dados da API, é necessário, inserir suas chaves de acesso. Basta criar uma pasta (diretório) chamado ```streamlit``` e um arquivo ```streamlit/secrets.toml``` Nele, basta preencher o valor das chaves com os seus valores de login na plataforma XP

Arquivo ```streamlit/secrets.toml```
``` 
HACK_XP_CLIENT_ID = "CHAVE_CLIENT_ID"
HACK_XP_CLIENT_SECRET = "CHAVE_CLIENT_SECRET"
```
