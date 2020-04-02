#faz as importações necessárias
import json
import minhas_funcoes as mf
from bs4 import BeautifulSoup
import os

def busca_noticias(nomeArquivoJson, nomeArquivoTmp):
  #cria as lista para cada tipo de informação a ser guardada
  lista_de_horarios = []
  lista_de_imagens = []
  lista_de_titulos = []
  lista_de_descricoes = []
  lista_de_links = []

  #coleta a resposta http e cria o objeto soup
  link_base = "http://www.ifb.edu.br/brasilia/noticiasbrasilia"
  resposta_http = mf.getPage(link_base)
  objeto_soup = BeautifulSoup(resposta_http.read(), features="html.parser")

  #cria listas com informações sem formatação
  horario = mf.getDataHora(objeto_soup)
  imagem = mf.getImagem(objeto_soup)
  titulo = mf.getTitle(objeto_soup)
  descricao = mf.getDescricao(objeto_soup)
  link = mf.getUrlNoticia(objeto_soup)

  #verifica se existe algo no retorno
  if(horario!=None and imagem!=None and titulo!=None and descricao!=None and link!=None):
    
    #adiciona os textos formatados às listas correspondente
    for i in range(0, len(titulo)):
      lista_de_horarios.append(horario[i].strip())
      lista_de_imagens.append('<a href="{}{}">.</a>'.format("https://www.ifb.edu.br", imagem[i]))
      lista_de_titulos.append("<b>"+titulo[i].get_text().strip()+"</b>")
      lista_de_descricoes.append(descricao[i].get_text().strip())
      lista_de_links.append("https://www.ifb.edu.br{}".format(link[i]))
  else:
    print("Ocorreu um erro na captura das informações!")

  #cria um dicionário com as notícias coletadas
  lista_de_noticias = {}
  for i in range(0, len(lista_de_titulos)): #testes aqui
    lista_de_noticias[lista_de_horarios[i]] = \
    (
      lista_de_imagens[i],
      lista_de_titulos[i],
      lista_de_descricoes[i],
      lista_de_links[i]
    )

  #nomeArquivoJson = "noticias.json"
  #nomeArquivoTmp = 'arquivo.tmp'

  if (os.path.exists(nomeArquivoJson)):
    a = open(nomeArquivoJson, "r")
    noticiasJs = json.loads(a.read())
    a.close()

    ultimaDataHora = mf.getTmpData(nomeArquivoTmp)
    ultimaDataHora = mf.getDT(ultimaDataHora)

    # Dentro desse for estamos navegando nas chaves da lista de noticias

    for dataHora in lista_de_noticias.keys():
      dataHoraConvertida = mf.getDT(dataHora)
      # Dentro desse if teremos as datas e horas de noticias novas (que não estão no arquivo .json)
      if dataHoraConvertida > ultimaDataHora:
        noticiasJs[dataHora] = \
          (
            lista_de_noticias[dataHora][0],
            lista_de_noticias[dataHora][1],
            lista_de_noticias[dataHora][2],
            lista_de_noticias[dataHora][3]
          )
    # Fora do for, gerar o JSON novo e salvar no arquivo com o mesmo nome com permissão W
    a = open(nomeArquivoJson, 'w')
    js = json.dumps(noticiasJs, ensure_ascii=False, indent=2)
    js = str(js)
    a.write(js)
    a.close()
  else:
    js = json.dumps(lista_de_noticias, ensure_ascii=False, indent=2)
    js = str(js)
    a = open(nomeArquivoJson, 'w')
    a.write(js)
    a.close()

  #salva a data/hora da última notícia em arquivo temporário
  arquivo_tmp = open(nomeArquivoTmp, 'w')
  arquivo_tmp.write(list(lista_de_noticias.keys())[0])
  arquivo_tmp.close()

if __name__ == "__main__":
  busca_noticias("noticias.json", "arquivo.tmp")