import unittest
from datetime import datetime, timedelta
from classes.perfis import Perfil, PessoaFisica, PessoaJuridica
from classes.repositorio import RepositorioUsuarios
from classes.mytwitter import MyTwitter
from classes.tweet import Tweet, gerador_id
from exceptions import PEException, PDException, PIException, MFPException, SIException, UJCException, UNCException, NFPException

class TestTweet(unittest.TestCase):
  """Testes para a classe Tweet"""

  def setUp(self):
    """Configuração antes de cada teste: reinicia o gerador de IDs manualmente."""
    self.gerador_id = gerador_id()
    self.tweets = []

  def criar_tweet(self, usuario, mensagem):
    """Cria um tweet."""
    return Tweet(usuario, mensagem, self.gerador_id)

  def test_criacao_tweet(self):
    """Testa se um tweet é criado corretamente com os atributos esperados."""
    tweet = self.criar_tweet(usuario='Lincoln',
                             mensagem='eu na antena parabolica')

    self.assertEqual(tweet.get_usuario(), 'Lincoln')
    self.assertEqual(tweet.get_mensagem(), 'eu na antena parabolica')
    self.assertEqual(tweet.get_id(), 1)

    now = datetime.now()
    self.assertTrue(
        now - timedelta(seconds=2) <= tweet.get_data_postagem() <= now)

  def test_geracao_ids_and_diferentes_users(self):
    """Testa se os IDs dos tweets são gerados corretamente e são diferentes entre usuários."""
    tweet1 = self.criar_tweet(usuario='Lincoln',
                              mensagem='eu na antena parabolica')
    tweet2 = self.criar_tweet(
        usuario='Petkovich',
        mensagem='animo galera tudo vai melhorar depois da copa de 2014')
    tweet3 = self.criar_tweet(
        usuario='Rodrigo',
        mensagem=
        'ridiculo homem que trabalha em necroterio e toca berimbau no horario de almoco'
    )
    tweet4 = self.criar_tweet(
        usuario='Neymar', mensagem='To chegando com os refrii rapaziada !!')

    self.assertEqual(tweet1.get_id(), 1)
    self.assertEqual(tweet1.get_usuario(), 'Lincoln')
    self.assertEqual(tweet2.get_id(), 2)
    self.assertEqual(tweet2.get_usuario(), 'Petkovich')
    self.assertEqual(tweet3.get_id(), 3)
    self.assertEqual(tweet3.get_usuario(), 'Rodrigo')
    self.assertEqual(tweet4.get_id(), 4)
    self.assertEqual(tweet4.get_usuario(), 'Neymar')

  def test_data_postagem(self):
    """Testa se a data de postagem do tweet é atualizada corretamente."""
    antes = datetime.now() - timedelta(seconds=1)
    tweet = self.criar_tweet(usuario='TestUser',
                             mensagem='verificando data de postagem')
    depois = datetime.now() + timedelta(seconds=1)

    self.assertTrue(antes <= tweet.get_data_postagem() <= depois)


