import requests,json,sys,datetime,os
from tabulate import tabulate
import tkinter as tk
from PIL import Image,ImageTk
from io import BytesIO 

ano_atual = datetime.date.today().year
try:
    ano_informado = int(input(f"Informe o ano (2021 a {ano_atual}): "))
except ValueError:
    sys.exit("\nErro: O ano informado deve ser um número inteiro.")

while ano_informado < 2021 or ano_informado > ano_atual:
    try:
        ano_informado = int(input(f"Ano inválido. Informe um ano entre 2021 e {ano_atual}: "))
    except ValueError:
        sys.exit("\nErro: O ano informado deve ser um número inteiro.")
try:
    if ano_informado == ano_atual:
        strURL = 'https://api.cartolafc.globo.com/atletas/mercado'
        dictCartola = requests.get(strURL).json()
    else:
        nome_arquivo = f'cartola_fc_{ano_informado}.json'
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            dictCartola = json.load(file)
except requests.exceptions.RequestException as e:
    sys.exit("\nErro ao fazer a requisição:", e)
except FileNotFoundError:
    sys.exit(f"\nErro: O arquivo {nome_arquivo} não foi encontrado.")
except json.JSONDecodeError:
    sys.exit(f"\nErro ao decodificar o arquivo {nome_arquivo}.")  
except UnicodeDecodeError:
    sys.exit(f"\nErro ao decodificar o arquivo {nome_arquivo} devido à codificação incorreta.")
escalacao_disponiveis = {
    1: '3-4-3',
    2: '3-5-2',
    3: '4-3-3',
    4: '4-4-2',
    5: '4-5-1',
    6: '5-3-2',
    7: '5-4-1'
}
print("Escolha uma das escalações que estão disponíveis :")
tabela_escalacoes = [[num, escalacao] for num, escalacao in escalacao_disponiveis.items()]
print(tabulate(tabela_escalacoes, headers=['Número', 'Escalação'], tablefmt='fancy_grid'))
try:
    escalacao_escolhida = int(input("Informe o numero (1 a 7) da escalação que você deseja escolher : "))
except ValueError:
    sys.exit("Erro: A escolha deve ser um número inteiro.")

while escalacao_escolhida < 1 or escalacao_escolhida > 7:
    try:
        escalacao_escolhida = int(input("Escalação invalida. Escolha uma escalação dentre as apresentadas : "))
    except ValueError:
        sys.exit("Erro: A escolha deve ser um número inteiro.")
        
esquemas_taticos = {
    '3-4-3': {'goleiro': 1, 'zagueiro': 3, 'lateral': 0, 'meia': 4, 'atacante': 3, 'tecnico': 1},
    '3-5-2': {'goleiro': 1, 'zagueiro': 3, 'lateral': 0, 'meia': 5, 'atacante': 2, 'tecnico': 1},
    '4-3-3': {'goleiro': 1, 'zagueiro': 2, 'lateral': 2, 'meia': 3, 'atacante': 3, 'tecnico': 1},
    '4-4-2': {'goleiro': 1, 'zagueiro': 2, 'lateral': 2, 'meia': 4, 'atacante': 2, 'tecnico': 1},
    '4-5-1': {'goleiro': 1, 'zagueiro': 2, 'lateral': 2, 'meia': 5, 'atacante': 1, 'tecnico': 1},
    '5-3-2': {'goleiro': 1, 'zagueiro': 3, 'lateral': 2, 'meia': 3, 'atacante': 2, 'tecnico': 1},
    '5-4-1': {'goleiro': 1, 'zagueiro': 3, 'lateral': 2, 'meia': 4, 'atacante': 1, 'tecnico': 1},
}
esquema_selecionado = escalacao_disponiveis[escalacao_escolhida]
quantidade_posicoes = esquemas_taticos[esquema_selecionado]
selecionados = {}
for posicao, quantidade in quantidade_posicoes.items():
    posicao_id = {
        'goleiro': 1,
        'zagueiro': 3,
        'lateral': 2,
        'meia': 4,
        'atacante': 5,
        'tecnico': 6
    }[posicao]
    
    jogadores = [atleta for atleta in dictCartola['atletas'] if atleta['posicao_id'] == posicao_id]
    
    for atleta in jogadores:
        atleta['pontuacao_total'] = round(atleta.get('media_num', 0) * atleta.get('jogos_num', 0), 2)
    
    jogadores = sorted(jogadores, key=lambda x: x.get('pontuacao_total', 0), reverse=True)[:quantidade]
    
    selecionados[posicao] = jogadores

cartola_selecao = {}
for posicao, atletas in selecionados.items():
    for atleta in atletas:
        id_atleta = atleta['atleta_id']
        foto_url = atleta.get('foto', '')
        foto_url = foto_url.replace('_FORMATO_', '_220x220_').replace('_FORMATO', '_220x220')

        # Verificando se o clube existe no dicionário de clubes
        clube_id = str(atleta['clube_id'])
        clube_nome = dictCartola['clubes'].get(clube_id, {}).get('nome', 'Clube Desconhecido')
        escudo_url = dictCartola['clubes'].get(clube_id, {}).get('escudos', {}).get('60x60', '')

        cartola_selecao[id_atleta] = {
            'id': id_atleta,
            'nome': atleta.get('nome', 'Desconhecido'),
            'apelido': atleta.get('apelido', 'Sem Apelido'),
            'url_foto': foto_url,
            'clube': clube_nome,
            'escudo': escudo_url,
            'id_posicao': atleta['posicao_id'],
            'nome_posicao': posicao,
            'pontuacao': atleta.get('pontuacao_total', 0)
        }
try:
    with open(f'cartola_selecao_{esquema_selecionado}_{ano_informado}.json', 'w', encoding='utf-8') as outfile:
        json.dump(cartola_selecao, outfile, indent=4, ensure_ascii=False, )
except IOError:
    sys.exit("Erro ao salvar o arquivo JSON.")    
print("\nSeleção do Cartola FC:")
tabela_selecao = []
for posicao in ['goleiro', 'zagueiro', 'lateral', 'meia', 'atacante', 'tecnico']:
    if posicao in selecionados:
        for atleta in selecionados[posicao]:
            clube_id = str(atleta['clube_id'])
            clube_nome = dictCartola['clubes'].get(clube_id, {}).get('nome', 'Clube Desconhecido')
            tabela_selecao.append([
                atleta['nome'],
                atleta['apelido'],
                clube_nome,
                posicao.capitalize(),
                f"{atleta.get('pontuacao_total', 0):.2f}"
            ])

print(tabulate(tabela_selecao, headers=['Nome', 'Apelido', 'Clube', 'Posição', 'Pontuação'], tablefmt='fancy_grid'))
with open(f'cartola_selecao_{esquema_selecionado}_{ano_informado}.json', 'r') as f:
    cartola_selecao = json.load(f)
