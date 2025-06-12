from typing import List, Generator
from .perfis import Perfil, PessoaFisica, PessoaJuridica
from .repositorio import RepositorioUsuarios
from .tweet import Tweet
from exceptions import PEException, PDException, PIException, MFPException, SIException, NFPException, PJSException 

class MyTwitter:
    """
    Classe que implementa funcionalidades básicas de uma rede social, incluindo:
    - Criar, cancelar e verificar perfis
    - Criar tweets e consultar timelines
    - Seguir e obter informações sobre seguidores e seguidos
    """

    def __init__(self):
        """
        Inicializa a rede social com um repositório de usuários.
        """
        self.__repositorio = RepositorioUsuarios()

    def existe_usuario(self, usuario: str) -> bool:
        """
        Verifica se um usuário existe e está ativo.

        :param usuario: Nome do usuário a ser verificado.
        :return: True se o usuário existir e estiver ativo, False caso contrário.
        """
        perfil = self.__repositorio.buscar(usuario)
        return perfil is not None and perfil.is_ativo()

    def criar_perfil(self, perfil: Perfil) -> None:
        """
        Cria um novo perfil de usuário.

        :param perfil: Perfil do usuário a ser criado.
        :raises NFPException: Se o nome não estiver entre 1 e 15 caracteres.
        :raises PEException: Se o nome de usuário já existir.
        """
        usuario = perfil.get_usuario().strip()
        perfil.set_usuario(usuario)
        if len(usuario) not in range(1, 16):
            raise NFPException()
      
        if self.__repositorio.buscar(usuario):
            raise PEException(usuario)
        
        self.__repositorio.cadastrar(perfil)

    def cancelar_perfil(self, usuario: str) -> None:
        """
        Desativa um perfil de usuário.

        :param usuario: Nome do usuário a ser desativado.
        :raises PDException: Se o perfil já estiver desativado.
        :raises PIException: Se o perfil não existir.
        """
        perfil = self.__repositorio.buscar(usuario)
        if perfil:
            if perfil.is_ativo():
                perfil.set_inativo()
                self.__repositorio.atualizar(perfil)
            else:
                raise PDException(usuario)
        else:
            raise PIException(usuario)

    def tweetar(self, usuario: str, mensagem: str, gerador_id: Generator) -> None:
        """
        Publica um tweet para um usuário.

        :param usuario: Nome do usuário que está tweetando.
        :param mensagem: Conteúdo do tweet.
        :param gerador_id: Função geradora passada à classe Tweet
        :raises MFPException: Se a mensagem for vazia ou ultrapassar 140 caracteres.
        :raises PIException: Se o perfil do usuário não existir.
        """
        mensagem = mensagem.strip()
        perfil = self.__repositorio.buscar(usuario)
        if perfil:
            if len(mensagem) in range(1, 141):
                tweet = Tweet(usuario, mensagem, gerador_id)
                perfil.add_tweet(tweet)
                self.__repositorio.atualizar(perfil)
            else:
                raise MFPException()
        else:
            raise PIException(usuario)

    def timeline(self, usuario: str) -> List[Tweet]:
        """
        Retorna a timeline de um usuário, contendo tweets próprios e de perfis seguidos.

        :param usuario: Nome do usuário.
        :return: Lista de tweets na timeline.
        :raises PDException: Se o perfil estiver desativado.
        :raises PIException: Se o perfil não existir.
        """
        perfil = self.__repositorio.buscar(usuario)
        if perfil:
            if perfil.is_ativo():
                return perfil.get_timeline()
            else:
                raise PDException(usuario)
        else:
            raise PIException(usuario)

    def tweets(self, usuario: str) -> List[Tweet]:
        """
        Retorna a lista de tweets feitos por um usuário.

        :param usuario: Nome do usuário.
        :return: Lista de tweets publicados pelo usuário.
        :raises PDException: Se o perfil estiver desativado.
        :raises PIException: Se o perfil não existir.
        """
        perfil = self.__repositorio.buscar(usuario)
        if perfil:
            if perfil.is_ativo():
                return perfil.get_tweets()
            else:
                raise PDException(usuario)
        else:
            raise PIException(usuario)

    def seguir(self, seguidor: str, seguido: str) -> None:
        """
        Permite que um usuário siga outro.

        :param seguidor: Nome do usuário que deseja seguir.
        :param seguido: Nome do usuário a ser seguido.
        :raises PIException: Se algum dos perfis não existir.
        :raises PDException: Se algum dos perfis estiver desativado.
        :raises SIException: Se um usuário tentar seguir a si mesmo.
        """
        perfil_seguidor = self.__repositorio.buscar(seguidor)
        if not perfil_seguidor:
            raise PIException(seguidor)
        if not perfil_seguidor.is_ativo():
            raise PDException(seguidor)

        perfil_seguido = self.__repositorio.buscar(seguido)
        if not perfil_seguido:
            raise PIException(seguido)
        if not perfil_seguido.is_ativo():
            raise PDException(seguido)
        if seguidor == seguido:
            raise SIException(seguidor)
        
        lista_seguidores_seguido = self.seguidores(seguido)
        if seguidor in lista_seguidores_seguido:
            raise PJSException()

        perfil_seguidor.add_seguidos(perfil_seguido)
        perfil_seguido.add_seguidor(perfil_seguidor)

    def numero_seguidores(self, usuario: str) -> int:
        """
        Retorna o número de seguidores de um usuário.

        :param usuario: Nome do usuário.
        :return: Número de seguidores ativos.
        :raises PIException: Se o perfil não existir.
        :raises PDException: Se o perfil estiver desativado.
        """
        perfil = self.__repositorio.buscar(usuario)
        if not perfil:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        return perfil.get_numero_seguidores()

    def seguidores(self, usuario: str) -> List[Perfil]:
        """
        Obtém a lista de seguidores ativos de um usuário.

        :param usuario: Nome do usuário cujo seguidores serão retornados.
        :return: Lista de perfis que seguem o usuário e estão ativos.
        :raises PIException: Se o usuário não existir.
        :raises PDException: Se o usuário estiver desativado.
        """
        perfil = self.__repositorio.buscar(usuario)
        if not perfil:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        return [seguidor for seguidor in perfil.get_seguidores() if seguidor.is_ativo()]

    def seguidos(self, usuario: str) -> List[Perfil]:
        """
        Obtém a lista de usuários que um perfil segue e que estão ativos.

        :param usuario: Nome do usuário cujo seguidos serão retornados.
        :return: Lista de perfis seguidos que estão ativos.
        :raises PIException: Se o usuário não existir.
        :raises PDException: Se o usuário estiver desativado.
        """
        perfil = self.__repositorio.buscar(usuario)
        if not perfil:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        return [seguido for seguido in perfil.get_seguidos() if seguido.is_ativo()]

    def usuarios_cadastrados(self) -> List[str]:
        """
        Retorna uma lista de nomes de usuários cadastrados, indicando se estão ativos ou inativos.

        :return: Lista contendo os nomes dos usuários, com um indicador de inatividade quando aplicável.
        """
        lista_perfis = self.__repositorio.get_usuarios()
        return [perfil.get_usuario() if perfil.is_ativo() else f"{perfil.get_usuario()} (inativo)" for perfil in lista_perfis]

    def get_instance_perfil(self, usuario: str) -> str:
        """
        Retorna o tipo de perfil associado a um usuário.

        :param usuario: Nome do usuário a ser verificado.
        :return: Uma string indicando se o perfil é "PessoaFisica", "PessoaJuridica" ou "None" caso não pertença a nenhum desses tipos.
        :raises PIException: Se o usuário não existir.
        """
        perfil = self.__repositorio.buscar(usuario)
        if not perfil:
            raise PIException(usuario)

        if isinstance(perfil, PessoaFisica):
            return 'PessoaFisica'
        elif isinstance(perfil, PessoaJuridica):
            return 'PessoaJuridica'
        else:
            return 'None'