class TestMyTwitter(unittest.TestCase):

  def setUp(self):
    """Executado antes de cada teste."""
    self.twitter = MyTwitter()
    self.perfil1 = PessoaFisica("usuario1", "123")
    self.perfil2 = PessoaJuridica("empresa1", "456")
    self.twitter.criar_perfil(self.perfil1)
    self.twitter.criar_perfil(self.perfil2)
    self.gerador_id = gerador_id()

  def test_existe_usuario(self):
    self.assertTrue(self.twitter.existe_usuario("usuario1"))
    self.assertFalse(self.twitter.existe_usuario("inexistente"))

  def test_criar_perfil(self):
    with self.assertRaises(PEException):
        self.twitter.criar_perfil(PessoaFisica("usuario1", "123"))  # Já existe
    with self.assertRaises(NFPException):
        self.twitter.criar_perfil(PessoaFisica("", "123"))  # Nome inválido
        self.twitter.criar_perfil(PessoaFisica("a"*16, "123"))
      
  def test_cancelar_perfil(self):
    self.twitter.cancelar_perfil("usuario1")
    self.assertFalse(self.twitter.existe_usuario("usuario1"))
    with self.assertRaises(PDException):
        self.twitter.cancelar_perfil("usuario1")  # Já cancelado
    with self.assertRaises(PIException):
        self.twitter.cancelar_perfil("inexistente")

  def test_tweetar(self):
    self.twitter.tweetar("usuario1", "Primeiro tweet!", self.gerador_id)
    self.assertEqual(len(self.twitter.tweets("usuario1")), 1)
    with self.assertRaises(MFPException, ):
        self.twitter.tweetar("usuario1", "", self.gerador_id)  # Mensagem vazia
        self.twitter.tweetar("usuario1", "     ", self.gerador_id)
        self.twitter.tweetar("usuario1", "a"*141, self.gerador_id)
    with self.assertRaises(PIException):
        self.twitter.tweetar("inexistente", "Mensagem", self.gerador_id)

  def test_timeline(self):
    self.twitter.tweetar("usuario1", "Tweet na timeline", self.gerador_id)
    self.assertEqual(len(self.twitter.timeline("usuario1")), 1)
    with self.assertRaises(PIException):
        self.twitter.timeline("inexistente")

  def test_seguir(self):
    self.twitter.seguir("usuario1", "empresa1")
    self.assertIn(self.perfil1, self.twitter.seguidores("empresa1"))
    self.assertIn(self.perfil2, self.twitter.seguidos("usuario1"))
    with self.assertRaises(SIException):
        self.twitter.seguir("usuario1", "usuario1")  # Seguir a si mesmo
    with self.assertRaises(PIException):
        self.twitter.seguir("usuario1", "inexistente")

  def test_numero_seguidores(self):
    self.twitter.seguir("usuario1", "empresa1")
    self.assertEqual(self.twitter.numero_seguidores("empresa1"), 1)

  def test_usuarios_cadastrados(self):
    usuarios = self.twitter.usuarios_cadastrados()
    self.assertIn("usuario1", usuarios)
    self.assertIn("empresa1", usuarios)

  def test_get_instance_perfil(self):
    self.assertEqual(self.twitter.get_instance_perfil("usuario1"), "PessoaFisica")
    self.assertEqual(self.twitter.get_instance_perfil("empresa1"), "PessoaJuridica")
    with self.assertRaises(PIException):
        self.twitter.get_instance_perfil("inexistente")


class TestRepositorioUsuarios(unittest.TestCase):
  """Testes para a classe RepositorioUsuarios"""

  def test_cadastrar(self):
    """Testa a função de cadastro de usuário"""
    repositorio = RepositorioUsuarios()
    jolyne = Perfil('Jolyne')
    repositorio.cadastrar(jolyne)
    usuario_encontrado = repositorio.buscar('Jolyne')
    self.assertEqual(usuario_encontrado, jolyne)

  def test_buscar(self):
    """Testa a função de busca de usuário"""
    repositorio = RepositorioUsuarios()
    jolyne = Perfil('Jolyne')
    repositorio.cadastrar(jolyne)
    usuario_encontrado = repositorio.buscar('Jolyne')
    self.assertEqual(usuario_encontrado, jolyne)

  def test_atualizar(self):
    """Testa a função de atualização de usuário"""
    repositorio = RepositorioUsuarios()
    jolyne = Perfil('Jolyne')
    repositorio.cadastrar(jolyne)
    jolyne.set_usuario('Jolyne Kujo')
    repositorio.atualizar(jolyne)

    perfil_atualizado = repositorio.buscar('Jolyne Kujo')
    self.assertIs(perfil_atualizado, jolyne)  
    self.assertEqual(perfil_atualizado.get_usuario(), 'Jolyne Kujo')

  def test_buscar_usuario_nao_existe(self):
    """Testa a busca de um usuário que não foi cadastrado"""
    repositorio = RepositorioUsuarios()
    usuario_nao_existe = repositorio.buscar('Usuario Inexistente')
    self.assertIsNone(usuario_nao_existe)

  def test_cadastrar_usuario_já_existente(self):
    """Testa o cadastro de um usuário já existente"""
    repositorio = RepositorioUsuarios()
    jolyne = Perfil('Jolyne')
    repositorio.cadastrar(jolyne)
    try:
      repositorio.cadastrar(jolyne)
      self.fail("Deve lançar uma exceção de UJCException")
    except UJCException :
      pass
  
  def test_atualizar_usuario_nao_existente(self): 
    """Testa a atualização de um usuário que não foi cadastrado"""
    repositorio = RepositorioUsuarios()
    rakon = Perfil('Rakon')
    try:
      repositorio.atualizar(rakon)
      self.fail("Deve lançar uma exceção de UNCException")
    except UNCException :
      pass

  def test_lista_usuarios(self):
    """Testa a listagem de usuários cadastrados"""
    repositorio = RepositorioUsuarios()
    rakon = Perfil('Rakon')
    jolyne = Perfil('Jolyne')
    marshal = Perfil('Marshal')
    
    repositorio.cadastrar(rakon)
    repositorio.cadastrar(jolyne)
    repositorio.cadastrar(marshal) 

    usuarios = repositorio.get_usuarios()
    self.assertEqual(len(usuarios), 3)
    self.assertIn(rakon, usuarios)
    self.assertIn(jolyne, usuarios)
    self.assertIn(marshal, usuarios)
    

