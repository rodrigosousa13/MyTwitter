from typing import List
from .perfis import Perfil
from exceptions import UJCException, UNCException

class RepositorioUsuarios:
  def __init__(self):
    """
    Inicializa o repositório de usuários.
    """
    self.__usuarios = []

  def cadastrar(self, usuario: Perfil) -> None:
    """
    Cadastra um novo usuário no repositório.

    Raise:
        UJCException: Se o usuário já estiver cadastrado.
    """
    if not self.buscar(usuario.get_usuario()):
      self.__usuarios.append(usuario)
    else:
      raise UJCException(usuario)

  def buscar(self, usuario: str) -> Perfil | None:
    """
    Busca um usuário pelo nome de usuário.
    """
    for perfil in self.__usuarios:
      if perfil.get_usuario().lower() == usuario.lower():
        return perfil
    return None

  def atualizar(self, perfil: Perfil) -> None:
    """
    Atualiza as informações de um perfil no repositório.
     
    raise:
        UNCException: Se o usuário não estiver cadastrado.
    """
    usuario = self.buscar(perfil.get_usuario())
    if usuario: # verifica se usuario existe
      self.__usuarios[self.__usuarios.index(usuario)] = perfil
    else:
      raise UNCException(perfil.get_usuario())

  def get_usuarios(self) -> List[Perfil]:
    """
    Retorna a lista de todos os perfis cadastrados.
    """
    return self.__usuarios