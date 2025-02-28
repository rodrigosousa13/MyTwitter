class PEException(Exception):
  """
  Exceção para perfil já existente (Case Insensitive).
  """
  def __init__(self, usuario):
    super().__init__(f"Perfil '{usuario}' já existente (Case Insensitive)")

class PDException(Exception):
  """
  Exceção para perfil desativado.
  """
  def __init__(self, usuario):
    super().__init__(f"Perfil '{usuario}' desativado")

class PIException(Exception):
  """
  Exceção para perfil inexistente.
  """
  def __init__(self, usuario):
    super().__init__(f"Perfil '{usuario}' inexistente")

class MFPException(Exception):
  """
  Exceção para mensagem fora do padrão (1 - 140 caracteres não vazios).
  """
  def __init__(self):
    super().__init__("Mensagem fora do padrão (1 - 140 caracteres não vazios)")

class NFPException(Exception):
  """
  Exceção para nome de usuário fora do padrão (1 - 15 caracteres não vazios).
  """
  def __init__(self):
    super().__init__("Nome de usuário fora do padrão (1 - 15 caracteres não vazios)")

class SIException(Exception):
  """
  Exceção para quando um usuário tenta seguir a si mesmo.
  """
  def __init__(self, usuario):
    super().__init__(f"Usuário {usuario} não pode seguir a si mesmo")

class UJCException(Exception):
  """
  Exceção para perfil já cadastrado.
  """
  def __init__(self, usuario):
    super().__init__(f"Perfil '{usuario}' já cadastrado")

class UNCException(Exception):
  """
  Exceção para usuário não cadastrado.
  """
  def __init__(self, usuario):
    super().__init__(f"Usuário {usuario} não cadastrado")

class PJSException(Exception):
  """
  Exceção para usuário já seguido.
  """
  def __init__(self):
    super().__init__(f"Usuário já seguido.")