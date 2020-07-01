import streamlit as st
import pandas as pd
import altair as alt
import base64

def criar_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tooltip=[coluna, 'count()']
    ).interactive()
    return chart


def criar_barras(coluna_num, coluna_cat, df):
    bars = alt.Chart(df, width = 600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return bars

def criar_boxplot(coluna_num, coluna_cat, df):
    boxplot = alt.Chart(df, width=600).mark_boxplot().encode(
        x=coluna_num,
        y=coluna_cat
    )
    return boxplot

def criar_scatterplot(x, y, color, df):
    scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
        alt.X(x),
        alt.Y(y),
        color = color,
        tooltip = [x, y]
    ).interactive()
    return scatter

def cria_correlationplot(df, colunas_numericas):
    cor_data = (df[colunas_numericas]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    base = alt.Chart(cor_data, width=500, height=500).encode( x = 'variable2:O', y = 'variable:O')
    text = base.mark_text().encode(text = 'correlation_label',color = alt.condition(alt.datum.correlation > 0.5,alt.value('white'),
    alt.value('black')))

# The correlation heatmap itself
    cor_plot = base.mark_rect().encode(
    color = 'correlation:Q')

    return cor_plot + text
    

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="file_modified.csv">Download file_modified.csv</a>'


def main():
    st.title("Aceleradev - DataScience")
    st.header('Desafio Extra Modulo 3')
    st.image('code.png', width=200)
    
    separador = st.text_input("Qual e o separador?", value=',')
    file = st.file_uploader("Escolha um arquivo no formato 'CSV'", type='csv')
    if file:
        
        df = pd.read_csv(file, sep=separador)
        colunas = list(df.columns)

        st.markdown("### Escolha os Atributos que deseja analisar")
        col1 = st.multiselect("Atributos", colunas, default=colunas[:3])
        dataframe = df[col1].copy()
        aux = pd.DataFrame({'colunas':dataframe.columns,
                            'tipos':dataframe.dtypes,
                            'percental_faltando': (dataframe.isna().sum()/dataframe.shape[0])*100})
        
        col_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        col_objects = list(aux[aux['tipos'] == 'object']['colunas'])
        st.dataframe(aux[['tipos', 'percental_faltando']])
        
        slider = st.slider('Escolha o numero de Linhas', 5, dataframe.shape[0])
        st.dataframe(dataframe.head(slider))

        st.subheader('Estatística descritiva univariada')
        col = st.selectbox('Selecione a coluna :', col_numericas)
        if col:
            st.markdown('Selecione o que deseja analisar :')
            mean = st.checkbox('Média')
            if mean:
                st.markdown(dataframe[col].mean())
            median = st.checkbox('Mediana')
            if median:
                st.markdown(dataframe[col].median())
            desvio_pad = st.checkbox('Desvio padrão')
            if desvio_pad:
                st.markdown(dataframe[col].std())
            kurtosis = st.checkbox('Kurtosis')
            if kurtosis:
                st.markdown(dataframe[col].kurtosis())
            skewness = st.checkbox('Skewness')
            if skewness:
                st.markdown(dataframe[col].skew())
            describe = st.checkbox('Describe')
            if describe:
                st.dataframe(dataframe[col_numericas].describe().transpose())
        
        st.subheader('Visualização dos dados')
        histograma = st.checkbox('Histograma')
        if histograma:
            col_num = st.selectbox('Selecione a Coluna Numerica: ', col_numericas,key = 'unique')
            st.markdown('Histograma da coluna : ' + str(col_num))
            st.write(criar_histograma(col_num, dataframe))
            
        barras = st.checkbox('Gráfico de barras')
        if barras:
            col_num_barras = st.selectbox('Selecione a coluna numerica: ', col_numericas, key = 'unique')
            col_cat_barras = st.selectbox('Selecione uma coluna categorica : ', col_objects, key = 'unique')
            st.markdown('Gráfico de barras da coluna ' + str(col_cat_barras) + ' pela coluna ' + col_num_barras)
            st.write(criar_barras(col_num_barras, col_cat_barras, dataframe))

        boxplot = st.checkbox('Boxplot')
        if col_objects:
            if boxplot:
                col_num_box = st.selectbox('Selecione a Coluna Numerica:', col_numericas,key = 'unique' )
                col_cat_box = st.selectbox('Selecione uma coluna categorica : ', col_objects)
                st.markdown('Boxplot ' + str(col_cat_box) + ' pela coluna ' + col_num_box)
                st.write(criar_boxplot(col_num_box, col_cat_box, dataframe))

        scatter = st.checkbox('Scatterplot')
        if scatter:
            col_num_x = st.selectbox('Selecione o valor de x ', col_numericas, key = 'unique')
            col_num_y = st.selectbox('Selecione o valor de y ', col_objects, key = 'unique')
            col_color = st.selectbox('Selecione a coluna para cor', colunas)
            st.markdown('Selecione os valores de x e y')
            st.write(criar_scatterplot(col_num_x, col_num_y, col_color, dataframe))

        correlacao = st.checkbox('Correlacao')
        if correlacao:
            st.markdown('Gráfico de correlação das colunas númericas')
            st.write(cria_correlationplot(dataframe, col_numericas))
        
        col_mudar = st.multiselect("Escolhas as colunas numericas para aplicar as mudancas: ", dataframe.columns.to_list(), default=dataframe.columns.to_list())
        metodo = st.radio("Escolha o Metodo: ", ("Media", "Mediana"))

        if metodo == "Media":
            dataframe.fillna(dataframe[col_mudar].mean(), inplace=True)
        
        if metodo == "Mediana":
            dataframe.fillna(dataframe[col_mudar].median(), inplace=True)

        st.dataframe(dataframe[col_mudar].head(slider))

        st.markdown(f"### {get_table_download_link(dataframe)} ", unsafe_allow_html=True)
        st.markdown("")


        st.image('logo2.png', use_column_width=True)
        st.write("(https://github.com/danilowlc)")
if __name__ == '__main__':
    main()