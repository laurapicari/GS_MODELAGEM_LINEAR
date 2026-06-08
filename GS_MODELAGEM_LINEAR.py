import time
import sys
import os
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def efeito_digitacao(texto, delay=0.1):
    for caractere in texto:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def digitar(texto, delay=0.05):
    for caractere in texto:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        time.sleep(delay)
    print()


historico = []

temperatura_nave = None
nivel_energia = None
comunicacao = None
modulo_operacao = None

dados = None

tabela_discreta = None
tabela_continua = None
analises_estatisticas = {}
graficos_gerados = []


# Base única escolhida:
# Amateur Satellite Database / SatNOGS
# Fonte: GitHub
URL_BASE = "https://raw.githubusercontent.com/palewire/amateur-satellite-database/main/data/satnogs.csv"


def inserir_dados():
    temperatura = float(input("Digite a temperatura da nave: "))
    print()

    energia = float(input("Digite o nível de energia da nave em %: "))
    print()

    comunicacao = int(input("""
0 = Afetado
1 = Operando
Digite o status de comunicação: """))
    print()

    modulo = int(input("""
0 = Módulo com falha
1 = Módulo operando normalmente
Digite o status dos módulos de operação: """))
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

    print("CARREGANDO BASE ÚNICA ESCOLHIDA")
    print("Base: Amateur Satellite Database / SatNOGS")
    print("Fonte: GitHub")
    print()

    try:
        dados = pd.read_csv(URL_BASE, engine="python", on_bad_lines="skip")

        print("Base carregada diretamente do GitHub.")
        print()

        colunas_necessarias = ["launched", "status", "norad_cat_id", "countries", "name"]

        for coluna in colunas_necessarias:
            if coluna not in dados.columns:
                print(f"Erro: a coluna '{coluna}' não foi encontrada na base.")
                return

        dados["launched"] = pd.to_datetime(dados["launched"], errors="coerce", utc=True)
        dados["ano_lancamento"] = dados["launched"].dt.year

        data_atual = pd.Timestamp.now(tz="UTC")
        dados["dias_em_orbita"] = (data_atual - dados["launched"]).dt.days

        dados["norad_cat_id"] = pd.to_numeric(dados["norad_cat_id"], errors="coerce")

        dados = dados.dropna(subset=["ano_lancamento", "dias_em_orbita", "status"])
        dados = dados[dados["dias_em_orbita"] > 0]

        dados["ano_lancamento"] = dados["ano_lancamento"].astype(int)
        dados["dias_em_orbita"] = dados["dias_em_orbita"].astype(int)

        dados.to_csv("base_satelites_github.csv", index=False)

        print("Base preparada com sucesso!")
        print(f"Quantidade de linhas: {dados.shape[0]}")
        print(f"Quantidade de colunas: {dados.shape[1]}")
        print()
        print("Arquivo salvo para entrega como:")
        print("base_satelites_github.csv")
        print()

        print("Colunas principais utilizadas:")
        print("- ano_lancamento: ano em que o satélite foi lançado")
        print("- dias_em_orbita: quantidade aproximada de dias desde o lançamento")
        print("- status: situação atual do satélite")
        print("- countries: país relacionado ao satélite")
        print("- norad_cat_id: identificador NORAD")
        print()

    except Exception as erro:
        print("Erro ao carregar a base de dados.")
        print("Verifique sua conexão com a internet.")
        print(f"Detalhes do erro: {erro}")


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
    global tabela_discreta

    if not verificar_base():
        return

    print("TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIAS")
    print("Variável quantitativa discreta: ano_lancamento")
    print()

    frequencia = dados["ano_lancamento"].value_counts().sort_index()
    frequencia_relativa = frequencia / frequencia.sum()
    percentual = frequencia_relativa * 100

    tabela_discreta = pd.DataFrame({
        "Ano de Lançamento": frequencia.index,
        "Frequência Absoluta": frequencia.values,
        "Frequência Relativa": frequencia_relativa.values,
        "Percentual (%)": percentual.values
    })

    print(tabela_discreta.head(20))
    print()
    print("Observação: foram exibidas as 20 primeiras linhas da tabela.")
    print()

    mostrar_tabela_como_imagem(tabela_discreta, "Tabela de Frequência - Ano de Lançamento")

    tabela_discreta.to_csv("tabela_frequencia_discreta_ano_lancamento.csv", index=False)
    print("Tabela salva como: tabela_frequencia_discreta_ano_lancamento.csv")


