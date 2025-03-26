import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import re
import smtplib
from email.mime.text import MIMEText

# Configuração inicial do Streamlit
st.set_page_config(page_title="Análise de Turnover", layout="wide")

# Função para validar e-mail (copiada do app 9box)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Função para enviar e-mail com os dados no corpo (ajustada com suas credenciais)


def send_email(user_email):
    sender_email = st.secrets["email"]["sender_email"]
    sender_password = st.secrets["email"]["sender_password"]
    receiver_email = "aquelequeuiva@gmail.com"

    msg = MIMEText(
        f"Novo acesso ao aplicativo:\nE-mail: {user_email}\nData/Hora: {pd.Timestamp.now()}")
    msg['Subject'] = "Novo acesso ao aplicativo de Turnover"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        st.success("E-mail enviado com sucesso ao administrador!")
    except Exception as e:
        st.error(f"Falha ao enviar e-mail: {e}")


# Inicializar o estado da sessão para controle de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "email" not in st.session_state:
    st.session_state.email = ""

# Tela de autenticação
if not st.session_state.authenticated:
    st.title("Análise de Turnover")
    st.write("Por favor, insira um e-mail válido para acessar o dashboard gratuito.")

    # Usar colunas para alinhar o campo de entrada à esquerda
    col1, col2 = st.columns([2, 3])
    with col1:
        email_input = st.text_input(
            "E-mail", value=st.session_state.email, key="email_input")

    if st.button("Acessar"):
        if email_input:
            if is_valid_email(email_input):
                st.session_state.email = email_input
                # Enviar e-mail para controle de acesso
                send_email(email_input)
                st.session_state.authenticated = True
                st.success(
                    "Acesso liberado! Redirecionando para o dashboard...")
                st.rerun()
            else:
                st.error(
                    "Por favor, insira um e-mail válido (exemplo: usuario@dominio.com).")
        else:
            st.error("O campo de e-mail não pode estar vazio.")
