from .mytwitter import MyTwitter
from .perfis import PessoaFisica, PessoaJuridica
    
def usuarios_padrao(twitter: MyTwitter) -> None:
  """
  Cadastra usuários padrão no sistema
  :param twitter: Classe que gerencia o sistema
  """

  twitter.criar_perfil(PessoaFisica('Rodrigo','457.602.897-34'))
  twitter.criar_perfil(PessoaFisica('Clara','684.641.648-73'))
  twitter.criar_perfil(PessoaFisica('Ryan','187.179.932-82'))
  twitter.criar_perfil(PessoaFisica('Arthur','309.855.127-96'))
  twitter.criar_perfil(PessoaFisica('Jolyne','587.157.833-65'))
  twitter.criar_perfil(PessoaFisica('Rakon','486.564.425-41'))
  twitter.criar_perfil(PessoaFisica('Marshal','481.878.918-35'))
  twitter.criar_perfil(PessoaFisica('Francisca','740.515.397-12'))
  twitter.criar_perfil(PessoaFisica('Nana','656.984.171-45'))
  twitter.criar_perfil(PessoaFisica('Jade','710.361.119-58'))

  twitter.criar_perfil(PessoaJuridica('Xuiter_Oficial','123.231.4444.69'))
  twitter.criar_perfil(PessoaJuridica('Tech_Master', '987.654.3210.12'))
  twitter.criar_perfil(PessoaJuridica('Mega_Stores', '456.789.1234.56'))
  twitter.criar_perfil(PessoaJuridica('Fast_Solutions', '321.654.9876.34'))
  twitter.criar_perfil(PessoaJuridica('Alpha_Systems', '159.753.4862.90'))

  
  

