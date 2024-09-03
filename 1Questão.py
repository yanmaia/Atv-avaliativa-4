import requests,sys,datetime
strURL = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata'
strURL += '/Moedas?$top=100&$format=json'
dictMoedas = requests.get(strURL).json()
codigomoeda= [moeda['simbolo']for moeda in dictMoedas['value']] 
nomemoeda= [nome['nomeFormatado']for nome in dictMoedas['value']]
anoatual=(datetime.date.today().year)

while True:
    print (f"\n{'---'*10}Estas são todas as moedas disponiveis{'---'*10}")
    for i in range(len(codigomoeda)):
        print(f'|{codigomoeda[i]}-{nomemoeda[i]}')    
    print('\nCaso queira sair digite 0')
    moeda=input('\nInforme a moeda:').upper()   
    if moeda =='0':break
    if moeda not in codigomoeda:
        print('\nEssa moeda não e valida, use as moedas disponiveis')
        continue
    ano=int(input(f'\nInforme o ano desejado da consulta entre 1980 e {anoatual}:'))
    if ano ==0:break
                         #verifica se a moeda e valida
    if ano> anoatual or ano < 1980:
        print('\nO ano Desejado Não e valido, siga as instruções')                # Verifica se o ano e superior que  o atual
        continue
                    #verifica se a moeda e valida
   
    strURL = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/'
    strURL += 'CotacaoMoedaPeriodo(moeda=@moeda,dataInicial='
    strURL += '@dataInicial,dataFinalCotacao=@dataFinalCotacao)?'
    strURL += f'@moeda=%27{moeda}%27&@dataInicial=%2701-01-{ano}%27&'
    strURL += f'@dataFinalCotacao=%2712-31-{ano}%27&$top=100&$format=json'
    dictCotacoes = requests.get(strURL).json()
    print(dictCotacoes)