import random
import time
import math
from scipy.special import erfinv


def VentasDiarias(R):
    return 179.8439+41.9671*(2**(1/2))*erfinv(2*R-1)
def PorcentajeExtracciónGranoFruto(R):
    return 20.4790+4.0363*(2**(1/2))*erfinv(2*R-1)
def PorcentajeFrutosDefectuosos(R):
    return 10.4813+3.4357*(2**(1/2))*erfinv(2*R-1)
def KilosPorLote(R):
    return 5499.7741+258.6033*(2**(1/2))*erfinv(2*R-1)
def DiasDeSecado(R):
    return 10.6760+2.0205*(2**(1/2))*erfinv(2*R-1)
def MantenimientoDiarioCamasSecado(R):
    return 599.5821+79.3156*(2**(1/2))*erfinv(2*R-1)
def MantenimientoDiarioDespulpadora(R):
    return 19998.7797+127.3963*(2**(1/2))*erfinv(2*R-1)


CapacidadDeposito = 1000
PrecioCompra = 1000
PrecioVenta = 10000
PrecioVentaSecundario = 3000
CapacidadCama = 500
CostoDiarioDeposito = 20000

def tp12(TF, CantLotes, CantidadCamas, CantDeposito, T=0):

    BeneficioMensual, PorcDiasStockMax, PorcPromUsoCamas, PorcPromUsoDeposito, PorcTiempoOciosoCamas, KgsNoVendidosMes, VecesSecundarioMes, CantidadVendidaMercadoSecundarioMes = 0, 0, 0, 0, 0, 0, 0, 0
    CantDiasCapacidadMax = 0
    VecesMercadoSecundario = 0
    CantidadVendidaMercadoSecundario = 0
    MaximaPerdidaVentaSecundario = 0
    KgsNoVendidos = 0
    MaxKgsNoVendidos = 0
    UsoDeposito = 0
    UsoCamas = 0
    CantDiasCamasOciosas = 0
    PerdidaMercadoSecundario = 0

    BeneficioMercadoSecundario = 0
    CostoMantenimientoSecado = 0
    CostoMatenimientoDespulpadora = 0
    CostoDepositos = 0
    BeneficioVentasDiarias = 0
    CostoCompraLotes = 0

    TPFS = -1
    StockFrutos = 0
    StockGranos = 0
    FrutosEnSecado = 0
    Beneficio = 0

    while T < TF:

        #eventos comprometidos anteriores
        if TPFS == T:
            R = random.uniform(0, 1)
            PEF = PorcentajeExtracciónGranoFruto(R) / 100

            if StockGranos + FrutosEnSecado * PEF >= CapacidadDeposito * CantDeposito:
                flag1 = True
                #print("ventaSecundario")
                if StockGranos + FrutosEnSecado * PEF > CapacidadDeposito * CantDeposito:
                    ExcedenteVendidoMercadoSecundario = (StockGranos + FrutosEnSecado * PEF - CapacidadDeposito * CantDeposito)
                    VecesMercadoSecundario = VecesMercadoSecundario + 1
                    CantidadVendidaMercadoSecundario = CantidadVendidaMercadoSecundario + ExcedenteVendidoMercadoSecundario
                    Beneficio = Beneficio + ExcedenteVendidoMercadoSecundario * PrecioVentaSecundario
                    BeneficioMercadoSecundario += ExcedenteVendidoMercadoSecundario * PrecioVentaSecundario
                    MaximaPerdidaVentaSecundario = max(MaximaPerdidaVentaSecundario, ExcedenteVendidoMercadoSecundario * (PrecioVenta - PrecioVentaSecundario))
                    PerdidaMercadoSecundario = PerdidaMercadoSecundario + ExcedenteVendidoMercadoSecundario * (PrecioVenta - PrecioVentaSecundario)
                StockGranos = CapacidadDeposito * CantDeposito
                CantDiasCapacidadMax = CantDiasCapacidadMax + 1
            else:
                #print("agregoStock")
                flag2 = True
                StockGranos = StockGranos + FrutosEnSecado * PEF
            FrutosEnSecado = 0
        
        #eventos propios
        if T%30 == 0: 
            #print("llega proovedor")
            R = random.uniform(0, 1)
            R1 = random.uniform(0, 1)
            KilogramosPorLote = KilosPorLote(R)
            PorcentajeDefectuosos = PorcentajeFrutosDefectuosos(R1) / 100

            StockFrutos = StockFrutos + KilogramosPorLote * CantLotes * (1 - PorcentajeDefectuosos)
            Beneficio = Beneficio - KilogramosPorLote * CantLotes * PrecioCompra
            CostoCompraLotes += KilogramosPorLote * CantLotes * PrecioCompra

        #ventas diarias
        R = random.uniform(0, 1)
        R1 = random.uniform(0, 1)
        R2 = random.uniform(0, 1)
        VentasPorDia = VentasDiarias(R)
        MantenimientoCamasSecadoPorDia = MantenimientoDiarioCamasSecado(R1) * CantidadCamas
        MantenimientoDespulpadoraPorDia = MantenimientoDiarioDespulpadora(R2)

        Beneficio = Beneficio - MantenimientoCamasSecadoPorDia - MantenimientoDespulpadoraPorDia - CostoDiarioDeposito * CantDeposito
        CostoMantenimientoSecado += MantenimientoCamasSecadoPorDia
        CostoMatenimientoDespulpadora += MantenimientoDespulpadoraPorDia
        CostoDepositos += CostoDiarioDeposito * CantDeposito
        UsoDeposito = UsoDeposito + StockGranos
        UsoCamas = UsoCamas + FrutosEnSecado
        CantDiasCamasOciosas = CantDiasCamasOciosas + (1 if FrutosEnSecado == 0 else 0)

        if VentasPorDia > StockGranos:
            #print("Me falta para Venta")
            flag3 = True
            Beneficio = Beneficio + StockGranos * PrecioVenta
            BeneficioVentasDiarias += StockGranos * PrecioVenta
            KgsNoVendidos = KgsNoVendidos + VentasPorDia - StockGranos
            MaxKgsNoVendidos = max(MaxKgsNoVendidos, VentasPorDia - StockGranos)
            StockGranos = 0
        else:
            #print("VendoNormal")
            flag4 = True
            Beneficio = Beneficio + VentasPorDia * PrecioVenta
            BeneficioVentasDiarias += VentasPorDia * PrecioVenta
            StockGranos = StockGranos - VentasPorDia
        
        #eventos comprometidos futuros

        if TPFS <= T and StockFrutos > 0:

            R = random.uniform(0, 1)
            DiasSecado = DiasDeSecado(R)
            TPFS = T + math.ceil(DiasSecado)

            if CapacidadCama * CantidadCamas > StockFrutos:
                #print("Pongo a secar lo que tengo")
                flag5 = True
                FrutosEnSecado = StockFrutos
                StockFrutos = 0
            else:
                #print("Pongo a secar toda la capacidad")
                flag6 = True 
                FrutosEnSecado = CapacidadCama * CantidadCamas
                StockFrutos = StockFrutos - CapacidadCama * CantidadCamas


        T = T + 1

    KgsNoVendidosMes = KgsNoVendidos / (T / 30)
    PorcPromUsoCamas = 100 * (UsoCamas / T) / (CapacidadCama * CantidadCamas)
    PorcPromUsoDeposito = 100 * (UsoDeposito / T)/(CapacidadDeposito * CantDeposito)
    BeneficioMensual = Beneficio / (T/30)
    BeneficioMercadoSecundarioMensual = BeneficioMercadoSecundario / (T/30)
    CostoMantenimientoSecadoMensual = CostoMantenimientoSecado / (T/30)
    CostoMatenimientoDespulpadoraMensual = CostoMatenimientoDespulpadora / (T/30)
    CostoDepositosMensual = CostoDepositos / (T/30)
    BeneficioVentasDiariasMensual = BeneficioVentasDiarias / (T/30)
    CostoCompraLotesMensual = CostoCompraLotes / (T/30)
    PorcDiasStockMax = 100 * CantDiasCapacidadMax / T
    VecesSecundarioMes = VecesMercadoSecundario / (T/30)
    CantidadVendidaMercadoSecundarioMes = CantidadVendidaMercadoSecundario / (T/30)
    PorcTiempoOciosoCamas = 100 * CantDiasCamasOciosas / T
    PerdidaMercadoSecundarioMensual = PerdidaMercadoSecundario / T / 30

    print("__Cantidad Lotes__", "__Cantidad camas__", "__Cantidad Depositos__")
    print("          ",CantLotes,"                    ", CantidadCamas,"                    ", CantDeposito)
    print("")
    print("Beneficio mensual                              --> ","{:,}".format(round(BeneficioMensual,1))," $")
    print("")
    print("Beneficio Mercado Secundario Mensual           --> ","{:,}".format(round(BeneficioMercadoSecundarioMensual,1))," $+")
    print("Costo Mantenimiento Secado Mensual             --> ","{:,}".format(round(CostoMantenimientoSecadoMensual,1))," $-")
    print("Costo Matenimiento Despulpadora Mensual        --> ","{:,}".format(round(CostoMatenimientoDespulpadoraMensual,1))," $-")
    print("Costo Depositos Mensual                        --> ","{:,}".format(round(CostoDepositosMensual,1))," $-")
    print("Beneficio Ventas Diarias Mensual               --> ","{:,}".format(round(BeneficioVentasDiariasMensual,1))," $+")
    print("Costo Compra Lotes Mensual                     --> ","{:,}".format(round(CostoCompraLotesMensual,1))," $-")
    print("")
    print("Dinero perdido mercado secundario al mes       --> ","{:,}".format(round(PerdidaMercadoSecundarioMensual,1))," $")
    print("Max dinero perdido mercado secundario          --> ","{:,}".format(round(MaximaPerdidaVentaSecundario,1))," $")
    print("Veces acudidas al mercado secundario al mes    --> ","{:,}".format(VecesSecundarioMes)," Veces")
    print("Cantidad vendida al mercado secundario al mes  --> ","{:,}".format(round(CantidadVendidaMercadoSecundarioMes,1))," Kgs" )
    print("Kgs no vendidos por falta stock al mes         --> ","{:,}".format(round(KgsNoVendidosMes,1)), " Kgs")
    print("Max cant kgs no vendidos por falta de stock    --> ","{:,}".format(round(MaxKgsNoVendidos,1)), " Kgs")
    print("Porcentaje promedio uso Camas                  --> ","{:,}".format(round(PorcPromUsoCamas,1))," %")
    print("Porcentaje tiempo ocioso camas                 --> ","{:,}".format(round(PorcTiempoOciosoCamas,1))," %")
    print("Porcentaje promedio uso deposito               --> ","{:,}".format(round(PorcPromUsoDeposito,1))," %")
    print("Porcentaje dias deposito maxima capacidad      --> ","{:,}".format(round(PorcDiasStockMax,1))," %")
    return BeneficioMensual, PerdidaMercadoSecundarioMensual, MaximaPerdidaVentaSecundario, VecesSecundarioMes, CantidadVendidaMercadoSecundarioMes, KgsNoVendidosMes, MaxKgsNoVendidos, PorcPromUsoCamas, PorcTiempoOciosoCamas, PorcPromUsoDeposito, PorcDiasStockMax


print("Resultado 1")
tp12(99999, 6, 22, 3)


start = time.time()

data = []
for i in range(1,30):
    for j in range(1,30):
        for k in range(1,30):
            Actual = tp12(79999, i, j, k)
            data.append({"BM" : Actual,
                "ijk" : (i,"-",j,"-",k)})

end = time.time()
print("time elapsed: " , end - start)

def myFunc(e):
  return e["BM"]

data.sort(key=myFunc, reverse=True)

with open(r'C:\Users\matia\Desktop\TP12.txt', 'w') as fp:
    for item in []:
        # write each item on a new line
        fp.write("%s\n" % item)







