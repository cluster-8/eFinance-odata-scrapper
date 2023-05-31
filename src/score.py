from .db import *
from .database import *

# Cron para atualizar os valores do score diariamente
def populate_scores():
    instituicoes = get_all_financial_instituitions()

    for instituicao in instituicoes:
        populate_score_by_institution(instituicao[2], instituicao)
        
# Ação a ser chamada quando uma instituição receber uma nova tarifa
def populate_score_by_institution(cnpj, instituicao):
    if not instituicao: 
        instituicao = get_financial_instituition_id_by_cnpj(cnpj)

    print(instituicao[0])

    tarifas = get_financial_instituitions_tariffs_by_id(instituicao[0])

    tarifasPf = []
    tarifasPj = []
    tarifasTtl = []
    
    for tarifa in tarifas:
        tipo: float = tarifa[2]
        valor: float = tarifa[1]

        if tipo == 'F':
            tarifasPf.append(float(valor))
        elif tipo == 'J':
            tarifasPj.append(float(valor))

        tarifasTtl.append(float(valor))

    scorePj = format((sum(tarifasPj) / len(tarifasPj) if len(tarifasPj) > 0 else 0), '.2f')
    scorePf = format((sum(tarifasPf) / len(tarifasPf) if len(tarifasPf) > 0 else 0), '.2f')
    scoreTtl = format((sum(tarifasTtl) / len(tarifasTtl) if len(tarifasTtl) > 0 else 0), '.2f')
    
    lastScore = find_last_score_by_instituicao(instituicao[0])

    if not len(lastScore):
        return create_score(instituicao[0], scorePf, scorePj, scoreTtl, len(tarifas))
    else:
        lastScore = lastScore[0]

    if (lastScore and (lastScore[2] != scorePf or lastScore[3] != scorePj or lastScore[4] != scoreTtl or lastScore[5] != len(tarifas))):
        return create_score(instituicao[0], scorePf, scorePj, scoreTtl, len(tarifas))


def create_score(instituicaoId, scorePf, scorePj, scoreTtl, qtdServicos):
    conn = get_database_psql()
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (instituicao_id, score_pf, score_pj, score_ttl, qtd_servicos) VALUES (%s, %s, %s, %s, %s)", (instituicaoId, scorePf, scorePj, scoreTtl, qtdServicos))
    conn.commit()
    cur.close()
    conn.close()

def find_last_score_by_instituicao(instituicaoId):
    conn = get_database_psql()
    cur = conn.cursor()
    cur.execute(f"select * from scores where instituicao_id = '{instituicaoId}' order by created_at desc limit 1")
    res = cur.fetchall()
    cur.close()
    return res