class TestPerfil(unittest.TestCase):
  def test_add_tweet(self):
    francisca = Perfil('francisca')
    teste = Tweet('francisca','teste')
    francisca.add_tweet(teste)
    self.assertEqual(francisca.get_num_tweets(), 1)

  def test_add_seguidos(self):
    francisca = Perfil('francisca')
    joao = Perfil('joao')
    francisca.add_seguidos(joao)
    self.assertEqual(len(francisca.get_seguidos()), 1)

  def test_add_seguidor(self):
    francisca = Perfil('francisca')
    joao = Perfil('joao')
    francisca.add_seguidor(joao)
    self.assertEqual(len(francisca.get_seguidores()), 1)

  def test_get_tweet(self):
    francisca = Perfil('francisca')
    teste = Tweet('francisca','teste')
    francisca.add_tweet(teste)
    id = teste.get_id()
    self.assertEqual(francisca.get_tweet(id), teste)

  def test_get_usuario(self):
    francisca = Perfil('francisca')
    self.assertEqual(francisca.get_usuario(), 'francisca')

  def test_set_usuario(self):
    francisca = Perfil('francisca')
    francisca.set_usuario('francisca_xane')
    self.assertEqual(francisca.get_usuario(), 'francisca_xane')

  def test_is_ativo(self):
    francisca = Perfil('francisca')
    self.assertEqual(francisca.is_ativo(), True)

  def test_is_inativo(self):
    francisca = Perfil('francisca')
    francisca.set_inativo()
    self.assertEqual(francisca.is_ativo(), False)

  def test_get_seguidores(self):
    francisca = Perfil('francisca')
    joao = Perfil('joao')
    francisca.add_seguidor('joao')
    self.assertEqual(francisca.get_seguidores(), ['joao'])

  def test_get_seguidos(self):
    francisca = Perfil('francisca')
    joao = Perfil('joao')
    francisca.add_seguidos('joao')
    self.assertEqual(francisca.get_seguidos(), ['joao'])

  def test_numero_seguidores(self):
    francisca = Perfil('francisca')
    joao = Perfil('joao')
    maria = Perfil('maria')
    francisca.add_seguidor(joao)
    francisca.add_seguidor(maria)
    self.assertEqual(francisca.get_numero_seguidores(), 2)

  def test_get_tweets(self):
    francisca = Perfil('francisca')
    tweet3 = Tweet('francisca','teste')
    tweet2 = Tweet('francisca','teste')
    tweet1 = Tweet('francisca','teste')
    francisca.add_tweet(tweet1)
    francisca.add_tweet(tweet2)
    francisca.add_tweet(tweet3)
    self.assertEqual(francisca.get_tweets(), [tweet1, tweet2, tweet3])


  def test_get_timeline(self):
    francisca = Perfil('francisca')
    joao = Perfil('joao')
    tuite = Tweet('joao', 'primeiro tweet!!') 
    tuite2 = Tweet('francisca', 'segundo tweet!!')
    joao.add_tweet(tuite)
    francisca.add_tweet(tuite2)
    francisca.add_seguidos(joao)
    self.assertEqual(francisca.get_timeline(), [tuite, tuite2])

class TestPessoaFisica(unittest.TestCase):
  def test_get_cpf(self):
    francisca = PessoaFisica('francisca', '1406')
    self.assertEqual(francisca.get_cpf(), '1406')


class TestPessoaJuridica(unittest.TestCase):
  def test_get_cnpj(self):
    francisca = PessoaJuridica('francisca_lanches', '4970')
    self.assertEqual(francisca.get_cnpj(), '4970')

if __name__ == '__main__':
  unittest.main()
