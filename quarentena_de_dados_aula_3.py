# -*- coding: utf-8 -*-
"""Quarentena de Dados - Aula 3

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PDdEGVN11XCZktm_B_EirRpldDSFJqBe

#Aula 1

Formulando hipóteses e respondendo a essas perguntas.
"""

#Importando a base
import pandas as pd
base_imdb = pd.read_csv("https://raw.githubusercontent.com/llucaslleall/quarentena-dados/master/Bases/movie_metadata.csv")

#Verificando os valores distintos da coluna color
base_imdb["color"].unique()

#% em cada um dos valores acima (não considera o nan)
base_imdb["color"].value_counts(normalize=True)

#Contando o número de vezes que cada diretor aparece
base_imdb["director_name"].value_counts()

#Descrevendo a coluna num_critic_for_reviews
base_imdb["num_critic_for_reviews"].describe()

criticas = base_imdb["num_critic_for_reviews"]

#Plotando a informação de críticas
criticas.plot(kind="hist")

#Usando o gráfico do seaborn
import seaborn as sns
sns.distplot(criticas)

#Pegando os 5 primeiros com maior bilheteria
base_imdb.sort_values("gross",ascending=False).head()

#Pegando valores aleatórios
base_imdb.sample(5)



"""#Analisando a cor do filme"""

#Tirando nulos (aqui vamos filtrar pelos valores não nulos)
color_or_bw = base_imdb.query("color in ['Color', ' Black and White']")
#Obs: tem um espaço antes do " Black"

#Criando a nova coluna com 0 ou 1
color_or_bw["color_0_ou_1"] = (color_or_bw["color"] == "Color")*1

color_or_bw["color_0_ou_1"].value_counts()

color_or_bw.groupby("color_0_ou_1").mean()["imdb_score"]

"""#Analisando a relação entre budget e faturamento"""

#Retirando os valores vazios
b_g = base_imdb[["director_name", "title_year", "country","budget","gross","imdb_score"]].dropna()

#Buscando apenas os registros americanos por causa do problema de conversão de moeda
imdb_usa = b_g.query("country == 'USA'")

imdb_usa["lucro"] = imdb_usa["gross"] - imdb_usa["budget"]

import seaborn as sns
sns.scatterplot(x="budget",y="lucro",data=imdb_usa)

imdb_usa.query("budget > 2.5*10**8 & lucro < -1.5*10**8")

base_imdb.query("budget == 263700000.0 & gross == 73058679.0")

"""#Verificando mais algumas relações"""

#Fazendo a contagem de filmes por diretor
filmes_diretor = imdb_usa["director_name"].value_counts()
filmes_diretor.head()

#Fazendo o join das duas tabelas
gross_director = imdb_usa[["director_name","gross"]].set_index("director_name").join(filmes_diretor, on="director_name")

#Renomeando as colunas e retirando o index
gross_director.columns = ['arrecadacao', 'filmes_mesmo_diretor']
gross_director = gross_director.reset_index()
gross_director.head()

#Traçando o gráfico desses 2 valores
import seaborn as sns
sns.scatterplot(x="filmes_mesmo_diretor",y="arrecadacao",data=gross_director)

#Agora fazendo o gráfico da base considerando os dados 2 a 2
sns.pairplot(data=imdb_usa[["gross","budget","lucro","title_year"]])

imdb_usa[["gross","budget","lucro","title_year"]].corr()

"""#Desafio

## 1. Considerar a nota na correlação
"""

sns.pairplot(data=imdb_usa[["gross","budget","lucro","title_year","imdb_score"]])

imdb_usa[["gross","budget","lucro","title_year", "imdb_score"]].corr()

"""## Somente os filmes após 2000"""

#Filtrando só os filmes após 2000
imdb_usa = imdb_usa.query("title_year >= 2000")

sns.pairplot(data=imdb_usa[["gross","budget","lucro","title_year","imdb_score"]])

imdb_usa[["gross","budget","lucro","title_year", "imdb_score"]].corr()

