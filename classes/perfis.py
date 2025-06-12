from __future__ import annotations
from typing import List
from .tweet import Tweet

class Perfil:
    def __init__(self, usuario: str) -> None: 
        """
        Inicializa um perfil com o nome de usuário fornecido.

        Args:
            usuario (str): Nome de usuário do perfil.
        """
        self.__usuario = usuario
        self.__seguidos = []
        self.__seguidores = []
        self.__tweets = []
        self.__ativo = True

    def add_tweet(self, tweet: Tweet) -> None:
        """
        Adiciona um tweet ao perfil.

        Args:
            tweet (Tweet): Tweet a ser adicionado.
        """
        self.__tweets.append(tweet)

    def add_seguidos(self, perfil: Perfil) -> None:
        """
        Adiciona um perfil à lista de seguidos.

        Args:
            perfil (Perfil): Perfil a ser seguido.
        """
        if perfil not in self.__seguidos:
            self.__seguidos.append(perfil)

    def add_seguidor(self, perfil: Perfil) -> None:
        """
        Adiciona um perfil à lista de seguidores.
        """
        if perfil not in self.__seguidores:
            self.__seguidores.append(perfil)

    def get_tweet(self, id: int) -> Tweet | None:
        """
        Retorna um tweet pelo seu ID.
        """
        for i in self.__tweets:
            if i.get_id() == id:
                return i
        print('Tweet não encontrado, tente novamente')

    def get_tweets(self) -> List[Tweet]:
        """
        Retorna a lista de tweets ordenados por data de postagem.
        """
        tweets_ordenados = sorted(self.__tweets, key=lambda x: x.get_data_postagem(), reverse=True)
        return tweets_ordenados

    def get_timeline(self) -> List[Tweet]:
        """
        Retorna a timeline do perfil, incluindo tweets dos perfis seguidos.
        """
        timeline = []
        for i in self.__seguidos:
            timeline += i.get_tweets()
        timeline += self.__tweets
        timeline = sorted(timeline, key=lambda x: x.get_data_postagem(), reverse=True)
        return timeline

    def get_usuario(self) -> str:
        """
        Retorna o nome de usuário do perfil.
        """
        return self.__usuario

    def set_usuario(self, usuario) -> None:
        """
        Define um novo nome de usuário para o perfil.

        Args:
            usuario (str): Novo nome de usuário.
        """
        self.__usuario = usuario

    def set_ativo(self) -> None:
        """
        Define o perfil como ativo.
        """
        self.__ativo = True

    def set_inativo(self) -> None:
        """
        Define o perfil como inativo.
        """
        self.__ativo = False

    def is_ativo(self) -> bool:
        """
        Verifica se o perfil está ativo.
        """
        return self.__ativo

    def get_numero_seguidores(self):
        """
        Retorna o número de seguidores do perfil.
        """
        return len(self.__seguidores)

    def get_seguidores(self) -> List[Perfil]:
        """
        Retorna a lista de seguidores do perfil.
        """
        return self.__seguidores

    def get_seguidos(self) -> List[Perfil]:
        """
        Retorna a lista de perfis seguidos.
        """
        return self.__seguidos
    

class PessoaFisica(Perfil):
    """
    Classe que representa um perfil de Pessoa Física no sistema MyTwitter.

    Esta classe herda da classe Perfil e adiciona o atributo cpf.

    Atributos:
        __cpf (str): CPF da pessoa física (Cadastro de Pessoa Física).

    Métodos:
        get_cpf(): Retorna o CPF da pessoa física.

    Exemplo de uso:
        pessoa = PessoaFisica("João", "123.456.789-00")
        print(pessoa.get_usuario())  # João
        print(pessoa.get_cpf())  # 123.456.789-00
    """

    def __init__(self, usuario, cpf):
        """
        Inicializa um perfil de Pessoa Física.

        Args:
            usuario (str): Nome de usuário do perfil.
            cpf (str): CPF do usuário (formato recomendado: 'XXX.XXX.XXX-XX').
        """
        super().__init__(usuario)
        self.__cpf = cpf

    def get_cpf(self):
        """
        Retorna o CPF da pessoa física.
        """
        return self.__cpf


class PessoaJuridica(Perfil):
    """
    Classe que representa um perfil de Pessoa Jurídica no sistema MyTwitter.

    Esta classe herda da classe Perfil e adiciona o atributo cnpj.

    Atributos:
        __cnpj (str): CNPJ da empresa (Cadastro Nacional da Pessoa Jurídica).

    Métodos:
        get_cnpj(): Retorna o CNPJ da empresa.

    Exemplo de uso:
        empresa = PessoaJuridica("Deepseek", "12.345.678/0001-99")
        print(empresa.get_usuario())  # Deepseek
        print(empresa.get_cnpj())  # 12.345.678/0001-99
    """

    def __init__(self, usuario, cnpj):
        """
        Inicializa um perfil de Pessoa Jurídica.

        Args:
            usuario (str): Nome de usuário da empresa.
            cnpj (str): CNPJ da empresa (formato recomendado: 'XX.XXX.XXX/0001-XX').
        """
        super().__init__(usuario)
        self.__cnpj = cnpj

    def get_cnpj(self):
        """
        Retorna o CNPJ da empresa.
        """
        return self.__cnpj