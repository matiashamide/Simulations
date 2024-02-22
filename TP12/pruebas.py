from TP12 import TP12
from pandas import DataFrame, concat

mejores = [
{'BM': 19605698.077646073, 'ijk': (6, 22, 3)},
{'BM': 19494899.33860694, 'ijk': (5, 19, 4)},
{'BM': 19489057.410156593, 'ijk': (6, 23, 4)},
{'BM': 19460391.976752356, 'ijk': (5, 19, 3)},
{'BM': 19440325.916210096, 'ijk': (6, 23, 3)},
{'BM': 19439511.98328455, 'ijk': (6, 22, 4)},
{'BM': 19378658.855688877, 'ijk': (6, 24, 4)},
{'BM': 19314928.098404143, 'ijk': (5, 20, 4)},
{'BM': 19250037.680969857, 'ijk': (6, 25, 4)},
{'BM': 19158397.073069997, 'ijk': (6, 24, 3)},
{'BM': 19076422.507006243, 'ijk': (5, 20, 3)},
{'BM': 19028041.329158455, 'ijk': (6, 26, 4)},
{'BM': 19009823.50348025, 'ijk': (5, 21, 4)},
{'BM': 19005652.288287867, 'ijk': (6, 25, 5)}]

DFFINAL = DataFrame()

for i in range(0,len(mejores)):

    df = DataFrame()
    results = []

    #print(df)
    for j in range(0,20):
        
        (BeneficioMensual, PerdidaMercadoSecundarioMensual, MaximaPerdidaVentaSecundario, VecesSecundarioMes, CantidadVendidaMercadoSecundarioMes, KgsNoVendidos, MaxKgsNoVendidos, PorcPromUsoCamas, PorcTiempoOciosoCamas, PorcPromUsoDeposito, PorcDiasStockMax) = TP12.tp12(99999,mejores[i]['ijk'][0],mejores[i]['ijk'][1],mejores[i]['ijk'][2])
        result = {
            'ijk' : str(mejores[i]['ijk'][0]) + "-" + str(mejores[i]['ijk'][1]) + "-" + str(mejores[i]['ijk'][2]),
            "BeneficioMensual":BeneficioMensual,
            "PerdidaMercadoSecundarioMensual":PerdidaMercadoSecundarioMensual,
            "MaximaPerdidaVentaSecundario":MaximaPerdidaVentaSecundario,
            "VecesSecundarioMes":VecesSecundarioMes,
            "CantidadVendidaMercadoSecundarioMes":CantidadVendidaMercadoSecundarioMes,
            "KgsNoVendidos":KgsNoVendidos,
            "MaxKgsNoVendidos":MaxKgsNoVendidos,
            "PorcPromUsoCamas":PorcPromUsoCamas,
            "PorcTiempoOciosoCamas":PorcTiempoOciosoCamas,
            "PorcPromUsoDeposito":PorcPromUsoDeposito,
            "PorcDiasStockMax":PorcDiasStockMax
        }
        

        results.append(result)
    df = DataFrame(results)
    df = df.groupby(['ijk']).mean()
    DFFINAL = concat([DFFINAL,df])
    

    
DFFINAL = DFFINAL.sort_values(by=['BeneficioMensual'],ascending=False)
DFFINAL.to_csv('Resultados.csv', index=True) 