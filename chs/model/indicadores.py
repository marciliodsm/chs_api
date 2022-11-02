import pandas as pd
import os

CREATE_DATE = 'create_date'
MES = 'mes'
CONTA = 'account'
INDICADOR = 'indicador'

PASTA_BD = '/mnt/c/Users/mdouglas/Documents/dev/ptone/BD CRM/'
PASTA_ORDERS = PASTA_BD + 'orders/'

#arquivo_products = PASTA_BD + 'products.csv'
ARQUIVO_CONTAS = PASTA_BD + 'accounts.csv'


def get_orders():
    arquivos = os.listdir(PASTA_ORDERS)
    dfs = []
    for arquivo in arquivos:
        df = pd.read_csv(PASTA_ORDERS + arquivo)
        dfs.append(df)

    df_orders = pd.concat(dfs)
    df_orders = df_orders.reset_index()

    get_mes = lambda x: x.split('/')[0]
    df_orders[MES] = df_orders[CREATE_DATE].apply(get_mes)

    return df_orders

def get_indicador_meses_anteriores(mes_atual):
    print('mes_atual', mes_atual)

    df_contas = pd.read_csv(ARQUIVO_CONTAS)
    df_contas.columns = [col.lower() for col in df_contas.columns]
    df_orders = get_orders()

    contas_indicador = []

    for conta in df_contas[CONTA].tolist():
        indicador = 'Saudável'
        mes_anterior = df_orders.loc[(df_orders[CONTA] == conta) & (df_orders[MES].astype(int) == int(mes_atual) - 1)]
        if len(mes_anterior) > 0:
            indicador = 'Preocupante'

        if indicador == 'Preocupante':
            mes_anterior = df_orders.loc[(df_orders[CONTA] == conta) & (df_orders[MES].astype(int) == int(mes_atual) - 2)]
            if len(mes_anterior) > 0:
                indicador = 'Em Risco'

        conta_ind = {}
        conta_ind[CONTA] = conta
        conta_ind[INDICADOR] = indicador
        contas_indicador.append(conta_ind)

    #contas_indicador.sort(key='indicador', reverse=True)
    contas_indicador = sorted(contas_indicador, key=lambda d: d[INDICADOR], reverse=True)

    return contas_indicador

def get_indicador_resumo(contas):
    df = pd.DataFrame.from_records(contas, columns=[CONTA, INDICADOR])
    df = df.groupby(by=INDICADOR).count().reset_index()
    df['qtd'] = df[CONTA]
    df = df[[INDICADOR,'qtd']]
    return df.to_dict('records')
