import sys

class Paciente:
    """Classe que representa um paciente na fila."""
    def __init__(self, nome, idade, prioridade):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade  # 'P' (prioritário) ou 'N' (normal)
        self.anterior = None
        self.proximo = None


class FilaAtendimento:
    """Classe que representa a fila duplamente encadeada de pacientes."""
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.qtd_prioritarios = 0
        self.qtd_normais = 0
        self.contador_atendimento = 0

    # ---------------- MONITORAMENTO DE MEMÓRIA ---------------- #
    def monitorar_memoria(self):
        total = sys.getsizeof(self)
        atual = self.inicio
        while atual:
            total += sys.getsizeof(atual)
            atual = atual.proximo
        return total

    # ---------------- OPERAÇÕES DA FILA ---------------- #
    def adicionar_paciente(self, nome, idade, prioridade):
        antes = self.monitorar_memoria()
        novo = Paciente(nome, idade, prioridade)

        if self.inicio is None:
            self.inicio = self.fim = novo
        elif prioridade == 'P':
            atual = self.inicio
            ultimo_prioritario = None
            while atual and atual.prioridade == 'P':
                ultimo_prioritario = atual
                atual = atual.proximo
            if ultimo_prioritario is None:
                novo.proximo = self.inicio
                self.inicio.anterior = novo
                self.inicio = novo
            else:
                novo.proximo = ultimo_prioritario.proximo
                if ultimo_prioritario.proximo:
                    ultimo_prioritario.proximo.anterior = novo
                else:
                    self.fim = novo
                novo.anterior = ultimo_prioritario
                ultimo_prioritario.proximo = novo
        else:
            self.fim.proximo = novo
            novo.anterior = self.fim
            self.fim = novo

        if prioridade == 'P':
            self.qtd_prioritarios += 1
        else:
            self.qtd_normais += 1

        depois = self.monitorar_memoria()
        print(f"Memória antes: {antes} bytes | depois: {depois} bytes | diferença: {depois - antes} bytes")

    def remover_paciente(self):
        antes = self.monitorar_memoria()
        if not self.inicio:
            print("Fila vazia.")
            return

        self.contador_atendimento += 1

        # alternância de 1 prioritário a cada 7 normais
        if self.qtd_prioritarios > 0 and self.qtd_normais >= 7:
            if self.contador_atendimento % 8 == 0:
                atual = self.inicio
                while atual and atual.prioridade != 'P':
                    atual = atual.proximo
                if atual:
                    if atual.anterior:
                        atual.anterior.proximo = atual.proximo
                    else:
                        self.inicio = atual.proximo
                    if atual.proximo:
                        atual.proximo.anterior = atual.anterior
                    else:
                        self.fim = atual.anterior
                    print(f"Atendido prioritário: {atual.nome}")
                    self.qtd_prioritarios -= 1
                    depois = self.monitorar_memoria()
                    print(f"Memória antes: {antes} | depois: {depois} | diferença: {depois - antes}")
                    return

        atendido = self.inicio
        print(f"Atendido: {atendido.nome}")
        self.inicio = atendido.proximo
        if self.inicio:
            self.inicio.anterior = None
        else:
            self.fim = None

        if atendido.prioridade == 'P':
            self.qtd_prioritarios -= 1
        else:
            self.qtd_normais -= 1

        depois = self.monitorar_memoria()
        print(f"Memória antes: {antes} | depois: {depois} | diferença: {depois - antes}")

    def editar_paciente(self, nome, nova_idade, nova_prioridade):
        antes = self.monitorar_memoria()
        atual = self.inicio
        while atual:
            if atual.nome == nome:
                atual.idade = nova_idade
                atual.prioridade = nova_prioridade
                print(f"Paciente {nome} atualizado.")
                depois = self.monitorar_memoria()
                print(f"Memória antes: {antes} | depois: {depois} | diferença: {depois - antes}")
                return
            atual = atual.proximo
        print("Paciente não encontrado.")

    def exibir_fila(self, invertida=False):
        if not self.inicio:
            print("Fila vazia.")
            return
        elementos = []
        atual = self.inicio
        while atual:
            tipo = "(P)" if atual.prioridade == 'P' else "(N)"
            elementos.append(f"[{atual.nome} {tipo}]")
            atual = atual.proximo
        if invertida:
            elementos.reverse()
        print("\nFila atual:")
        print(" --> ".join(elementos))

# ---------------- MODO PRINCIPAL ---------------- #
def carregar_pacientes_iniciais(fila):
    """Cria automaticamente 10 pacientes misturados."""
    pacientes = [
        ("João", 35, 'P'), ("Maria", 40, 'N'),
        ("Carlos", 28, 'N'), ("Ana", 65, 'P'),
        ("Pedro", 50, 'N'), ("Luiza", 32, 'N'),
        ("Rafaela", 47, 'P'), ("Tiago", 29, 'N'),
        ("Clara", 70, 'P'), ("Felipe", 25, 'N')
    ]
    for nome, idade, prio in pacientes:
        fila.adicionar_paciente(nome, idade, prio)

def modo_menu(fila):
    """Menu tradicional de opções."""
    while True:
        print("\n" + "="*60)
        print("SIMULAÇÃO DE FILA DE ATENDIMENTO MÉDICO")
        print("="*60)
        print("1 - Adicionar paciente")
        print("2 - Remover paciente")
        print("3 - Alterar paciente")
        print("4 - Exibir fila")
        print("5 - Exibir fila invertida")
        print("0 - Sair")
        print("="*60)
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            prio = input("Prioridade (P/N): ").upper()
            fila.adicionar_paciente(nome, idade, prio)
        elif opcao == "2":
            fila.remover_paciente()
        elif opcao == "3":
            nome = input("Nome do paciente a alterar: ")
            idade = int(input("Nova idade: "))
            prio = input("Nova prioridade (P/N): ").upper()
            fila.editar_paciente(nome, idade, prio)
        elif opcao == "4":
            fila.exibir_fila()
        elif opcao == "5":
            fila.exibir_fila(invertida=True)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def modo_comandos(fila):
    """Modo de comandos diretos."""
    print("\nComandos disponíveis:")
    print("add <nome> <idade> <P/N>")
    print("assist")
    print("edit <nome> <nova_idade> <P/N>")
    print("show")
    print("show inv")
    print("exit")

    while True:
        cmd = input("\n> ").strip().split()
        if not cmd:
            continue
        if cmd[0] == "add" and len(cmd) == 4:
            fila.adicionar_paciente(cmd[1], int(cmd[2]), cmd[3].upper())
        elif cmd[0] == "assist":
            fila.remover_paciente()
        elif cmd[0] == "edit" and len(cmd) == 4:
            fila.editar_paciente(cmd[1], int(cmd[2]), cmd[3].upper())
        elif cmd[0] == "show":
            fila.exibir_fila(invertida=(len(cmd) > 1 and cmd[1] == "inv"))
        elif cmd[0] == "exit":
            break
        else:
            print("Comando inválido.")

# ---------------- EXECUÇÃO ---------------- #
if __name__ == "__main__":
    fila = FilaAtendimento()
    carregar_pacientes_iniciais(fila)

    print("=== SELECIONE O MODO DE OPERAÇÃO ===")
    print("1 - Modo com MENU")
    print("2 - Modo com COMANDOS")
    escolha = input("Escolha: ")

    if escolha == "1":
        modo_menu(fila)
    elif escolha == "2":
        modo_comandos(fila)
    else:
        print("Opção inválida. Encerrando...")
