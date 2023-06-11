import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import os

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def texto_negrito(texto):
    return f"\033[1m{texto}\033[0m"


def aplicar_estilo(texto, cor):
    estilo = "1;"
    codigo_cor = {
        'vermelho': '31',
        'verde': '32',
        'amarelo': '33',
        'azul': '34',
        'magenta': '35',
        'ciano': '36',
        'branco': '37'
    }
    if cor in codigo_cor:
        codigo = codigo_cor[cor]
        print(f"\033[{estilo}{codigo}m{texto}\033[0m")
    else:
        print(texto)


def filtrar_string(string):
    # Remove acentuação
    string = re.sub(r'[^\w\s]', '', string, flags=re.UNICODE)

    # Remove pontuação
    string = re.sub(r'[^\w\s]', '', string)

    return string


def preprocess(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)
    # Remove stopwords and punctuation
    words = [word.lower() for word in words if
             word.lower() not in stopwords.words('english') and word not in string.punctuation]
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words


def get_most_relevant_sentence(query):
    query = preprocess(query)

    max_similarity = linha = 0
    most_relevant_sentence = ""

    for li, sentence in enumerate(corpus):
        similarity = len(set(query).intersection(sentence)) / float(len(set(query).union(sentence)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = " ".join(sentence)
            linha = li
    return most_relevant_sentence, linha


def chatbot(question):
    # Find the most relevant sentence
    question = filtrar_string(question)

    most_relevant_sentence, linha = get_most_relevant_sentence(question)
    # Return the answer
    return most_relevant_sentence, linha


def verifica_arquivo(nome_arquivo):
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)

    with open(nome_arquivo, 'w') as f:
        pass


def escrever_valores_arquivo(dicionario, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for chave, valor in dicionario.items():
            arquivo.write(str(valor) + '\n')


def configura_chatbot(arquivo):
    dicionario = {}
    respostas = []
    aplicar_estilo("===== Tela de Configuração =====", 'vermelho')
    i = 0
    while True:
        i+=1
        print('\nPara sair digite sair\n')
        intent = input(texto_negrito(f'-- ({i}) O que você quer que o chat responda: '))

        if intent == 'sair':
            break
        resposta = input(texto_negrito(f'-- ({i}) O que ele deve responder sobre isso: '))

        if resposta == 'sair':
            break

        respostas.append(resposta)

        if resposta[len(resposta)-1] != '.':
            resposta = resposta + '.'

        dicionario[intent] = intent

    escrever_valores_arquivo(dicionario, arquivo)
    return respostas


def main(respostas):
    print('\n')
    print("===== Chatbot =====")
    question = input("Você:")
    response, linha = chatbot(question)

    print('Chat' + ': '+respostas[linha])


if __name__ == "__main__":
    arquivo = 'chat.txt'
    verifica_arquivo(arquivo)
    respostas = configura_chatbot(arquivo)

    with open('chat.txt', 'r', encoding='latin1') as f:
        data = f.read().splitlines()
    sentences = []

    for sentence in data:
        tokenized_sentence = sent_tokenize(sentence)
        sentences.extend(tokenized_sentence)
        corpus = [preprocess(sentence) for sentence in sentences]

    while True:
        main(respostas)
