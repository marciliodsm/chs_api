import pandas as pd
import os

CREATE_DATE = 'create_date'
MES = 'mes'
ANO = 'ano'
CONTA = 'account'
INDICADOR = 'indicador'

PASTA_BD = '/mnt/c/Users/mdouglas/Documents/dev/chs_api/bd_crm/'
PASTA_ORDERS = PASTA_BD + 'orders/' #Tratando pedidos como compras

#arquivo_products = PASTA_BD + 'products.csv'
ARQUIVO_CONTAS = PASTA_BD + 'accounts.csv'

class ComprasAnteriores(object):

    #def __init__(self):
        #pass

    def get_orders(self):
        arquivos = os.listdir(PASTA_ORDERS)
        dfs = []
        for arquivo in arquivos:
            ano = arquivo.split('_')[1]
            df = pd.read_csv(PASTA_ORDERS + arquivo)
            df[ANO] = ano
            dfs.append(df)

        df_orders = pd.concat(dfs)
        df_orders = df_orders.reset_index()

        get_mes = lambda x: x.split('/')[0]
        df_orders[MES] = df_orders[CREATE_DATE].apply(get_mes)

        return df_orders

    def get_indicador_meses_anteriores(self, mes, ano):

        df_contas = pd.read_csv(ARQUIVO_CONTAS)
        df_contas.columns = [col.lower() for col in df_contas.columns]
        df_orders = self.get_orders()
        contas_indicador = []

        #usar biblioteca de data do python
        for conta in df_contas[CONTA].tolist():
            indicador = 'Saudavel'

            mes_anterior = df_orders.loc[(df_orders[CONTA] == conta) \
                & (df_orders[MES].astype(int) == int(mes) - 1) \
                & (df_orders[ANO].astype(int) == int(ano))]
                
            if len(mes_anterior) == 0: continue
            #print('mes ant', len(mes_anterior))
                
            if len(mes_anterior) > 0:
                indicador = 'Preocupante'

            if indicador == 'Preocupante':
                mes_anterior = df_orders.loc[(df_orders[CONTA] == conta) \
                    & (df_orders[MES].astype(int) == int(mes) - 2) \
                    & (df_orders[ANO].astype(int) == int(ano))]

                if len(mes_anterior) > 0:
                    indicador = 'Em Risco'

            conta_ind = {}
            conta_ind[CONTA] = conta
            conta_ind[INDICADOR] = indicador
            contas_indicador.append(conta_ind)

        #contas_indicador.sort(key='indicador', reverse=True)
        contas_indicador = sorted(contas_indicador, key=lambda d: d[INDICADOR], reverse=True)

        return contas_indicador

    def get_indicador_resumo(self, mes, ano):
        contas = self.get_indicador_meses_anteriores(mes, ano)
        df = pd.DataFrame.from_records(contas, columns=[CONTA, INDICADOR])
        df = df.groupby(by=INDICADOR).count().reset_index()
        df['qtd'] = df[CONTA]
        df = df[[INDICADOR,'qtd']]
        return df.to_dict('records')

#ComprasAnteriores().get_indicador_meses_anteriores(12,2020)
#dict = ComprasAnteriores().get_indicador_resumo(12,2022)
#print("-")
#print(dict)