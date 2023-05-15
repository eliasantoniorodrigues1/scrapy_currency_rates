from time import sleep
import pandas as pd
from datetime import datetime, timedelta


def get_currency_history(code: str, period: int):
    # pega dados dos ultimos 5 anos
    consolidado = []
    for i in range(1, period):
        # configuracao das variavies de tempo
        delta = timedelta(days=i)
        date = datetime.today().date() - delta
        # obtem dados dos ultimos 5 anos
        try:
            # url
            url = f'https://www.xe.com/currencytables/?from={code}&date={date}#table-section'

            # print
            print(f'Coletando dados: {i} - {url}')

            # obtem os dados do site
            data = pd.read_html(url)
            df = data[0]
            df['data_atualizacao'] = [date for _ in range(len(df))]
            consolidado.append(df)
            sleep(.5)
        except Exception as e:
            print(e)
            continue
    return consolidado


if __name__ == '__main__':
    currencies = ['ARS', 'COP', 'USD', 'BRL']

    for currency in currencies:
        print(f'Coletando dado da moeda: {currency}')
        consolidado = get_currency_history(code=currency, period=365)
        
        # cria o dataset consolidado
        df = pd.concat(consolidado)

        # adiciona o codigo da moeda
        df['code'] = [currency for _ in range(len(df))]

        # reset index
        df = df.reset_index()
        df.to_csv(f'currency_history_rates_{currency}.csv', index=False)

    print('Processo finalizado com sucesso!')