def montar_tabela_frequencia_continua():
    global tabela_continua

    if not verificar_base():
        return

    print("TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIAS")
    print("Variável quantitativa contínua: dias_em_orbita")
    print()

    valores = dados["dias_em_orbita"].dropna()

    quantidade_classes = int(np.sqrt(len(valores)))

    if quantidade_classes > 15:
        quantidade_classes = 15

    tabela = pd.cut(valores, bins=quantidade_classes).value_counts().sort_index()

    frequencia_relativa = tabela / tabela.sum()
    percentual = frequencia_relativa * 100

    tabela_continua = pd.DataFrame({
        "Intervalo de Dias em Órbita": tabela.index.astype(str),
        "Frequência Absoluta": tabela.values,
        "Frequência Relativa": frequencia_relativa.values,
        "Percentual (%)": percentual.values
    })

    print(tabela_continua)
    print()

    mostrar_tabela_como_imagem(tabela_continua, "Tabela de Frequência - Dias em Órbita")

    tabela_continua.to_csv("tabela_frequencia_continua_dias_orbita.csv", index=False)
    print("Tabela salva como: tabela_frequencia_continua_dias_orbita.csv")


def gerar_graficos():
    global graficos_gerados

    if not verificar_base():
        return

    print("GERAÇÃO DE GRÁFICOS ESTATÍSTICOS")
    print("Serão gerados dois gráficos usando a base de satélites do GitHub.")
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
    plt.hist(dados["dias_em_orbita"], bins=20, color="lightgreen", edgecolor="black")
    plt.title("Distribuição dos Dias em Órbita")
    plt.xlabel("Dias em órbita")
    plt.ylabel("Frequência")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("grafico_2_dias_em_orbita.png")
    plt.show()
    plt.close()

    graficos_gerados = [
        "grafico_1_status_satelites.png",
        "grafico_2_dias_em_orbita.png"
    ]

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
    global analises_estatisticas

    if not verificar_base():
        return

    print("ANÁLISE UNIVARIADA COM ESTATÍSTICA DESCRITIVA")
    print("Variáveis analisadas: ano_lancamento e dias_em_orbita")
    print()

    analises_estatisticas["ano_lancamento"] = calcular_medidas("ano_lancamento")
    analises_estatisticas["dias_em_orbita"] = calcular_medidas("dias_em_orbita")

    resultado = []

    for variavel, medidas in analises_estatisticas.items():
        linha = {"Variável": variavel}
        linha.update(medidas)
        resultado.append(linha)

    tabela_resultado = pd.DataFrame(resultado)

    print(tabela_resultado)
    print()

    mostrar_tabela_como_imagem(tabela_resultado, "Análise Univariada - Estatística Descritiva")

    tabela_resultado.to_csv("analise_univariada_satelites.csv", index=False)
    print("Análise salva como: analise_univariada_satelites.csv")


def interpretar_variavel(nome_variavel, medidas):
    texto = ""

    if nome_variavel == "ano_lancamento":
        nome = "ano de lançamento dos satélites"
    elif nome_variavel == "dias_em_orbita":
        nome = "quantidade de dias em órbita"
    else:
        nome = nome_variavel

    texto += f"A variável {nome} apresentou média de {medidas['Média']:.2f}, "
    texto += f"mediana de {medidas['Mediana']:.2f} e moda de {medidas['Moda']}. "

    texto += f"Os valores variaram entre {medidas['Mínimo']:.2f} e {medidas['Máximo']:.2f}, "
    texto += f"com amplitude de {medidas['Amplitude']:.2f}. "

    texto += f"A variância foi de {medidas['Variância']:.2f} e o desvio padrão foi de {medidas['Desvio Padrão']:.2f}. "

    if medidas["Coeficiente de Variação (%)"] < 15:
        texto += "O coeficiente de variação indica baixa dispersão dos dados. "
    elif medidas["Coeficiente de Variação (%)"] < 30:
        texto += "O coeficiente de variação indica dispersão moderada dos dados. "
    else:
        texto += "O coeficiente de variação indica alta dispersão dos dados. "

    texto += f"Os quartis foram Q1 = {medidas['1º Quartil']:.2f}, "
    texto += f"Q2 = {medidas['2º Quartil']:.2f} e Q3 = {medidas['3º Quartil']:.2f}. "

    return texto


def quebrar_texto(texto, largura=95):
    linhas = []

    for paragrafo in texto.split("\n"):
        if paragrafo.strip() == "":
            linhas.append("")
        else:
            linhas.extend(textwrap.wrap(paragrafo, width=largura))

    return "\n".join(linhas)


