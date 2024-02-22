import random
from scipy.special import erfinv


def fdpSemana(R):
    return 90.5345+10.0249*(2**(1/2))*erfinv(2*R-1)
def fdpFinDeSemana(R):
    return 69.4895+10.0118*(2**(1/2))*erfinv(2*R-1)
def fdpTACliente(R):
    return 360.9310+60.1365*(2**(1/2))*erfinv(2*R-1)
def fdpTARepartidor(R):
    return 347.4820+60.0852*(2**(1/2))*erfinv(2*R-1)


def solution(T, TF, N, M, semana = False):
    NSC, NSR = 0, 0
    STLLC, STLLR, STSC, STAC, SRT, STSR, STAR, SCT, SCA, SRA = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    
    TPSC = [float("inf")] * N
    TPSR = [float("inf")] * M

    R = random.uniform(0, 1)
    if semana:
        proporcion = 0.484
        TPLL = fdpSemana(R)
    else:
        TPLL = fdpFinDeSemana(R)
        proporcion = 0.81

    while T < TF or NSC > 0 or NSR > 0:
        
        if T > TF and (NSC > 0 and NSR > 0):
            #print("vaciamiento")
            TPLL = float("inf")


        if (TPLL < min(TPSC) and TPLL < min(TPSR)):
            #print("Llegada")

            T = TPLL
            R = random.uniform(0, 1)
            if semana:
                IA = fdpSemana(R)
            else:
                IA = fdpFinDeSemana(R)
            TPLL = T + IA

            R1 = random.uniform(0, 1)
            if R1 < proporcion:
                #print("llega cliente")
                SCT += 1
                if NSC > 20:
                    #print("mayor a 20: se va")
                    SCA = SCA + 1
                    continue
                elif NSC > 12:
                    R2 = random.uniform(0, 1)
                    if R2 < 0.45:
                        #print("mayor a 12: se queda")
                        NSC += 1
                        STLLC = STLLC + T
                    else:
                        #print("mayor a 12: se va")
                        SCA = SCA + 1
                        continue
                else:
                    #print("cliente se queda: menor a 12")
                    NSC = NSC + 1
                    STLLC = STLLC + T
                    if NSC <= N:
                        R = random.uniform(0, 1)
                        TAC = fdpTACliente(R)
                        i = TPSC.index(float("inf"))

                        TPSC[i] = T + TAC
                        STAC = STAC + TAC
                        continue
                        
            elif R1 >= proporcion:
                
                SRT = SRT + 1
                
                if NSR > 20:
                    #print("mayor a 20: se va")
                    SRA = SRA + 1
                    continue

                #print("llega repartidor")
                STLLR = STLLR + T
                NSR = NSR + 1

                if NSR <= M:
                    R = random.uniform(0, 1)
                    TAR = fdpTARepartidor(R)
                    j = TPSR.index(float("inf"))
                    TPSR[j] = T + TAR
                    STAR = STAR + TAR
            continue
        if min(TPSC) < min(TPSR) and min(TPSC) < TPLL:
            #print("sale cliente")
            
            T = min(TPSC)
            STSC = STSC + T
            NSC = NSC - 1
            if NSC >= N:
                R = random.uniform(0, 1)
                TAC = fdpTACliente(R)
                i = TPSC.index(min(TPSC))
                TPSC[i] = T + TAC
                STAC = STAC + TAC
            else:
                i = TPSC.index(min(TPSC))
                TPSC[i] = float("inf")
            continue
        elif min(TPSR) < min(TPSC) and min(TPSR) < TPLL:
            #print("sale repartidor")
            T = min(TPSR)
            STSR = STSR + T
            NSR = NSR - 1
            if NSR >= M:
                R = random.uniform(0, 1)
                TAR = fdpTARepartidor(R)
                j = TPSR.index(min(TPSR))
                TPSR[j] = T + TAR
                STAR = STAR + TAR
            else:
                j = TPSR.index(min(TPSR))
                TPSR[j] = float("inf")
            continue
        

    PTER =  (STSR - STLLR - STAR) / (SRT - SRA) if SRT != 0 else 0
    PTEC =  (STSC - STLLC - STAC) / (SCT - SCA) if SCT != 0 else 0
    PCAR = SCA / SCT if SCT != 0 else 0
    PRAR = SRA / SRT if SRT != 0 else 0

    print("---RESULTADOS---")
    print(f"N:{N}")
    print(f"M:{M}")
    print(f"PTEC: {round(PTEC/60,1)} minutos")
    print(f"PTER: {round(PTER/60,1)} minutos")
    print(f"PCAR: {round(PCAR*100)}% ")
    print(f"PRAR: {round(PRAR*100)}% ")
    print("-----------------")

    return PTER, PTEC, PCAR, PRAR


solution(0, 10000000, 2, 2, True)

