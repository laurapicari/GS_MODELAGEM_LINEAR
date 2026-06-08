import time
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def efeito_digitacao(texto, delay=0.1):
    for caractere in texto:
        print(caractere, end="", flush=True)
        time.sleep(delay)
    print()


def digitar(texto, delay=0.05):
    for caractere in texto:
        print(caractere, end="", flush=True)
        time.sleep(delay)
    print()


def ler_float(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor == "":
            print("Você precisa digitar um valor. Tente novamente.")
            continue

        try:
            return float(valor.replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite apenas números.")


def ler_opcao_0_1(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor == "":
            print("Você precisa digitar 0 ou 1. Tente novamente.")
            continue

        try:
            valor = int(valor)
        except ValueError:
            print("Valor inválido. Digite apenas 0 ou 1.")
            continue

        if valor in [0, 1]:
            return valor
        else:
            print("Opção inválida. Digite apenas 0 ou 1.")


def ler_opcao_menu():
    while True:
        valor = input("Escolha uma opção: ").strip()

        if valor == "":
            print("Você precisa escolher uma opção do menu.")
            continue

        try:
            return int(valor)
        except ValueError:
            print("Digite apenas números.")


historico = []

temperatura_nave = None
nivel_energia = None
comunicacao = None
modulo_operacao = None

dados = None

# Arquivo .csv separado, entregue junto com este código
ARQUIVO_BASE = "base_satelites_github.csv"


def inserir_dados():
    temperatura = ler_float("Digite a temperatura da nave: ")
    print()

    energia = ler_float("Digite o nível de energia da nave em %: ")
    print()

    comunicacao = ler_opcao_0_1("""
0 = Afetado
1 = Operando
Digite o status de comunicação: """)
    print()

    modulo = ler_opcao_0_1("""
0 = Módulo com falha
1 = Módulo operando normalmente
Digite o status dos módulos de operação: """)
    print()

    leitura = [temperatura, energia, comunicacao, modulo]
    historico.append(leitura)

    efeito_digitacao("Carregando informações...", delay=0.08)
    print()

    return temperatura, energia, comunicacao, modulo


def visualizar_status(temperatura, energia, comunicacao, modulo):
    if temperatura is None:
        print("Nenhum dado foi inserido ainda.")
        return

    efeito_digitacao("STATUS ATUAL DA NAVE")
    print(f"Temperatura: {temperatura} °C")
    print(f"Nível de energia: {energia}%")

    if comunicacao == 0:
        print("Comunicação: Afetada")
    else:
        print("Comunicação: Operando")

    if modulo == 0:
        print("Módulos de operação: Com falha")
    else:
        print("Módulos de operação: Operando normalmente")

    print()


def executar_analise(temperatura, energia, comunicacao, modulo):
    if temperatura is None:
        print("Insira os dados antes de executar a análise.")
        return

    efeito_digitacao("Carregando informações...", delay=0.08)
    print()

    alerta_critico = False

    print("ANÁLISE AUTOMÁTICA DA MISSÃO")
    print()

    print("Temperatura:")
    if temperatura >= 80:
        digitar("Alerta de superaquecimento.")
        alerta_critico = True
    elif temperatura <= 20:
        digitar("Alerta de temperatura muito baixa.")
        alerta_critico = True
    else:
        digitar("Temperatura normal.")
    print()

    print("Energia:")
    if energia <= 10:
        digitar("Nível de energia crítico.")
        alerta_critico = True
    elif energia <= 20:
        digitar("Economia de energia recomendada.")
    else:
        digitar("Energia estável.")
    print()

    print("Comunicação:")
    if comunicacao == 0:
        digitar("Falha de comunicação detectada.")
        alerta_critico = True
    else:
        digitar("Comunicação estável.")
    print()

    print("Módulos de operação:")
    if modulo == 0:
        digitar("Falha em módulo operacional.")
        alerta_critico = True
    else:
        digitar("Módulos funcionando corretamente.")
    print()

    if alerta_critico:
        digitar("ALERTA GERAL: A missão apresenta situação crítica e exige intervenção.")
    else:
        digitar("STATUS GERAL: A missão está operando em condições seguras.")

    print()


def mostrar_historico():
    if len(historico) == 0:
        print("Nenhuma leitura foi registrada ainda.")
        return

    print("HISTÓRICO DAS LEITURAS")
    print()

    for i, leitura in enumerate(historico):
        temperatura = leitura[0]
        energia = leitura[1]
        comunicacao = leitura[2]
        modulo = leitura[3]

        print(f"Leitura {i + 1}:")
        print(f"Temperatura: {temperatura} °C")
        print(f"Energia: {energia}%")

        if comunicacao == 0:
            print("Comunicação: Afetada")
        else:
            print("Comunicação: Operando")

        if modulo == 0:
            print("Módulos: Com falha")
        else:
            print("Módulos: Operando normalmente")

        print()


def carregar_base_dados():
    global dados

    print("CARREGANDO BASE DE DADOS")
    print("Base: Amateur Satellite Database / SatNOGS")
    print("Fonte: GitHub")
    print(f"Arquivo utilizado: {ARQUIVO_BASE}")
    print()

    if not os.path.exists(ARQUIVO_BASE):
        print("Arquivo da base não encontrado.")
        print("Deixe o arquivo base_satelites_github.csv na mesma pasta deste código.")
        return

    try:
        dados = pd.read_csv(ARQUIVO_BASE)

        dados["launched"] = pd.to_datetime(dados["launched"], errors="coerce")
        dados["ano_lancamento"] = dados["launched"].dt.year

        data_atual = pd.Timestamp.today()
        dados["dias_em_orbita"] = (data_atual - dados["launched"]).dt.days

        dados["norad_cat_id"] = pd.to_numeric(dados["norad_cat_id"], errors="coerce")

        dados = dados.dropna(subset=["ano_lancamento", "dias_em_orbita", "status"])
        dados = dados[dados["dias_em_orbita"] > 0]

        dados["ano_lancamento"] = dados["ano_lancamento"].astype(int)
        dados["dias_em_orbita"] = dados["dias_em_orbita"].astype(int)

        print("Base carregada com sucesso!")
        print(f"Quantidade de linhas: {dados.shape[0]}")
        print(f"Quantidade de colunas: {dados.shape[1]}")
        print()

        print("Colunas utilizadas na análise:")
        print("- ano_lancamento: ano em que o satélite foi lançado")
        print("- dias_em_orbita: quantidade aproximada de dias desde o lançamento")
        print("- status: situação do satélite")
        print("- countries: país relacionado ao satélite")
        print("- norad_cat_id: identificador NORAD")
        print()

    except Exception as erro:
        print("Erro ao carregar a base de dados.")
        print(f"Detalhes: {erro}")


def verificar_base():
    if dados is None:
        print("A base ainda não foi carregada.")
        print("Use a opção 5 primeiro.")
        return False
    return True


def mostrar_tabela_como_imagem(tabela, titulo):
    tabela_exibida = tabela.copy()

    if len(tabela_exibida) > 20:
        tabela_exibida = tabela_exibida.head(20)

    for coluna in tabela_exibida.columns:
        tabela_exibida[coluna] = tabela_exibida[coluna].apply(
            lambda valor: f"{valor:.2f}" if isinstance(valor, (int, float, np.integer, np.floating)) else str(valor)
        )

    plt.figure(figsize=(12, 6))
    plt.axis("off")
    plt.title(titulo, fontsize=14, weight="bold", pad=20)

    tabela_plot = plt.table(
        cellText=tabela_exibida.values,
        colLabels=tabela_exibida.columns,
        loc="center",
        cellLoc="center",
        colLoc="center"
    )

    tabela_plot.auto_set_font_size(False)
    tabela_plot.set_fontsize(8)
    tabela_plot.scale(1, 1.5)

    plt.tight_layout()
    plt.show()


def montar_tabela_frequencia_discreta():
    if not verificar_base():
        return

    print("TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIAS")
    print("Variável quantitativa discreta: ano_lancamento")
    print()

    frequencia = dados["ano_lancamento"].value_counts().sort_index()
    frequencia_relativa = frequencia / frequencia.sum()
    percentual = frequencia_relativa * 100

    tabela = pd.DataFrame({
        "Ano de Lançamento": frequencia.index,
        "Frequência Absoluta": frequencia.values,
        "Frequência Relativa": frequencia_relativa.values,
        "Percentual (%)": percentual.values
    })

    print(tabela)
    print()

    mostrar_tabela_como_imagem(tabela, "Tabela de Frequência - Ano de Lançamento")

    tabela.to_csv("tabela_frequencia_discreta.csv", index=False)
    print("Tabela salva como: tabela_frequencia_discreta.csv")


def montar_tabela_frequencia_continua():
    if not verificar_base():
        return

    print("TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIAS")
    print("Variável quantitativa contínua: dias_em_orbita")
    print()

    valores = dados["dias_em_orbita"].dropna()

    quantidade_classes = int(np.sqrt(len(valores)))

    if quantidade_classes < 3:
        quantidade_classes = 3

    if quantidade_classes > 8:
        quantidade_classes = 8

    frequencia = pd.cut(valores, bins=quantidade_classes).value_counts().sort_index()
    frequencia_relativa = frequencia / frequencia.sum()
    percentual = frequencia_relativa * 100

    tabela = pd.DataFrame({
        "Intervalo de Dias em Órbita": frequencia.index.astype(str),
        "Frequência Absoluta": frequencia.values,
        "Frequência Relativa": frequencia_relativa.values,
        "Percentual (%)": percentual.values
    })

    print(tabela)
    print()

    mostrar_tabela_como_imagem(tabela, "Tabela de Frequência - Dias em Órbita")

    tabela.to_csv("tabela_frequencia_continua.csv", index=False)
    print("Tabela salva como: tabela_frequencia_continua.csv")


def gerar_graficos():
    if not verificar_base():
        return

    print("GERAÇÃO DE GRÁFICOS ESTATÍSTICOS")
    print()

    plt.figure(figsize=(8, 5))
    dados["status"].value_counts().plot(kind="bar", color="skyblue")
    plt.title("Quantidade de Satélites por Status")
    plt.xlabel("Status")
    plt.ylabel("Frequência")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("grafico_1_status_satelites.png")
    plt.show()
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(dados["dias_em_orbita"], bins=8, color="lightgreen", edgecolor="black")
    plt.title("Distribuição dos Dias em Órbita")
    plt.xlabel("Dias em órbita")
    plt.ylabel("Frequência")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("grafico_2_dias_em_orbita.png")
    plt.show()
    plt.close()

    print("Gráficos gerados e exibidos com sucesso!")
    print("- grafico_1_status_satelites.png")
    print("- grafico_2_dias_em_orbita.png")
    print()


def calcular_medidas(coluna):
    valores = dados[coluna].dropna()

    media = valores.mean()
    mediana = valores.median()

    moda = valores.mode()
    if len(moda) > 0:
        moda = moda.iloc[0]
    else:
        moda = "Não possui"

    maximo = valores.max()
    minimo = valores.min()
    amplitude = maximo - minimo
    variancia = valores.var()
    desvio_padrao = valores.std()

    if media != 0:
        coeficiente_variacao = (desvio_padrao / media) * 100
    else:
        coeficiente_variacao = 0

    q1 = valores.quantile(0.25)
    q2 = valores.quantile(0.50)
    q3 = valores.quantile(0.75)

    return {
        "Média": media,
        "Mediana": mediana,
        "Moda": moda,
        "Máximo": maximo,
        "Mínimo": minimo,
        "Amplitude": amplitude,
        "Variância": variancia,
        "Desvio Padrão": desvio_padrao,
        "Coeficiente de Variação (%)": coeficiente_variacao,
        "1º Quartil": q1,
        "2º Quartil": q2,
        "3º Quartil": q3
    }


def realizar_analise_univariada():
    if not verificar_base():
        return

    print("ANÁLISE UNIVARIADA COM ESTATÍSTICA DESCRITIVA")
    print("Variáveis analisadas: ano_lancamento e dias_em_orbita")
    print()

    analises = {
        "ano_lancamento": calcular_medidas("ano_lancamento"),
        "dias_em_orbita": calcular_medidas("dias_em_orbita")
    }

    resultado = []

    for variavel, medidas in analises.items():
        linha = {"Variável": variavel}
        linha.update(medidas)
        resultado.append(linha)

    tabela_resultado = pd.DataFrame(resultado)

    print(tabela_resultado)
    print()

    mostrar_tabela_como_imagem(tabela_resultado, "Análise Univariada - Estatística Descritiva")

    tabela_resultado.to_csv("analise_univariada.csv", index=False)
    print("Análise salva como: analise_univariada.csv")


while True:
    print()
    print("""MENU DO SISTEMA DA NAVE

1 - Inserir dados simulados da missão
2 - Visualizar status atual
3 - Executar análise automática da missão
4 - Histórico das leituras
5 - Carregar base de dados CSV
6 - Gerar tabela de frequência discreta
7 - Gerar tabela de frequência contínua
8 - Gerar gráficos estatísticos
9 - Realizar análise univariada
10 - Encerrar sistema""")
    print()

    opcao = ler_opcao_menu()

    print()

    if opcao == 1:
        temperatura_nave, nivel_energia, comunicacao, modulo_operacao = inserir_dados()

    elif opcao == 2:
        visualizar_status(temperatura_nave, nivel_energia, comunicacao, modulo_operacao)

    elif opcao == 3:
        executar_analise(temperatura_nave, nivel_energia, comunicacao, modulo_operacao)

    elif opcao == 4:
        mostrar_historico()

    elif opcao == 5:
        carregar_base_dados()

    elif opcao == 6:
        montar_tabela_frequencia_discreta()

    elif opcao == 7:
        montar_tabela_frequencia_continua()

    elif opcao == 8:
        gerar_graficos()

    elif opcao == 9:
        realizar_analise_univariada()

    elif opcao == 10:
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida. Tente novamente.")
