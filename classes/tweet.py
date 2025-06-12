from datetime import datetime
from typing import Generator

def gerador_id():
    """
    Gerador infinito de IDs numéricos sequenciais.

    Retorna:
        int: O próximo número da sequência, começando em 1.

    Exemplo de uso:
        gerador = gerador_id()
        print(next(gerador))  # 1
        print(next(gerador))  # 2
    """
    id = 1
    while True:
        yield id
        id += 1

gerador = gerador_id()


class Tweet:
    """
    Classe que representa um tweet no sistema MyTwitter.

    Atributos:
        __id (int): Identificador único do tweet, gerado automaticamente.
        __usuario (str): Nome do usuário que criou o tweet.
        __mensagem (str): Conteúdo do tweet (limite sugerido: 280 caracteres).
        __data_postagem (datetime): Data e hora da criação do tweet.

    Métodos:
        get_id(): Retorna o ID do tweet.
        get_usuario(): Retorna o nome do usuário que criou o tweet.
        get_mensagem(): Retorna o conteúdo do tweet.
        get_data_postagem(): Retorna a data e hora da postagem do tweet.

    Exemplo de uso:
        tweet = Tweet("Clara", "Meu primeiro tweet!")
        print(tweet.get_usuario())  # Clara
        print(tweet.get_mensagem())  # Meu primeiro tweet!
        print(tweet.get_id())  # 1
        print(tweet.get_data_postagem())  # Data e hora da postagem
    """

    def __init__(self, usuario: str, mensagem: str, gerador_id: Generator = gerador):
        """
        Inicializa um tweet com os dados fornecidos.

        Args:
            usuario (str): Nome do usuário que fez a postagem.
            mensagem (str): Texto do tweet.

        Atributos:
            __id (int): ID único gerado automaticamente.
            __usuario (str): Nome do usuário.
            __mensagem (str): Conteúdo da postagem.
            __data_postagem (datetime): Data e hora da criação do tweet.
        """
        self.__id = next(gerador_id)
        self.__usuario = usuario
        self.__mensagem = mensagem
        self.__data_postagem = datetime.today()

    def get_id(self):
        """
        Retorna o ID único do tweet.

        Returns:
            int: O identificador único do tweet.
        """
        return self.__id

    def get_usuario(self):
        """
        Retorna o nome do usuário que postou o tweet.

        Returns:
            str: Nome do usuário.
        """
        return self.__usuario

    def get_mensagem(self):
        """
        Retorna o conteúdo do tweet.

        Returns:
            str: Texto do tweet.
        """
        return self.__mensagem

    def get_data_postagem(self):
        """
        Retorna a data e hora da postagem do tweet.

        Returns:
            datetime: Data e hora da criação do tweet.
        """
        return self.__data_postagem
