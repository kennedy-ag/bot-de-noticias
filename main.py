import buscador
import bot

opcao = int(input("o que você deseja fazer?\n1 - Buscar notícias\n2 - Atualizar o bot\n"))
if(opcao==1):
  buscador.busca_noticias("noticias.json", "arquivo.tmp")
elif(opcao==2):
  bot.manda_noticia("noticias.json")
else:
  print("Opção inválida!")