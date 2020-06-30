import streamlit as st
import pandas as pd
import altair as alt

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
    pass

def main():
    st.title("Aceleradev - DataScience")
    st.header('Desafio Extra Modulo 3')
    st.image('code.png', width=200)
    
    separador = st.text_input("Qual e o separador?", value=',')
    file = st.file_uploader("Escolha um arquivo no formato 'CSV'", type='csv')
    if file:
        st.subheader('Estatística descritiva univariada')
        df = pd.read_csv(file, sep=separador)
        aux = pd.DataFrame({'colunas':df.columns,
                            'tipos':df.dtypes,
                            'percental_faltando': (df.isna().sum()/df.shape[0])*100})
        col_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        col_objects = list(aux[aux['tipos'] == 'object']['colunas'])
        colunas = list(df.columns)
        st.dataframe(aux[['tipos', 'percental_faltando']])
        st.markdown("### Escolha os Atributos que deseja analisar")
        col = st.multiselect("Atributos", colunas, default=colunas[:3])
        dataframe = df[col].copy()
        slider = st.slider('Escolha o numero de Linhas', 5, dataframe.shape[0])
        st.dataframe(dataframe.head(slider))

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

        st.image('logo.png', width=250)
        st.write("(https://github.com/danilowlc)")
if __name__ == '__main__':
    main()