def adicionar_texto_pdf(pdf, titulo, texto):
    plt.figure(figsize=(8.27, 11.69))
    plt.axis("off")

    texto_formatado = quebrar_texto(texto, largura=90)

    plt.text(
        0.5,
        0.92,
        titulo,
        fontsize=18,
        ha="center",
        va="top",
        weight="bold"
    )

    plt.plot([0.15, 0.85], [0.89, 0.89], linewidth=1)

    plt.text(
        0.5,
        0.83,
        texto_formatado,
        fontsize=11,
        ha="center",
        va="top",
        linespacing=1.6
    )

    pdf.savefig(bbox_inches="tight")
    plt.close()


def preparar_tabela_para_pdf(tabela):
    tabela_formatada = tabela.copy()

    for coluna in tabela_formatada.columns:
        tabela_formatada[coluna] = tabela_formatada[coluna].apply(
            lambda valor: f"{valor:.2f}" if isinstance(valor, (int, float, np.integer, np.floating)) else str(valor)
        )

    return tabela_formatada


def adicionar_tabela_pdf(pdf, titulo, tabela):
    plt.figure(figsize=(11.69, 8.27))
    plt.axis("off")

    tabela_exibida = tabela.copy()

    if len(tabela_exibida) > 12:
        tabela_exibida = tabela_exibida.head(12)

    tabela_exibida = preparar_tabela_para_pdf(tabela_exibida)

    plt.text(
        0.5,
        0.93,
        titulo,
        fontsize=17,
        ha="center",
        va="center",
        weight="bold"
    )

    plt.plot([0.12, 0.88], [0.89, 0.89], linewidth=1)

    tabela_plot = plt.table(
        cellText=tabela_exibida.values,
        colLabels=tabela_exibida.columns,
        loc="center",
        cellLoc="center",
        colLoc="center"
    )

    tabela_plot.auto_set_font_size(False)
    tabela_plot.set_fontsize(8)
    tabela_plot.scale(1.1, 1.6)

    for (linha, coluna), celula in tabela_plot.get_celld().items():
        celula.set_edgecolor("black")

        if linha == 0:
            celula.set_text_props(weight="bold")
            celula.set_height(0.08)
        else:
            celula.set_height(0.06)

    pdf.savefig(bbox_inches="tight")
    plt.close()


def adicionar_imagem_pdf(pdf, titulo, caminho_imagem):
    if not os.path.exists(caminho_imagem):
        return

    imagem = plt.imread(caminho_imagem)

    plt.figure(figsize=(11.69, 8.27))
    plt.axis("off")

    plt.text(
        0.5,
        0.95,
        titulo,
        fontsize=17,
        ha="center",
        va="center",
        weight="bold"
    )

    plt.plot([0.12, 0.88], [0.91, 0.91], linewidth=1)

    plt.imshow(imagem, extent=[0.08, 0.92, 0.08, 0.86], aspect="auto")

    pdf.savefig(bbox_inches="tight")
    plt.close()


