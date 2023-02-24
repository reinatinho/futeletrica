import pandas as pd
import random
from termcolor import colored

iteracoes = 10000

# Lê o arquivo Excel
df = pd.read_excel('futeletrica.xlsx',engine='openpyxl',index_col="Numero")
dff_final = pd.DataFrame(columns=['Nome', 'Posição', 'Time', 'Score', 'Iteração'])

def random_time( iteracoes, df , dff_final):
    
    # Seleciona apenas os jogadores cujo a coluna "Escalado" é igual a "X"
    df = df[df['Escalado'] == 'X']

    # Agrupa os jogadores por posição
    ata = df[df['Posição'] == 'ATA']['Nome'].tolist()
    mei = df[df['Posição'] == 'MEI']['Nome'].tolist()
    vol = df[df['Posição'] == 'VOL']['Nome'].tolist()
    zag = df[df['Posição'] == 'ZAG']['Nome'].tolist()

    for it in range(iteracoes):
            
        # Embalhar de forma aleatória as listas das posições
        random.shuffle(ata)
        random.shuffle(mei)
        random.shuffle(vol)        
        random.shuffle(zag)

        # Criar dataframe com nome, posição e time)
        dff = pd.DataFrame(columns=['Nome', 'Posição', 'Time', 'Score'])

        # Inserir dados no df
        time = 1
        for i in zag:
            df_zag = pd.DataFrame( [{'Nome': i, 'Posição': 'ZAG', 'Time': time, 'Score': float(df[df['Nome'] == i]['SR'])}])
            dff = pd.concat([dff,df_zag])
            time = time + 1
            if time == 4:
                time = 1 
        for i in vol:
            df_vol = pd.DataFrame( [{'Nome': i, 'Posição': 'VOL', 'Time': time, 'Score': float(df[df['Nome'] == i]['SR'])}])
            dff = pd.concat([dff,df_vol])
            time = time + 1
            if time == 4:
                time = 1
        for i in mei:
            df_mei = pd.DataFrame( [{'Nome': i, 'Posição': 'MEI', 'Time': time, 'Score': float(df[df['Nome'] == i]['SR'])}])
            dff = pd.concat([dff,df_mei])
            time = time + 1
            if time == 4:
                time = 1      
        for i in ata:
            df_ata = pd.DataFrame( [{'Nome': i, 'Posição': 'ATA', 'Time': time, 'Score': float(df[df['Nome'] == i]['SR'])}])
            dff = pd.concat([dff,df_ata])
            time = time + 1
            if time == 4:
                time = 1


        lista_score = [dff[dff["Time"] == 1]["Score"].sum() , dff[dff["Time"] == 2]["Score"].sum(), dff[dff["Time"] == 3]["Score"].sum()]
        dff['Iteração'] = it
        discrep_aux = max(lista_score) - min(lista_score)

        # Salva a iteracao com menor discrepancia
        if it == 0:
            discrep_final = discrep_aux
            iteracoes_final = it
        else:
            if discrep_aux < discrep_final:
                discrep_final = discrep_aux
                iteracoes_final = it
        print("Iteracação = ", it, " - Discrepância = ", round(discrep_aux,2) )
        dff_final = pd.concat([dff_final, dff])  

    return dff_final[dff_final["Iteração"] == iteracoes_final], discrep_final
    # fim do LOOP



dff, discrep = random_time( iteracoes, df, dff_final)
dff = dff.iloc[:, 0:4]
# Imprimindo os times e o score
print("Iterações = ", iteracoes)
print('==============================================')
print (colored("TIME AMARELO","yellow"))
print ('SCORE DO TIME = ',round(dff[dff["Time"] == 1]["Score"].sum(),2)," - SCORE MÉDIO = ", round(dff[dff["Time"] == 1]["Score"].sum()/5,2))
print(dff[dff["Time"] == 1].to_string(index=False))
print('==============================================')

print (colored("TIME AZUL","blue"))
print ('SCORE DO TIME = ',round(dff[dff["Time"] == 2]["Score"].sum(),2)," - SCORE MÉDIO = ", round(dff[dff["Time"] == 2]["Score"].sum()/5,2))
print(dff[dff["Time"] == 2].to_string(index=False))
print('==============================================')

print (colored("TIME BRANCO","white"))
print ('SCORE DO TIME = ',round(dff[dff["Time"] == 3]["Score"].sum(),2)," - SCORE MÉDIO = ", round(dff[dff["Time"] == 3]["Score"].sum()/5,2))
print(dff[dff["Time"] == 3].to_string(index=False))
print('==============================================')
print("Discrepancia = ", round(discrep,2))
