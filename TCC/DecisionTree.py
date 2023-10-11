import pyodbc
import configparser
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Concatenate
from sklearn.model_selection import train_test_split

# Função para carregar as credenciais do arquivo .ini
def carregar_credenciais(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    db_config = config['BancoDeDados']
    return db_config['url'], db_config['usuario'], db_config['senha']

if __name__ == "__main__":
    arquivo_ini = r'C:\opt\nutrilife\conf\nutrilife.ini'  # Caminho absoluto correto para o seu arquivo .ini
    url, usuario, senha = carregar_credenciais(arquivo_ini)

    try:
        conn = pyodbc.connect(
            f'DRIVER=SQL Server;SERVER={url};DATABASE=adm;UID={usuario};PWD={senha}'
        )
        cursor = conn.cursor()

        # Consulta para selecionar um usuário específico (por exemplo, ID = 1)
        query_users = "SELECT * FROM Usuario WHERE ID = 1"
        df_users = pd.read_sql(query_users, conn)

        # Consulta para selecionar todas as receitas
        query_recipes = "SELECT * FROM Receita"
        df_recipes = pd.read_sql(query_recipes, conn)

        conn.close()

        # Crie um DataFrame que contenha as interações entre usuários e receitas (se houver)
        interactions_df = pd.merge(df_users, df_recipes, left_on='ID', right_on='ID_usuario')

        # Número de usuários e receitas
        num_users = len(df_users)
        num_recipes = len(df_recipes)

        # Defina o número de dimensões para as incorporações
        embedding_dim = 64

        # Crie um DataFrame com dados de entrada X e destino y para treinamento
        X = interactions_df[['ID_usuario', 'ID_receita']].values
        y = interactions_df['classificacao'].values

        # Divida os dados em conjuntos de treinamento e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Crie as camadas de entrada
        input_user = Input(shape=(1,))
        input_recipe = Input(shape=(1,))

        # Crie camadas de Embedding para representar usuários e receitas
        embedding_user = Embedding(input_dim=num_users, output_dim=embedding_dim)(input_user)
        embedding_recipe = Embedding(input_dim=num_recipes, output_dim=embedding_dim)(input_recipe)

        # Aplique a camada de Flatten para a saída do Embedding
        flatten_user = Flatten()(embedding_user)
        flatten_recipe = Flatten()(embedding_recipe)

        # Concatene as representações de usuário e receita
        concatenated = Concatenate()([flatten_user, flatten_recipe])

        # Camadas densas para a rede neural
        dense1 = Dense(128, activation='relu')(concatenated)
        dense2 = Dense(64, activation='relu')(dense1)
        output = Dense(1)(dense2)

        # Crie o modelo
        model = tf.keras.Model(inputs=[input_user, input_recipe], outputs=output)

        # Compile o modelo com função de perda e otimizador apropriados
        model.compile(loss='mean_squared_error', optimizer='adam')

        # Treine o modelo nos dados de treinamento
        model.fit([X_train[:, 0], X_train[:, 1]], y_train, epochs=10, batch_size=64)

        # Avalie o modelo nos dados de teste
        loss = model.evaluate([X_test[:, 0], X_test[:, 1]], y_test)
        print(f"Loss no conjunto de teste: {loss}")

        # Selecione o usuário com ID = 1
        user_id = 1
        user_tensor = tf.convert_to_tensor([user_id])

        # Crie uma lista de receitas para prever a classificação
        receitas_para_prever = df_recipes['ID'].values

        # Crie um tensor para as receitas
        recipe_tensors = tf.convert_to_tensor(receitas_para_prever)

        # Faça previsões para as receitas recomendadas para o usuário
        predictions = model.predict([user_tensor, recipe_tensors])

        # Combine as IDs das receitas com as previsões
        recomendacoes = list(zip(receitas_para_prever, predictions.flatten()))

        # Ordene as recomendações com base nas previsões
        recomendacoes_ordenadas = sorted(recomendacoes, key=lambda x: x[1], reverse=True)

        # Exiba as 10 principais recomendações
        top_10_recomendacoes = recomendacoes_ordenadas[:10]
        print("Top 10 recomendações:")
        for receita_id, pontuacao in top_10_recomendacoes:
            print(f"Receita ID: {receita_id}, Pontuação: {pontuacao}")

    except pyodbc.Error as ex:
        print(f"Erro na conexão com o banco de dados: {ex}")
