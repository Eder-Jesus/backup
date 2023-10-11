import json
import random
import csv

class Receita:
    def __init__(self, nome, ingredientes, preparo, curtidas, kcal):
        self.Nome = nome
        self.Ingredientes = ingredientes
        self.Preparo = preparo
        self.Curtidas = curtidas
        self.Kcal = kcal

def main():
    with open('C:\Users\Edzera\Desktop\TCC\afrodite.json', 'r') as json_file:
        json_content = json_file.read()
        json_data = json.loads(json_content)

    objetosSeparados = []

    for objeto in json_data:
        nomeReceita = ""
        ingredientes = ""
        preparo = ""
        ingredientesBanco = ""
        preparoBanco = ""
        oi = str(objeto)
        ois = oi.split("nome")

        # Para obter o nome
        for chars in ois[1]:
            if chars.isalpha() or (nomeReceita and chars == ' '):
                nomeReceita += chars

        nomeReceita = nomeReceita.replace("secao", "").strip()

        # Para obter os ingredientes
        ingrediente = ois[2].split(":")
        ingredientesBanco = ingrediente[2].replace("\r\n", "").replace("\\\"", "").replace("[", "").replace("]", "").replace("\"", "").replace("},", "").replace("{", "").replace("}", "").strip()
        ingredientes = ingrediente[2].replace("\r\n", "").replace("\\\"", "").replace("[", "").replace("]", "").replace("\"", "").replace("},", "").replace("{", "").replace(",", "").replace("}", "").strip()

        # Para obter o Modo de preparo
        if len(ois) > 3:
            preparoBanco = ois[3].replace("\r\n", "").replace("\": \" Modo de Preparo\",      \"conteudo\": [        ", "").replace("\"", "").replace("},", "").replace("]", "").replace("{", "").replace(",", "\n").replace("}", "").strip()
            preparo = ois[3].replace("\r\n", "").replace("\": \" Modo de Preparo\",      \"conteudo\": [        ", "").replace("\"", "").replace("},", "").replace("]", "").replace("{", "").replace(",", "").replace("}", "").strip()

        if len(objetosSeparados) == 798:
            pass

        caminhoArquivo = "C:\\Users\\DEV_05\\Documents\\teste.csv"

        if preparoBanco and ingredientesBanco:
            if "Modo de Preparo" not in nomeReceita and "Modo de Preparo" not in ingredientes and "Modo de Preparo" not in preparo:
                if "conteudo" not in nomeReceita and "conteudo" not in ingredientes and "conteudo" not in preparo:
                    numeroAleatorio = random.randint(100, 600)

                    receita = Receita(nomeReceita, ingredientesBanco, preparoBanco, 0, numeroAleatorio)
                    objetosSeparados.append(receita)

                    with open(caminhoArquivo, 'a', encoding='utf-8') as csv_file:
                        writer = csv.writer(csv_file)
                        linha = [nomeReceita, ingredientes, numeroAleatorio, preparo, 0]
                        writer.writerow(linha)

    # Resto do seu código...

if __name__ == "__main__":
    main()
