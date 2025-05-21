## Sobre o Aplicativo Análise de Turnover

O **Análise de Turnover** é uma aplicação web interativa desenvolvida para auxiliar gestores, profissionais de Recursos Humanos e analistas de People Analytics na análise de rotatividade (turnover) de funcionários em empresas. Construído com [Streamlit](https://streamlit.io/), um framework Python para criação de dashboards, o aplicativo combina a potência de bibliotecas como Pandas para manipulação de dados e Plotly para visualizações interativas, oferecendo uma experiência intuitiva e eficiente.

### Objetivo

O principal objetivo do **Análise de Turnover** é fornecer uma ferramenta prática para monitorar e analisar métricas de rotatividade de forma detalhada e visual. Com ele, é possível identificar padrões de turnover por loja, setor, cargo e motivos de contratação/desligamento, permitindo que as empresas tomem decisões mais informadas para melhorar a retenção de talentos e otimizar processos de gestão de pessoas.

### Público-Alvo

Este aplicativo é ideal para:
- **Gestores de RH**: Que desejam monitorar a rotatividade e identificar áreas críticas para intervenção.
- **Analistas de People Analytics**: Que buscam insights baseados em dados para estratégias de retenção.
- **Líderes de Negócios**: Que precisam de uma visão clara do impacto do turnover em diferentes unidades ou setores da empresa.

### Funcionalidades Principais

O **Análise de Turnover** oferece uma série de funcionalidades para facilitar a análise de dados de rotatividade:

- **Autenticação Segura**: O acesso ao dashboard é protegido por uma tela de login que exige um e-mail válido. Cada acesso é registrado e notificado ao administrador via e-mail, garantindo controle e rastreabilidade.
  
- **Upload de Arquivos Excel**: O usuário pode carregar um arquivo Excel com dados de turnover, contendo informações como loja, datas de admissão e demissão, motivos de contratação/desligamento, setor e função.

- **Filtros Interativos**:
  - **Período de Análise**: Selecione o intervalo de datas (início e fim) para analisar os dados.
  - **Lojas**: Escolha uma ou mais lojas específicas para focar a análise, ou analise todas as lojas de uma vez.

- **Métricas de Alto Nível**:
  - Quantidade de **admitidos** no período.
  - Quantidade de **desligados** no período.
  - Número de **colaboradores ativos**.
  - **Taxa de Turnover (%)**, calculada com base nos dados do período selecionado.

- **Visualizações Detalhadas**:
  - **% Turnover por Loja**: Um gráfico de barras verticais exibe a taxa de turnover por loja, com rolagem horizontal para navegar entre as lojas (mostra 10 lojas por vez). O usuário pode arrastar o gráfico para visualizar todas as lojas.
  - **Motivos de Desligamento**: Um gráfico de barras horizontais mostra os 5 principais motivos de desligamento, com porcentagens.
  - **Motivos de Contratação**: Similar ao anterior, exibe os 5 principais motivos de contratação.
  - **Setores com Mais Desligamentos**: Um gráfico de barras destaca os 5 setores com maior número de desligamentos.
  - **Cargos Mais Desligados**: Outro gráfico de barras mostra os 5 cargos com mais desligamentos.

- **Notificações por E-mail**: Cada acesso ao aplicativo é registrado, e uma notificação é enviada ao administrador com o e-mail do usuário e a data/hora do acesso.

### Benefícios

- **Facilidade de Uso**: Interface amigável e intuitiva, projetada para usuários sem conhecimento técnico avançado.
- **Análise Rápida**: Visualize métricas e padrões de turnover em poucos cliques.
- **Flexibilidade**: Filtros permitem personalizar a análise conforme as necessidades do usuário.
- **Tomada de Decisão Baseada em Dados**: Identifique áreas problemáticas (ex.: lojas com alto turnover, setores com muitos desligamentos) e aja de forma estratégica.

### Como Funciona

1. **Acesso ao Dashboard**:
   - O usuário insere um e-mail válido na tela de login.
   - O sistema registra o acesso e envia uma notificação ao administrador.

2. **Upload de Dados**:
   - O usuário carrega um arquivo Excel com os dados de turnover, que devem incluir colunas específicas (ex.: `Loja`, `Data de Admissão`, `Data de Demissão`, etc.).

3. **Análise e Visualização**:
   - Use os filtros na barra lateral para selecionar o período e as lojas de interesse.
   - Explore as métricas principais (admitidos, desligados, colaboradores, % turnover).
   - Navegue pelos gráficos interativos para obter insights detalhados.

4. **Saída**:
   - Clique no botão "Sair" para retornar à tela de login.

O **Análise de Turnover** é uma ferramenta poderosa para transformar dados brutos em insights acionáveis, ajudando empresas a gerirem melhor seus talentos e reduzirem a rotatividade de forma estratégica.

# 🌐 Acesso ao Aplicativo

O app está disponível online e pode ser acessado diretamente:

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://data-turnover.streamlit.app/)

🔗 [https://data-turnover.streamlit.app/](https://data-turnover.streamlit.app/)

## 📊 Arquivo de Exemplo

Baixe o modelo pronto para uso:  
[Exemplo.xlsx](./Exemplo.xlsx)

## 👨💻 Autor
**Fábio Dias**  
[<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20"> LinkedIn](https://www.linkedin.com/in/fabio-data-science)  
[<img src="https://cdn-icons-png.flaticon.com/512/281/281769.png" width="20"> Email](mailto:fabiodias.elesbao@gmail.com)