def gerar_relatorio_pdf():
    if not verificar_base():
        return

    if tabela_discreta is None:
        print("A tabela de frequência discreta ainda não foi gerada.")
        print("Use a opção 6 antes de gerar o relatório.")
        return

    if tabela_continua is None:
        print("A tabela de frequência contínua ainda não foi gerada.")
        print("Use a opção 7 antes de gerar o relatório.")
        return

    if len(graficos_gerados) == 0:
        print("Os gráficos ainda não foram gerados.")
        print("Use a opção 8 antes de gerar o relatório.")
        return

    if len(analises_estatisticas) == 0:
        print("A análise univariada ainda não foi realizada.")
        print("Use a opção 9 antes de gerar o relatório.")
        return

    nome_pdf = "relatorio_estatistico_global_solution.pdf"

    with PdfPages(nome_pdf) as pdf:
        plt.figure(figsize=(8.27, 11.69))
        plt.axis("off")

        plt.text(
            0.5,
            0.78,
            "GLOBAL SOLUTION",
            fontsize=26,
            ha="center",
            va="center",
            weight="bold"
        )

        plt.text(
            0.5,
            0.72,
            "1º SEMESTRE",
            fontsize=18,
            ha="center",
            va="center"
        )

        plt.plot([0.2, 0.8], [0.68, 0.68], linewidth=1.5)

        plt.text(
            0.5,
            0.58,
            "Sistema Inteligente de Monitoramento\npara Missão Espacial Experimental",
            fontsize=16,
            ha="center",
            va="center",
            linespacing=1.5
        )

        plt.text(
            0.5,
            0.43,
            "Base de dados utilizada:\nAmateur Satellite Database / SatNOGS",
            fontsize=13,
            ha="center",
            va="center",
            linespacing=1.5
        )

        plt.text(
            0.5,
            0.32,
            "Relatório Estatístico",
            fontsize=15,
            ha="center",
            va="center",
            weight="bold"
        )

        plt.text(
            0.5,
            0.18,
            "Fonte: GitHub",
            fontsize=11,
            ha="center",
            va="center"
        )

        pdf.savefig(bbox_inches="tight")
        plt.close()

        texto_introducao = (
            "Este relatório apresenta uma análise estatística baseada na base Amateur Satellite Database / SatNOGS, "
            "disponibilizada em formato CSV por meio do GitHub. A base contém informações reais sobre satélites, "
            "incluindo nome, status, país, identificador NORAD e data de lançamento.\n\n"
            "A escolha dessa base se relaciona diretamente ao tema da Global Solution, pois utiliza dados reais ligados "
            "ao contexto espacial. A análise permite transformar dados brutos em informações úteis para sistemas "
            "inteligentes de monitoramento, tomada de decisão e identificação de padrões operacionais."
        )

        adicionar_texto_pdf(pdf, "Introdução", texto_introducao)

        texto_objetivo = (
            "O objetivo deste relatório é organizar, visualizar e interpretar dados relacionados a satélites por meio "
            "de tabelas de distribuição de frequências, gráficos estatísticos e medidas de estatística descritiva.\n\n"
            "Com isso, busca-se demonstrar como a análise de dados pode apoiar decisões em uma missão espacial experimental, "
            "contribuindo para a identificação de variações, padrões e possíveis pontos de atenção."
        )

        adicionar_texto_pdf(pdf, "Objetivo da Análise", texto_objetivo)

        adicionar_tabela_pdf(pdf, "Tabela de Frequência - Ano de Lançamento", tabela_discreta)
        adicionar_tabela_pdf(pdf, "Tabela de Frequência - Dias em Órbita", tabela_continua)

        adicionar_imagem_pdf(pdf, "Gráfico 1 - Status dos Satélites", "grafico_1_status_satelites.png")
        adicionar_imagem_pdf(pdf, "Gráfico 2 - Distribuição dos Dias em Órbita", "grafico_2_dias_em_orbita.png")

        tabela_analise = pd.DataFrame(analises_estatisticas).T.reset_index()
        tabela_analise = tabela_analise.rename(columns={"index": "Variável"})

        adicionar_tabela_pdf(pdf, "Análise Univariada", tabela_analise)

        texto_interpretacao = ""

        for variavel, medidas in analises_estatisticas.items():
            texto_interpretacao += interpretar_variavel(variavel, medidas)
            texto_interpretacao += "\n\n"

        texto_interpretacao += (
            "A análise do ano de lançamento permite observar a distribuição temporal dos satélites registrados, "
            "possibilitando identificar períodos com maior concentração de lançamentos. Já a variável dias em órbita "
            "ajuda a compreender há quanto tempo os satélites permanecem registrados desde seu lançamento.\n\n"
            "No contexto de uma missão espacial experimental, esses resultados auxiliam na organização das informações, "
            "na leitura de padrões, na avaliação de status operacionais e no apoio à tomada de decisão técnica."
        )

        adicionar_texto_pdf(pdf, "Interpretação dos Resultados", texto_interpretacao)

        texto_conclusao = (
            "A utilização da base Amateur Satellite Database / SatNOGS permitiu aplicar conceitos de estatística descritiva, "
            "distribuição de frequências e visualização gráfica em um contexto real da área espacial.\n\n"
            "Os resultados demonstram que a análise de dados pode transformar informações brutas em inteligência acionável. "
            "Dessa forma, o sistema desenvolvido contribui para o objetivo da Global Solution ao simular uma plataforma "
            "de monitoramento e análise voltada à tomada de decisão em missões espaciais experimentais."
        )

        adicionar_texto_pdf(pdf, "Conclusão", texto_conclusao)

    print()
    print(f"Relatório PDF gerado com sucesso: {nome_pdf}")
    print()


while True:
    print()
    print("""MENU DO SISTEMA DA NAVE

1 - Inserir dados simulados da missão
2 - Visualizar status atual
3 - Executar análise automática da missão
4 - Histórico das leituras
5 - Carregar base única de satélites do GitHub
6 - Gerar tabela de frequência discreta
7 - Gerar tabela de frequência contínua
8 - Gerar gráficos estatísticos
9 - Realizar análise univariada
10 - Gerar relatório estatístico em PDF
11 - Encerrar sistema""")
    print()

    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Digite apenas números.")
        continue

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
        gerar_relatorio_pdf()

    elif opcao == 11:
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida. Tente novamente.")