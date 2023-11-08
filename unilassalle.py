import pandas as pd
import sqlite3
import plotly.express as px
import webbrowser
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Nome do arquivo do banco de dados SQLite
db_file = 'C://Users//claud//OneDrive//Claudio Bonel-DADOTECA//_ProfessorClaudioBonel//SENAC//Provas práticas//Python//BD//ocorrencias.db'

try:
    # Tenta criar uma conexão com o banco de dados
    conn = sqlite3.connect(db_file)
    
    # Consulta SQL para calcular o somatório da quantidade de registros de ocorrência por delegacia
    # e ranqueá-las da maior para a menor quantidade de registros
    query = """
    SELECT tbDP.nome AS Delegacia, SUM(tbOcorrencias.qtde) AS TotalOcorrencias
    FROM tbOcorrencias
    JOIN tbDP ON tbOcorrencias.codDP = tbDP.codDP
    JOIN tbMunicipio ON tbOcorrencias.codIBGE = tbMunicipio.codIBGE
    WHERE tbMunicipio.regiao = 'Capital'
    GROUP BY tbDP.nome
    ORDER BY TotalOcorrencias DESC
    """
    
    # Query para obter a evolução da quantidade de recuperação de veículos e roubo de veículos ao longo dos anos
    query_evolucao = """
    SELECT ano,
    SUM(CASE WHEN ocorrencias = 'recuperacao_veiculos' THEN qtde ELSE 0 END) AS RecuperacaoVeiculos,
    SUM(CASE WHEN ocorrencias = 'roubo_veiculo' THEN qtde ELSE 0 END) AS RouboVeiculos
    FROM tbOcorrencias
    GROUP BY ano
    ORDER BY ano
    """
    
    # Executa a consulta SQL e armazena o resultado em um DataFrame
    df = pd.read_sql_query(query, conn)
    
    # Ordena o DataFrame da maior para a menor quantidade de registros de ocorrências
    df = df.sort_values(by='TotalOcorrencias', ascending=True)

    # Executa a consulta SQL e armazena o resultado em um DataFrame
    df_evolucao = pd.read_sql_query(query_evolucao, conn)
    
    # Fecha a conexão com o banco de dados
    conn.close()
    
    # Cria o gráfico de barras horizontais usando plotly
    fig1 = px.bar(df, x='TotalOcorrencias', y='Delegacia', orientation='h', title='Ranqueamento de Delegacias por Ocorrências')
    fig1.update_xaxes(title_text='Total de Ocorrências')
    fig1.update_yaxes(title_text='Delegacia')
    
    # Cria um gráfico de linhas usando plotly
    fig2 = px.line(df_evolucao, x='ano', y=['RecuperacaoVeiculos', 'RouboVeiculos'], title='Evolução de Recuperação vs. Roubo de Veículos ao Longo dos Anos')
    fig2.update_xaxes(title_text='Ano')
    fig2.update_yaxes(title_text='Quantidade')
    
    # Cria um subplot com os dois gráficos
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Ranqueamento de Delegacias por Ocorrências', 'Evolução de Recuperação vs. Roubo de Veículos ao Longo dos Anos'))
    
    # Adiciona os gráficos ao subplot
    fig.add_trace(fig1['data'][0], row=1, col=1)
    fig.add_trace(fig2['data'][0], row=2, col=1)
    
    # Atualiza o layout do subplot
    fig.update_layout(height=800, width=1000, title_text='Relatório de Ocorrências')
    
    # Gera o arquivo HTML com os gráficos
    fig.write_html('relatorio_ocorrencias.html')
    
    # Abre automaticamente o arquivo HTML no navegador padrão
    webbrowser.open('relatorio_ocorrencias.html')
    
except sqlite3.Error as e:
    # Trata exceções relacionadas ao SQLite
    print("Erro ao conectar-se ao banco de dados:", e)
