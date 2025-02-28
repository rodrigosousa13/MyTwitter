import locale
from typing import List
from classes import *
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from time import sleep
from classes.users import usuarios_padrao

# Define a localidade para português brasileiro
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

titulo = r"""
     .-.      __  __    _______       _ _   _           
    /'v'\    |  \/  |  |__   __|     (_) | | |           
   (/   \)   | \  / |_   _| |_      ___| |_| |_ ___ _ __ 
  ='="="===< | |\/| | | | | \ \ /\ / / | __| __/ _ \ '__|
     |_|     | |  | | |_| | |\ V  V /| | |_| ||  __/ |   
             |_|  |_|\__, |_| \_/\_/ |_|\__|\__\___|_|   
                      __/ |                              
                     |___/                               """

def back_menu():
   """Função para controlar a volta ao menu principal com um input do usuário"""
   
   input('[** Aperte Enter para voltar **]')
   console = Console()
   console.clear()
   with console.status('carregando'):
      sleep(0.5) 

def exibir_menu_principal() -> int:
   """Exibe o menu principal do programa

   :return: Retorna a opção escolhida pelo usuário
   """

   texto_console="""1. Criar um perfil
2. Consultar um perfil
3. Ver perfis cadastrados 
4. Sair do programa"""

   console = Console()
   console.clear()
   console.print("[white]Bem vindo ao terminal do[/]".center(70, ' '))
   console.print(f'[bold blue]{titulo}[/]')
   console.print(Panel(texto_console, expand=False, border_style="#666666"))
      
   # Pede uma opção até que a entrada seja válida
   while True:
      opcao = int(input("\nDigite uma opção: "))
      if opcao not in range(1, 5):
         print('\nDigite uma opção válida!')
      else:
         return opcao

def exibir_timeline(timeline: List[Perfil], usuario: str):
   """Exibe a timeline de um usuário
   
   :param timeline: Lista de tweets da timeline de um usuario
   :param usuario: Nome do usuário
   """

   console = Console()
   console.print(f"[bold blue]{titulo}[/bold blue]\n",)
   console.print(f"[bold blue] Timeline de {usuario.capitalize()}[/bold blue] \n")
   tweets= []
   for i in timeline:
      user = i.get_usuario()
      msg = i.get_mensagem()
      data = i.get_data_postagem()
      tweets.append((user, msg, data))

   for tweet in tweets:
      usuario, texto, data = tweet
      tweet_text = Text(f"@{usuario}\n", style="e7e9ea")
      tweet_text.append(f" "*45)
      tweet_text.append(f"\n{texto}\n", style="#e7e9ea")
      tweet_text.append(" ")
      i = (f"Tweetado em {data.strftime("%H:%M %d de %B de %Y")}")

      console.print(Panel(tweet_text, expand=False, border_style="#666666", width=50, subtitle=i))


def exibir_tweets(timeline: List[Perfil], usuario: str):
   """Exibe a timeline de um usuário

   :param timeline: Lista de tweets da timeline de um usuario
   :param usuario: Nome do usuário
   """
   console = Console()
   console.print(f"[bold blue]{titulo}[/bold blue]\n",)
   console.print(f"[bold blue] Tweets de {usuario.capitalize()}[/bold blue] \n")
   tweets= []
   for i in timeline:
      user = i.get_usuario()
      msg = i.get_mensagem()
      data = i.get_data_postagem()
      tweets.append((user, msg, data))

   for tweet in tweets:
      usuario, texto, data = tweet
      tweet_text = Text(f"@{usuario}\n", style="e7e9ea")
      tweet_text.append(f" "*45)
      tweet_text.append(f"\n{texto}\n", style="#e7e9ea")
      tweet_text.append(" ")
      i = (f"Tweetado em {data.strftime("%H:%M %d de %B de %Y")}")

      console.print(Panel(tweet_text, expand=False, border_style="#666666", width=50, subtitle=i))
        

def exibir_perfil(twitter: MyTwitter, usuario: str) -> None:
   """Exibe a timeline de um usuário

   :param twitter: Classe que gerencia o sistema
   :param usuario: Nome do usuário
   """
   console = Console()
   perfil_text=Text('')
   i = (f"{usuario.capitalize()}")
   j = f"{twitter.get_instance_perfil(usuario)}"
   perfil_text.append(f"{len(twitter.tweets(usuario))} tweets")
   perfil_text.append(f" \n{len(twitter.seguidores(usuario))} seguidores")
   perfil_text.append(f" \n{len(twitter.seguidos(usuario))} seguindo")
   console.print(Panel(perfil_text, border_style="#666666", width=30, title = i, subtitle=j))