else:
    # Estilo CSS para personalizar o layout e visual
    st.markdown(
        """
        <style>
        .metric-box {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            background-color: #f9f9f9;
            height: 120px;
            width: 240px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .metric-box h3 {
            font-size: 36px;
            color: #000000;
            margin: 0;
        }
        .metric-box p {
            font-size: 16px;
            color: #000000;
            margin: 0;
        }
        .stApp {
            background-color: #f0f0f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Título do dashboard
    st.title("Análise de Turnover")

    # Upload do arquivo Excel
    st.subheader("Carregar Arquivo de Dados (Excel)")
    uploaded_file = st.file_uploader(
        "Selecione um arquivo Excel com os dados de turnover", type=["xlsx", "xls"])

    # Verificar se o arquivo foi carregado
    if uploaded_file is not None:
        try:
            # Carregar o arquivo Excel usando pandas
            df = pd.read_excel(uploaded_file)

            # Verificar se as colunas necessárias estão presentes
            required_columns = ["Loja", "Data de Admissão", "Data de Demissão", "Motivo do Desligamento",
                                "Motivo da Contratação", "Setor", "Função"]
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(
                    f"O arquivo Excel deve conter as seguintes colunas: {', '.join(missing_columns)}")
            else:
                # Processar os dados
                df["Motivo da Contratação"] = df["Motivo da Contratação"].replace(
                    {"Subistituição": "Substituição"})
                df["Data de Admissão"] = pd.to_datetime(
                    df["Data de Admissão"], dayfirst=True, errors="coerce")
                df["Data de Demissão"] = pd.to_datetime(
                    df["Data de Demissão"], dayfirst=True, errors="coerce")

                # Função para calcular Turnover e outras métricas
                def calculate_turnover(df, start_date, end_date, selected_lojas):
                    df_filtered = df[df["Data de Admissão"].notna()]

                    if selected_lojas and selected_lojas != ["Todas"]:
                        df_filtered = df_filtered[df_filtered["Loja"].isin(
                            selected_lojas)]

                    df_admissions_until_end = df_filtered[
                        (df_filtered["Data de Admissão"].dt.to_period(
                            'M') <= end_date.to_period('M'))
                    ]
                    total_admissions = df_admissions_until_end.shape[0]

                    df_exits_until_end = df_filtered[
                        (df_filtered["Data de Demissão"].notna()) &
                        (df_filtered["Data de Demissão"].dt.to_period(
                            'M') <= end_date.to_period('M'))
                    ]
                    total_exits = df_exits_until_end.shape[0]

                    collaborators = total_admissions - total_exits

                    df_admissions_period = df_filtered[
                        (df_filtered["Data de Admissão"].dt.to_period('M').between(
                            start_date.to_period('M'), end_date.to_period('M')))
                    ]
                    admissions = df_admissions_period.shape[0]

                    df_exits_period = df_filtered[
                        (df_filtered["Data de Demissão"].notna()) &
                        (df_filtered["Data de Demissão"].dt.to_period('M').between(
                            start_date.to_period('M'), end_date.to_period('M')))
                    ]
                    exits = df_exits_period.shape[0]

                    total_for_turnover = collaborators + exits
                    turnover_rate = (exits / total_for_turnover) * \
                        100 if total_for_turnover > 0 else 0

                    return turnover_rate, exits, admissions, collaborators, df_filtered

                # Função para obter datas disponíveis
                def get_available_dates(df):
                    dates_admission = df["Data de Admissão"].dropna(
                    ).dt.to_period('M').unique()
                    dates_dismissal = df["Data de Demissão"].dropna(
                    ).dt.to_period('M').unique()
                    all_dates = pd.concat(
                        [pd.Series(dates_admission), pd.Series(dates_dismissal)]).dropna().unique()
                    all_dates = sorted(all_dates)
                    return [d.strftime('%m/%Y') for d in all_dates]

                # Função para obter lojas disponíveis
                def get_available_lojas(df):
                    return ["Todas"] + sorted(df["Loja"].dropna().unique().tolist())

                # Sidebar para filtros
                st.sidebar.header("FILTROS")
                available_dates = get_available_dates(df)
                default_start_date = available_dates[0] if available_dates else datetime(
                    2010, 1, 1).strftime('%m/%Y')
                default_end_date = available_dates[-1] if available_dates else datetime(
                    2018, 12, 31).strftime('%m/%Y')
                start_date = st.sidebar.selectbox(
                    "Data Início", options=available_dates, index=0, key="start_date")
                end_date = st.sidebar.selectbox("Data Fim", options=available_dates, index=len(
                    available_dates)-1, key="end_date")
                selected_lojas = st.sidebar.multiselect(
                    "Loja", options=get_available_lojas(df), default=["Todas"], key="lojas")

                # Converter datas de string (MM/YYYY) para datetime
                start_date_dt = pd.to_datetime(
                    start_date + '-01', format='%m/%Y-%d')
                end_date_dt = pd.to_datetime(
                    end_date + '-01', format='%m/%Y-%d') + pd.offsets.MonthEnd(0)

                # Calcular métricas com os dados carregados
                turnover_rate, exits, admissions, collaborators, df_filtered = calculate_turnover(
                    df, start_date_dt, end_date_dt, selected_lojas)

                # Layout superior: Qtde Admitidos, Qtde Desligados, Qtde Colaboradores e % Turnover
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <h3>{admissions}</h3>
                            <p>QTDE ADMITIDOS</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <h3>{exits}</h3>
                            <p>QTDE DESLIGADOS</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with col3:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <h3>{collaborators}</h3>
                            <p>QTDE COLABORADORES</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with col4:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <h3>{turnover_rate:.1f}%</h3>
                            <p>% TURNOVER</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Fator de escala para reduzir a altura das barras
                scale_factor = 0.5

                # Gráfico de barras verticais: Turnover por Loja (com rolagem horizontal para 10 lojas visíveis por vez)
                st.subheader("% Turnover por Loja")
                df_turnover_by_store = df_filtered[
                    (df_filtered["Data de Demissão"].notna()) &
                    (df_filtered["Data de Demissão"].dt.to_period('M').between(
                        start_date_dt.to_period('M'), end_date_dt.to_period('M')))
                ]

                df_admissions_by_store = df_filtered[
                    (df_filtered["Data de Admissão"].dt.to_period(
                        'M') <= end_date_dt.to_period('M'))
                ].groupby("Loja").size().reset_index(name="Total Admitidos")

                df_exits_by_store_until_end = df_filtered[
                    (df_filtered["Data de Demissão"].notna()) &
                    (df_filtered["Data de Demissão"].dt.to_period(
                        'M') <= end_date_dt.to_period('M'))
                ].groupby("Loja").size().reset_index(name="Total Desligados")

                df_collaborators_by_store = pd.merge(
                    df_admissions_by_store, df_exits_by_store_until_end, on="Loja", how="left").fillna(0)
                df_collaborators_by_store["Colaboradores"] = df_collaborators_by_store["Total Admitidos"] - \
                    df_collaborators_by_store["Total Desligados"]

                df_exits_by_store = df_turnover_by_store.groupby(
                    "Loja").size().reset_index(name="Desligados")

                df_turnover_by_store = pd.merge(
                    df_collaborators_by_store, df_exits_by_store, on="Loja", how="left").fillna(0)
                df_turnover_by_store["Turnover"] = (df_turnover_by_store["Desligados"] / (
                    df_turnover_by_store["Colaboradores"] + df_turnover_by_store["Desligados"])) * 100
                df_turnover_by_store["Turnover"] = df_turnover_by_store["Turnover"].fillna(
                    0)

                # Ordenar as lojas por turnover (para melhor visualização)
                df_turnover_by_store = df_turnover_by_store.sort_values(
                    "Turnover", ascending=False)

                df_turnover_by_store["Loja Abreviada"] = df_turnover_by_store["Loja"].str[:7]

                df_turnover_by_store["Turnover_Scaled"] = df_turnover_by_store["Turnover"] * scale_factor

                # Criar o gráfico
                fig_turnover_by_store = px.bar(
                    df_turnover_by_store,
                    x="Loja Abreviada",
                    y="Turnover_Scaled",
                    title="",
                    text=df_turnover_by_store["Turnover"].round(
                        1).astype(str) + "%"
                )
                fig_turnover_by_store.update_traces(
                    marker_color="#FF0000",
                    marker_line_color="black",
                    marker_line_width=1,
                    width=0.5,  # Largura relativa das barras
                    textposition="outside",
                    textfont=dict(color="black")
                )
                fig_turnover_by_store.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=20, b=40),
                    xaxis=dict(
                        title="",
                        tickfont=dict(color="black"),
                        fixedrange=False,  # Permitir rolagem no eixo X
                        # Mostrar 10 lojas por vez (índices de 0 a 9)
                        range=[-0.5, 9.5],
                    ),
                    yaxis=dict(
                        title="",
                        tickfont=dict(color="black"),
                        fixedrange=True,  # Impedir zoom/rolagem no eixo Y
                    ),
                    xaxis_tickangle=45,
                    plot_bgcolor="white",
                    showlegend=False,
                    dragmode="pan",  # Permitir arrastar para rolar
                )
                # Exibir o gráfico com a largura original do contêiner
                st.plotly_chart(fig_turnover_by_store, use_container_width=True, config={
                                "scrollZoom": True})

                # Seção intermediária: Motivos de Desligamento e Contratação
                scale_factor_motivos = 0.3

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Motivo de Desligamento")
                    df_desligamentos_period = df_filtered[
                        (df_filtered["Data de Demissão"].notna()) &
                        (df_filtered["Data de Demissão"].dt.to_period('M').between(
                            start_date_dt.to_period('M'), end_date_dt.to_period('M')))
                    ]

                    top_desligamentos = df_desligamentos_period["Motivo do Desligamento"].value_counts(
                    ).nlargest(5)
                    total_desligamentos = top_desligamentos.sum()
                    top_desligamentos_df = top_desligamentos.reset_index()
                    top_desligamentos_df.columns = [
                        "Motivo do Desligamento", "Contagem"]
                    top_desligamentos_df["Porcentagem"] = (
                        top_desligamentos_df["Contagem"] / total_desligamentos * 100).round(1).astype(str) + "%"

                    top_desligamentos_df["Contagem_Scaled"] = top_desligamentos_df["Contagem"] * \
                        scale_factor_motivos

                    fig_desligamentos = px.bar(
                        top_desligamentos_df,
                        y="Motivo do Desligamento",
                        x="Contagem_Scaled",
                        orientation="h",
                        title="",
                        text="Porcentagem"
                    )
                    fig_desligamentos.update_traces(
                        marker_color="#FF0000",
                        marker_line_color="black",
                        marker_line_width=1,
                        width=0.5,
                        textposition="inside",
                        textfont=dict(color="black")
                    )
                    fig_desligamentos.update_layout(
                        height=300,
                        margin=dict(l=20, r=50, t=20, b=20),
                        xaxis_title="",
                        yaxis_title="",
                        yaxis=dict(
                            tickfont=dict(color="black")
                        ),
                        bargap=0.4
                    )
                    st.plotly_chart(fig_desligamentos,
                                    use_container_width=True)

                with col2:
                    st.subheader("Motivo de Contratação")
                    df_contratacoes_period = df_filtered[
                        (df_filtered["Data de Admissão"].dt.to_period('M').between(
                            start_date_dt.to_period('M'), end_date_dt.to_period('M')))
                    ]

                    top_contratacoes = df_contratacoes_period["Motivo da Contratação"].value_counts(
                    ).nlargest(5)
                    total_contratacoes = top_contratacoes.sum()
                    top_contratacoes_df = top_contratacoes.reset_index()
                    top_contratacoes_df.columns = [
                        "Motivo da Contratação", "Contagem"]
                    top_contratacoes_df["Porcentagem"] = (
                        top_contratacoes_df["Contagem"] / total_contratacoes * 100).round(1).astype(str) + "%"

                    top_contratacoes_df["Contagem_Scaled"] = top_contratacoes_df["Contagem"] * \
                        scale_factor_motivos

                    fig_contratacoes = px.bar(
                        top_contratacoes_df,
                        y="Motivo da Contratação",
                        x="Contagem_Scaled",
                        orientation="h",
                        title="",
                        text="Porcentagem"
                    )
                    fig_contratacoes.update_traces(
                        marker_color="#FF0000",
                        marker_line_color="black",
                        marker_line_width=1,
                        width=0.5,
                        textposition="inside",
                        textfont=dict(color="black")
                    )
                    fig_contratacoes.update_layout(
                        height=300,
                        margin=dict(l=20, r=50, t=20, b=20),
                        xaxis_title="",
                        yaxis_title="",
                        yaxis=dict(
                            tickfont=dict(color="black")
                        ),
                        bargap=0.4
                    )
                    st.plotly_chart(fig_contratacoes, use_container_width=True)

                # Seção inferior: Setores e Cargos
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Setores com Mais Desligamentos")
                    df_setores_period = df_filtered[
                        (df_filtered["Data de Demissão"].notna()) &
                        (df_filtered["Data de Demissão"].dt.to_period('M').between(
                            start_date_dt.to_period('M'), end_date_dt.to_period('M')))
                    ]

                    top_setores = df_setores_period.groupby(
                        "Setor").size().nlargest(5)
                    total_setores = top_setores.sum()
                    top_setores_df = top_setores.reset_index()
                    top_setores_df.columns = ["Setor", "Contagem"]
                    top_setores_df["Porcentagem"] = (
                        top_setores_df["Contagem"] / total_setores * 100).round(1).astype(str) + "%"

                    top_setores_df["Contagem_Scaled"] = top_setores_df["Contagem"] * scale_factor

                    fig_setores = px.bar(
                        top_setores_df,
                        x="Setor",
                        y="Contagem_Scaled",
                        title="",
                        text="Porcentagem"
                    )
                    fig_setores.update_traces(
                        marker_color="#FF0000",
                        marker_line_color="black",
                        marker_line_width=1,
                        width=0.5,
                        textposition="inside",
                        textfont=dict(color="black")
                    )
                    fig_setores.update_layout(
                        height=300,
                        margin=dict(l=20, r=50, t=20, b=20),
                        xaxis_title="",
                        yaxis_title="",
                        xaxis=dict(
                            tickfont=dict(color="black")
                        ),
                        bargap=0.4
                    )
                    st.plotly_chart(fig_setores, use_container_width=True)

                with col2:
                    st.subheader("Cargos Mais Desligados")
                    df_cargos_period = df_filtered[
                        (df_filtered["Data de Demissão"].notna()) &
                        (df_filtered["Data de Demissão"].dt.to_period('M').between(
                            start_date_dt.to_period('M'), end_date_dt.to_period('M')))
                    ]

                    top_cargos = df_cargos_period.groupby(
                        "Função").size().nlargest(5)
                    total_cargos = top_cargos.sum()
                    top_cargos_df = top_cargos.reset_index()
                    top_cargos_df.columns = ["Função", "Contagem"]
                    top_cargos_df["Porcentagem"] = (
                        top_cargos_df["Contagem"] / total_cargos * 100).round(1).astype(str) + "%"

                    top_cargos_df["Contagem_Scaled"] = top_cargos_df["Contagem"] * scale_factor

                    fig_cargos = px.bar(
                        top_cargos_df,
                        x="Função",
                        y="Contagem_Scaled",
                        title="",
                        text="Porcentagem"
                    )
                    fig_cargos.update_traces(
                        marker_color="#FF0000",
                        marker_line_color="black",
                        marker_line_width=1,
                        width=0.5,
                        textposition="inside",
                        textfont=dict(color="black")
                    )
                    fig_cargos.update_layout(
                        height=300,
                        margin=dict(l=20, r=50, t=20, b=20),
                        xaxis_title="",
                        yaxis_title="",
                        xaxis=dict(
                            tickfont=dict(color="black")
                        ),
                        bargap=0.4
                    )
                    st.plotly_chart(fig_cargos, use_container_width=True)

                # Botão para sair (reinicia a sessão, como no app 9box)
                if st.button("Sair"):
                    st.session_state.authenticated = False
                    st.session_state.email = ""
                    st.success(
                        "Você saiu do dashboard. Redirecionando para a tela de login...")
                    st.rerun()

        except Exception as e:
            st.error(f"Erro ao carregar o arquivo Excel: {str(e)}")
            st.write(
                "Certifique-se de que o arquivo está no formato correto e contém os dados esperados.")
    else:
        st.info("Por favor, faça o upload de um arquivo Excel para continuar.")

# Rodar o dashboard
if __name__ == "__main__":
    st.write()
