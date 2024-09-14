import random,time,ast

try:
    def gerarcartelas():
        cartela = []
        colunas = {
            'B': range(1, 16),
            'I': range(16, 31),
            'N': range(31, 46),
            'G': range(46, 61),
            'O': range(61, 76)
        }
        for letras in colunas:
            numeros = sorted(random.sample(colunas[letras], 5))
            cartela.append(numeros)
        return cartela
    def salvar_cartelas(cartelas):
        dict_cartelas = {}
        colunas = ['B', 'I', 'N', 'G', 'O']        
        for numero_cartela, cartela in enumerate(cartelas, start=1):
            cartela_com_letras = []
            for letra, numeros in zip(colunas, cartela):
                cartela_com_letras.append([f"{letra}{num}" for num in numeros])
            dict_cartelas[numero_cartela] = cartela_com_letras
        with open('cartelas.txt', 'w') as arquivo:
            arquivo.write("{\n")
            for numero, cartela in dict_cartelas.items():
                cartela_str = str(cartela).replace('[', '[').replace(']', ']')
                arquivo.write(f" {numero}: {cartela_str},\n")
            arquivo.write("}\n")            
        print("\nCartelas salvas com sucesso em 'cartelas.txt'!")
        time.sleep(2)
    def ler_cartelas():
        with open('cartelas.txt', 'r') as arquivo:
            conteudo = arquivo.read()
        dict_cartelas = ast.literal_eval(conteudo)       
        cartelas = []
        for cartela_letras in dict_cartelas.values():
            cartela = []
            for letra_cartela in cartela_letras:
                numeros = [int(num[1:]) for num in letra_cartela]
                cartela.append(sorted(numeros))
            cartelas.append(cartela)       
        return cartelas
    def gerar_string_cartela(cartela, quantidades):
        cartela_string = f"+{'-' * 20}+\n" 
        cartela_string += f"| Cartela: {str(quantidades).zfill(5)}     |\n"
        cartela_string += f"+{'-' * 20}+\n"
        cartela_string += "+----+----+----+----+----+\n"
        cartela_string += "| B  | I  | N  | G  | O  |\n"
        cartela_string += "+----+----+----+----+----+\n"
        for i in range(5):
            linha = []
            for coluna in range(5):
                numero = str(cartela[coluna][i]).rjust(2) 
                linha.append(f" {numero} ")
            cartela_string += "|" + "|".join(linha) + "|\n"
            cartela_string += "+----+----+----+----+----+\n"
        return cartela_string    
    def imprimir_cartela(cartelas, numero_cartela):

        if 1 <= numero_cartela <= len(cartelas):
            cartela = cartelas[numero_cartela - 1]
            cartela_string = gerar_string_cartela(cartela, numero_cartela)
            print(cartela_string)
            return cartela
        else:
            print("\nNúmero da cartela inexistente.")    
            return None    
    def sortear_cartela(cartelas, cartela_escolhida):
        if not cartelas:
            print("Nenhuma cartela foi gerada. Não é possível iniciar o sorteio.")
            return
        if cartela_escolhida:
            numeros_sorteados = []
            cartela_escolhida_batida = False
            cartelas_batidas = []
            while True:
                nova_dezena = random.randint(1, 75)
                while nova_dezena in numeros_sorteados:
                    nova_dezena = random.randint(1, 75)
                numeros_sorteados.append(nova_dezena)
                numeros_sorteados.sort()
                print(f"\nNúmeros sorteados até agora: {numeros_sorteados}")
                print(f"Dezena sorteada: {nova_dezena}\n")
                if verificar_cartela(cartela_escolhida, numeros_sorteados):
                    cartela_escolhida_batida = True
                    print("\nSua cartela ganhou!")
                    break
                for i, cartela in enumerate(cartelas):
                    if cartela != cartela_escolhida and verificar_cartela(cartela, numeros_sorteados):
                        cartelas_batidas.append(i + 1)
                if cartelas_batidas:
                    print("\nOutra cartela ganhou:", cartelas_batidas)
                    print("Infelizmente, sua cartela não ganhou.")
                    break
                time.sleep(2)
            if not cartela_escolhida_batida and not cartelas_batidas:
                print("\nInfelizmente, sua cartela não ganhou desta vez.")
        else:
            print("Nenhuma cartela foi escolhida para o sorteio.")
    def verificar_cartela(cartela, numeros_sorteados):
        print("\nVerificando colunas das cartelas com os números sorteados:")
        for letra, coluna in zip('BINGO', cartela):
            coluna_sorteada = [num for num in coluna if num in numeros_sorteados]
            coluna_marcada = [f"{num}*" if num in numeros_sorteados else str(num) for num in coluna]
            print(f"Coluna {letra}: {coluna_marcada} (Números sorteados: {coluna_sorteada})")
            if len(coluna_sorteada) != len(coluna):
                return False
        return True   
    def menu():
        cartelas = []
        cartela_escolhida = None
        while True:
            print ('\n - \n')
            print("Menu:\n")
            print("Gerar Cartelas - (1)")
            print("Salvar Cartelas - (2)")
            print("Ler Cartelas - (3)")
            print("Imprimir Cartela - (4)")
            print("Sorteio do Bingo - (5)")
            print("Sair - (6)")
            escolha = input("\nEscolha uma opção:\n")         

            if escolha == '1':
                try:
                    quantas_cartelas = int(input('Quantas cartelas deseja gerar? '))
                    if 1 <= quantas_cartelas <= 10000:
                        cartelas = [gerarcartelas() for _ in range(quantas_cartelas)]
                        print(f"\n{quantas_cartelas} cartelas geradas com sucesso!")
                        print('Qual será o próximo passo agora?')
                        time.sleep(2)
                    else:
                        print("O número deve estar entre 1 e 10.000.")
                        time.sleep(2)
                        return menu()
                except ValueError:
                    print("Erro: Por favor, insira um número válido.")
                except NameError:
                    print("\nErro: Por favor, não coloque caractere.")
                    time.sleep(2)
                    return menu()       

            elif escolha == '2':
                if cartelas:
                    salvar_cartelas(cartelas)                   
                else:
                    print("Nenhuma cartela foi gerada.")

            elif escolha == '3':
                try:
                    cartelas = ler_cartelas()
                    if cartelas:
                        for i, cartela in enumerate(cartelas):
                            cartela_string = gerar_string_cartela(cartela, i + 1)
                            print(cartela_string)
                        print('Ok... e agora?')
                        time.sleep(2)
                    else:
                        print("Nenhuma cartela foi encontrada no arquivo.")
                except FileNotFoundError:
                    print('\nO programa deu erro por não encontrar um arquivo existente.')  
                    time.sleep(2)  
                    return menu()                            

            elif escolha == '4':
                if cartelas:
                    try:
                        numero_cartela = int(input("Digite o número da cartela que deseja imprimir: "))
                        cartela_escolhida = imprimir_cartela(cartelas, numero_cartela)
                        print('\nVamos ao sorteio agora?!')
                        time.sleep(2)
                    except ValueError:
                        print("Erro: Por favor, insira um número válido.")
                    except FileNotFoundError:
                        print('\nO programa deu erro por não encontrar um arquivo existente.') 
                        time.sleep(2)  
                        return menu()
                    except NameError:
                        print("\nErro: Por favor, não coloque caractere.")
                        time.sleep(2)
                        return menu()
                else:
                    print("Nenhuma cartela foi gerada. Primeiro escolha a opção (Gerar Cartelas - 1)")
                    time.sleep(2)

            elif escolha == '5':
                if cartelas:
                    print("Iniciando sorteio...\n")
                    time.sleep(3)
                    while True:
                        if cartela_escolhida:
                            sortear_cartela(cartelas, cartela_escolhida)
                            repetir = input("\nDeseja repetir o sorteio com a mesma cartela? (s/n): ").lower()
                            if repetir != 's':
                                print('Voltando ao Menu...')
                                time.sleep(2)
                                return menu()
                        else:
                            print("Nenhuma cartela foi escolhida para o sorteio.")
                            print('Voltando ao Menu...')
                            time.sleep(2)
                            return menu()
                else:
                    print("Nenhuma cartela foi gerada.")
                    print('Voltando ao Menu...')
                    time.sleep(2)
                    return menu()

            elif escolha == '6':
                print("Saindo...")
                break

            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(2)

    menu()            

except Exception as e:
    print('\nO programa deu o seguinte erro:', e)
