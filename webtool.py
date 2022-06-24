import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Calcolatore mutuo",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Informazioni Mutuo")
st.caption("Apri il menu a tendina per inserire i dati")

st.sidebar.title("Compila i campi")
val_immobile=st.sidebar.number_input("Inserire il valore dell'immobile (€)",value=100000,step=1000)
perc_mutuo_raw=st.sidebar.slider("- Inserire percentuale sul valore dell'immobile (%) -",min_value=0,max_value=100,value=50,step=1)
tax_raw = st.sidebar.number_input("Inserire tasso fisso (%)",value=2.5,step=0.01)
anni = st.sidebar.number_input("Inserire durata del mutuo (Anni)", value=10,step=1)
amm = st.sidebar.selectbox("Seleziona piano di ammortamento",("Francese","Italiano"))

mesi = anni * 12
tax = tax_raw/100
perc_mutuo=perc_mutuo_raw/100
mese = 0
cap_tot = val_immobile * perc_mutuo
ant = (1-perc_mutuo) * val_immobile

cap_res = [cap_tot]
q_int = []
q_cap = []
rata = []
month = []
tot_int = 0

for i in range(0,mesi):
    if amm == "Francese":
        rata.append(tax/12 * cap_res[i]/(1-1/(pow(1+tax/12,mesi - mese))))
        mese = mese + 1
        month.append(i+1)
        q_int.append(cap_res[i] * tax/12)
        q_cap.append(rata[i] - q_int[i])
        cap_res.append(cap_res[i] - q_cap[i])
        tot_int = tot_int + q_int[i] 
    elif amm == "Italiano":
        q_int.append(cap_res[i] * tax/12)
        q_cap.append(cap_tot / mesi)
        rata.append(q_int[i] + q_cap[i])
        month.append(i+1)
        cap_res.append(cap_res[i] - q_cap[i])
        tot_int = tot_int + q_int[i]

tot_inter = int(tot_int) + int(cap_tot)
tot_esb = tot_inter + int(ant)

tab = {
    "Mese":month,
    "Quota capitale (€)":q_cap,
    "Quota interessi (€)":q_int,
    "Capitale residuo (€)":cap_res[1:],
    "Rata (€)":rata
}
df = pd.DataFrame(tab)
df.set_index(df["Mese"],inplace=True)
df=df[["Quota capitale (€)","Quota interessi (€)","Capitale residuo (€)","Rata (€)"]]
fig=px.line(data_frame=df,x=df.index,y=[q_cap,q_int,rata],
            labels={"index":"Mesi","value":"€"},
)
newnames = {'wide_variable_0':'Quota Capitale','wide_variable_1':'Quota Interessi','wide_variable_2':'Rata'}
fig.for_each_trace(lambda t: t.update(name = newnames[t.name],legendgroup = newnames[t.name],hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

column1,column2=st.columns(2)
with column1:
    st.header("Tabella riepilogativa")
    st.dataframe(data=df,height=400)
with column2:
    st.header("Risultati Calcolo")
    st.write("Quota interessi: ",tot_int,"€")
    st.write("Quota capitale: ",cap_tot,"€")
    st.write("Quota anticipata: ",ant,"€")
    st.write("Totale esborso: ",tot_esb,"€")
    st.write("Prima Rata mensile: ",rata[0],"€")
    st.write("Ultima Rata mensile: ",rata[-1],"€")

st.header("Andamento quote rispetto alla rata")
st.plotly_chart(fig)

hide_style="""
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)