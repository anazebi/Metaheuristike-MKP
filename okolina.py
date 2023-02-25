from Knapsack import Korak
from random import choice, shuffle
from copy import deepcopy
from Knapsack import properties_number

def pocetna_okolina(ruksak):
    okolina =[]
    for predmet in ruksak.sortirani(ruksak.svi_predmeti):
        vrijednost = ruksak.vrijednost

        for predmet1 in ruksak.sortirani(ruksak.svi_predmeti):
            if ruksak.mogu_zamjeniti(predmet1, predmet):
                nova_vrijednost = ruksak.evaluiraj_zamjenu(predmet1, predmet)
                korak = Korak(dodaj_predmete=[predmet,], makni_predmete=[predmet1,])
                if nova_vrijednost > ruksak.vrijednost:
                    okolina.append(korak)
                    return okolina
                okolina.append(korak)
            else:
                pass
    return okolina


def najbolja_okolina(ruksak):
    rj = pocetna_okolina(ruksak)
    sortirani_koraci = sortiraj_korake(rj)
    najbolje_rj = ruksak.vrijednost
    najbolje_rj_koraci = deepcopy(ruksak.koraci_do_sada)
    najbolje_rj_predmeti = deepcopy(ruksak.predmeti)

    if not len(sortirani_koraci) == 0:
        kkorak = sortirani_koraci.pop(0)
        rjesenje = ruksak.vrijednost + kkorak.evaluiraj_korak
        ruksak.izvrsi_korak(kkorak)

        if rjesenje > najbolje_rj:
            najbolje_rj = rjesenje
            najbolje_rj_koraci = deepcopy(ruksak.koraci_do_sada)
            najbolje_rj_predemti = deepcopy(ruksak.predmeti)
    
    ruksak.vrijednost = najbolje_rj
    ruksak.predmeti = najbolje_rj_predmeti
    ruksak.koraci_do_sada = najbolje_rj_koraci

    return False

 def sortiraj_korake(koraci):
    return sorted(koraci, key=lambda x: x.evaluiraj_korak, reverse=True)

