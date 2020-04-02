#faz as importações necessárias
import telepot
import json
import minhas_funcoes as mf
import time
import os

#cria o bot e guarda o id da conversa em que ele está
bot = telepot.Bot("690502812:AAHS7XRYaTV9GSADhYdNbvTN_5zs5P1SOTE")
chat_id = -1001437678543

#função para enviar as notícias para o Telegram
def manda_noticia(arquivo):
  #variáveis de controle de envios
  contador = 0
  repetidas = 0

  if (os.path.exists("noticias.json")):
    ultimo_envio = "ultimo_envio.tmp" 
    a = open('noticias.json', 'r')
    noticias = json.loads(a.read())
    a.close()

    chaves_organizadas = sorted(noticias.keys())

    if(os.path.exists(ultimo_envio)):
      dt_ultimo_envio = mf.getTmpData(ultimo_envio)
      data_ultima_enviada = dt_ultimo_envio
      dt_ultimo_envio = mf.getDT(dt_ultimo_envio)

      #atualiza o arquivo com a data do último envio
      a = open(ultimo_envio, 'w')
      a.write(data_ultima_enviada)
      a.close()

      for i in range(len(chaves_organizadas)):
        dt_da_chave = mf.getDT(str(chaves_organizadas[i]))
        if(dt_da_chave > dt_ultimo_envio):
          contador += 1
          noticia = "{0}\n{1}\n\n{2}\n\n{3}\n\n{4}".format(
            noticias[chaves_organizadas[i]][0],
            chaves_organizadas[i],
            noticias[chaves_organizadas[i]][1], 
            noticias[chaves_organizadas[i]][2], 
            noticias[chaves_organizadas[i]][3])
          
          bot.sendMessage(chat_id, noticia, parse_mode="HTML")
          time.sleep(2)
        elif(contador == 0 and repetidas == 0):
          repetidas += 1

    else:
      while chaves_organizadas!=[]:
        noticia = "{0}\n{1}\n\n{2}\n\n{3}\n\n{4}".format(
          noticias[chaves_organizadas[0]][0],
          chaves_organizadas[0], 
          noticias[chaves_organizadas[0]][1], 
          noticias[chaves_organizadas[0]][2], 
          noticias[chaves_organizadas[0]][3])
        
        ultima_msg_enviada = chaves_organizadas[0]
        del noticias[chaves_organizadas[0]]
        del(chaves_organizadas[0])

        bot.sendMessage(chat_id, noticia, parse_mode="HTML")
        time.sleep(2)

        a = open(ultimo_envio,'w')
        a.write(ultima_msg_enviada)
        a.close()

    os.remove("noticias.json")

  else:
    print("Arquivo de notícias não existe!")

if __name__ == "__main__":
  manda_noticia("noticias.json")