def exibir_menu_perfil(twitter: MyTwitter, usuario: str) -> int:
   """Exibe o menu de perfil de um usuário

   :param twitter: Classe que gerencia o sistema
   :param usuario: Nome do usuário
   :return: Retorna a opção escolhida pelo usuário
   """
   exibir_perfil(twitter, usuario)
   print("""1. Ver tweets
2. Ver timeline
3. Ver seguidores
4. Ver seguidos
5. Tweetar
6. Seguir perfil
7. Cancelar Perfil
8. Voltar ao menu principal""")

   # Pede uma opção até que a entrada seja válida
   while True:
      opcao = int(input("\nDigite uma opção: "))
      if opcao not in range(1, 9):
         print('\nDigite uma opção válida!')
      else:
         return opcao

# Loop principal
def main():
   """Executa o fluxo principal do programa"""

   # Inicializando MyTwitter e a função geradora de IDs
   twitter = MyTwitter()
   gerador_global = gerador_id()

   # Cadastrando usuários default
   usuarios_padrao(twitter)

   while True:
      try:

         opcao = exibir_menu_principal()

         if opcao == 1:  # Criar um perfil
            usuario = input("Nome de usuário: ")

            # Checar tipo do perfil
            numero = ''
            while True:
               tipo_perfil = input("Você é uma pesssoa física ou jurídica? [F/J]: ")
               if len(tipo_perfil) == 0:
                  print('Digite uma opção válida.')
                  continue
               if tipo_perfil in 'fF':
                  numero = input('CPF: ')
                  twitter.criar_perfil(PessoaFisica(usuario, numero))
                  break
               elif tipo_perfil in 'jJ':
                  numero = input('CNPJ: ')
                  twitter.criar_perfil(PessoaJuridica(usuario, numero))
                  break
               else:
                  print('Digite uma opção válida.')

            print('Cadastrado com sucesso.')

         elif opcao == 2:  # Consultar um perfil
            usuario = input("Nome de usuário: ")
            
            # Caso usuário inativo/inexistente
            if not twitter.existe_usuario(usuario):
               print('Usuário inativo ou inexistente.')
               back_menu()
               continue    # Volta ao menu principal

            # Loop do menu de perfil
            while True:
               console = Console()
               console.clear()
               opcao = exibir_menu_perfil(twitter, usuario)
               console.clear()

               if opcao == 1:  # ver tweets
                  exibir_tweets(twitter.tweets(usuario), usuario)

               elif opcao == 2:  # Ver timeline
                  exibir_timeline(twitter.timeline(usuario), usuario)

               elif opcao == 3:  # Ver seguidores
                  console.print((f'[bold blue]Seguidores de {usuario.capitalize()}: [/]\n'))
                  for seguidor in twitter.seguidores(usuario):
                     exibir_perfil(twitter, seguidor.get_usuario())
                  console.rule(style='bold black')

               elif opcao == 4:  # Ver seguidos
                  console.print((f'[bold blue]Seguidos de {usuario.capitalize()}: [/]\n'))
                  for seguido in twitter.seguidos(usuario):
                     exibir_perfil(twitter, seguido.get_usuario()) 
                  console.rule(style='bold black')

               elif opcao == 5:  # Tweetar
                  mensagem = input('Mensagem: ')
                  twitter.tweetar(usuario, mensagem, gerador_global)

                  print('Tweet postado com sucesso.')

               elif opcao == 6:  # Seguir perfil
                  try:
                     seguido = input('Nome do perfil a ser seguido: ')
                     twitter.seguir(usuario, seguido)
                  except PJSException:
                     print('Você já segue esse perfil!')
                  else:
                     print(f'Você segue {seguido} agora!')

               elif opcao == 7:  # Cancelar perfil
                  twitter.cancelar_perfil(usuario)

                  print('Cancelado com sucesso.')
                  back_menu()
                  break

               elif opcao == 8:  # Voltar ao menu principal
                  break

               back_menu()  # Volta para o menu de perfil

            continue  # Volta para o menu principal

         elif opcao == 3:  # Ver perfis cadastrados
            usuarios = twitter.usuarios_cadastrados()
            print(f'Exibindo {len(usuarios)} perfis:')
            for usuario in usuarios:
               print(f'\t-{usuario}')

         elif opcao == 4:  # Consultar um perfil
            break

      except Exception as e:
         print(f'Erro: {e}')

      back_menu()


if __name__ == '__main__':
   main()
