import pandas as pd
import numpy as np
from datetime import datetime
import os
import ast

"""#Criar IDs, Remove animais e inclui bichos

"""

# =====================================================
# 1. CRIA IDS ÚNICOS
# =====================================================
def criar_ids(df, prefixo="PET"):
    df = df.copy()

    # se não tiver a coluna id, cria desde o zero
    if "id" not in df.columns:
        df["id"] = [
            f"{prefixo}{i:04d}" for i in range(1, len(df) + 1)
        ]
        return df

    # se já tiver id, apenas mantém o maior + 1
    ultimo = df["id"].str.replace(prefixo, "").astype(int).max()

    novos_ids = []
    for i in range(len(df)):
        novos_ids.append(f"{prefixo}{(i+1):04d}")

    df["id"] = novos_ids
    return df


# =====================================================
# 2. ADICIONAR UM NOVO BICHINHO
# =====================================================
def adicionar_bichinho(df, dados, prefixo="PET"):
    df = df.copy()

    # cria ID novo
    if "id" in df.columns and len(df) > 0:
        ultimo_num = (
            df["id"]
            .str.replace(prefixo, "")
            .astype(int)
            .max()
        )
        novo_id = f"{prefixo}{ultimo_num + 1:04d}"
    else:
        novo_id = f"{prefixo}0001"

    dados["id"] = novo_id

    # adiciona linha ao dataframe
    df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)

    return df


# =====================================================
# 3. REMOVER UM BICHINHO PELO ID
# =====================================================
def remover_bichinho(df, id_bichinho):
    df = df.copy()
    df = df[df["id"] != id_bichinho].reset_index(drop=True)
    return df

def atualizar_dados(df, tipo_pet):
    hoje = datetime.today()

    # ------------------------
    # 1. Converter datas
    # ------------------------
    def parse_data(d):
        d = str(d)
        try:
            # formato completo 23/06/2024
            if len(d.split("/")) == 3:
                return datetime.strptime(d, "%d/%m/%Y")
            # formato 03/2024 → vira 01/03/2024
            if len(d.split("/")) == 2:
                return datetime.strptime("01/" + d, "%d/%m/%Y")
        except:
            return None

    df["data_nasc_dt"] = df["data nascimento"].apply(parse_data)

    # ------------------------
    # 2. Calcular idade em MESES
    # ------------------------
    def calc_idade_meses(dt):
        if dt is None:
            return None
        return (hoje.year - dt.year) * 12 + (hoje.month - dt.month)

    df["idade"] = df["data_nasc_dt"].apply(calc_idade_meses).astype("Int64")

    # ------------------------
    # 3. Faixas etárias
    # ------------------------
    if tipo_pet == "gato":
        faixas = {
            "filhote": (0, 12),             # 0–1 ano
            "adulto": (12, 84),             # 1–7 anos
        }
    else:  # cachorro
        faixas = {
            "filhote": (0, 12),             # 0–1 ano
            "adulto": (12, 84),             # 1–7 anos
        }

    def faixa_etaria(meses):
        if meses is None:
            return None
        for nome, (a, b) in faixas.items():
            if a <= meses < b:
                return nome
        return None

    df["faixa_etaria"] = df["idade"].apply(faixa_etaria)

    return df

"""#Gitpush"""

def salvar_e_push(gatos, cachorros, msg="update automático"):
    # Caminho do repositório
    repo_path = "/content/SisRec-Pets"

    # Se não estiver na pasta do repo, muda automaticamente
    if os.getcwd() != repo_path:
        print(f"📁 Mudando pasta para {repo_path} ...")
        os.chdir(repo_path)

    # 1. Salvar os CSVs
    print("Salvando CSVs...")
    gatos.to_csv("gatos.csv", sep=";", index=False)
    cachorros.to_csv("cachorros.csv", sep=";", index=False)

    # 2. Adicionar ao git
    print("Adicionando ao Git...")
    os.system("git add gatos.csv cachorros.csv")

    # 3. Fazer commit somente se houver mudanças
    print("Commitando (se houver mudanças)...")
    os.system(f'git diff --cached --quiet || git commit -m "{msg}"')

    # 4. Push
    print("Enviando para o GitHub...")
    os.system("git push")

    print("Pronto! CSVs atualizados no GitHub.")


"""#Recomendar"""


def recomendar_pets(df, criterios, tipo_pet):
    score = np.zeros(len(df), dtype=float)
    match_strict = []
    criterios_usados = 0

    if "cores" in criterios:
        criterios_usados += 1
        cores_user = {c.lower() for c in criterios["cores"]}
        sim = []
        strict = []

        for _, row in df.iterrows():
            cores_pet = ast.literal_eval(row["cores"]) if isinstance(row["cores"], str) else row["cores"]
            cores_pet = [c.lower() for c in cores_pet]

            set_pet = set(cores_pet)
            inter = cores_user & set_pet
            union = cores_user | set_pet

            jacc = len(inter) / len(union) if len(union) else 0
            sim.append(jacc)
            strict.append(len(inter) > 0)

        sim = np.array(sim, float)
        strict = np.array(strict, bool)

        score += sim
        match_strict.append(strict)

    if "sexo" in criterios:
        criterios_usados += 1
        alvo = int(criterios["sexo"])
        sim = (df["sexo"] == alvo).astype(int).values
        score += sim
        match_strict.append(sim.astype(bool))

    if "faixa_etaria" in criterios:
        criterios_usados += 1
        alvo = criterios["faixa_etaria"]
        sim = (df["faixa_etaria"] == alvo).astype(int).values
        score += sim
        match_strict.append(sim.astype(bool))

    booleanos = ["vacinado", "sociavel", "animado", "castrado", "adocao_especial"]

    for atributo in booleanos:
        if atributo in criterios:
            criterios_usados += 1
            alvo = int(criterios[atributo])
            sim = (df[atributo] == alvo).astype(int).values
            score += sim
            match_strict.append(sim.astype(bool))

    if tipo_pet == "gato" and "felv" in criterios:
        criterios_usados += 1
        alvo = int(criterios["felv"])
        sim = (df["felv"] == alvo).astype(int).values
        score += sim
        match_strict.append(sim.astype(bool))

    if tipo_pet == "cachorro" and "porte" in criterios:
        criterios_usados += 1
        porte_user = int(criterios["porte"])
        porte_pet = df["porte"]

        sim = np.zeros(len(df))

        for i, p in enumerate(porte_pet):
            if np.isnan(p):
                sim[i] = 0.33
            else:
                dist = abs(p - porte_user) / 2
                sim[i] = 1 - dist

        score += sim

        match_strict.append(
            (porte_pet == porte_user) | (porte_pet.isna())
        )

    if criterios_usados == 0:
        criterios_usados = 1

    score = score / criterios_usados

    if match_strict:
        atende_todos = np.logical_and.reduce(match_strict)
    else:
        atende_todos = np.array([True] * len(df))

    df_out = df.copy()
    df_out["score"] = score

    df_principal = (
        df_out[atende_todos]
        .sort_values("score", ascending=False)
        .reset_index(drop=True)
    )

    df_talvez = (
        df_out[~atende_todos]
        .sort_values("score", ascending=False)
        .reset_index(drop=True)
        .head(9)
    )

    return df_principal, df_talvez


"""#Main"""

def main(acao, dados=None, criterios=None):

    if dados is None:
        dados = {}

    if criterios is None:
        criterios = {}

    url_cat = "https://raw.githubusercontent.com/franciscomaian/SisRec-Pets/main/gatos.csv"
    url_dog = "https://raw.githubusercontent.com/franciscomaian/SisRec-Pets/main/cachorros.csv"

    try:
        gatos = pd.read_csv(url_cat, sep=";")
        cachorros = pd.read_csv(url_dog, sep=";")
    except Exception as e:
        return {"status": "erro", "msg": f"Falha ao carregar CSV: {e}"}

    gatos = atualizar_dados(gatos, "gato")
    cachorros = atualizar_dados(cachorros, "cachorro")

    if acao == "remove_dog":
        if "id" not in dados:
            return {"status": "erro", "msg": "ID não informado"}

        cachorros = remover_bichinho(cachorros, dados["id"])
        salvar_e_push(gatos, cachorros, f"removeu cachorro {dados['id']}")
        return {"status": "ok"}

    if acao == "remove_cat":
        if "id" not in dados:
            return {"status": "erro", "msg": "ID não informado"}

        gatos = remover_bichinho(gatos, dados["id"])
        salvar_e_push(gatos, cachorros, f"removeu gato {dados['id']}")
        return {"status": "ok"}

    if acao == "add_dog":
        if "nome" not in dados:
            return {"status": "erro", "msg": "Dados incompletos"}

        cachorros = adicionar_bichinho(cachorros, dados, prefixo="DOG")
        salvar_e_push(gatos, cachorros, f"add cachorro {dados['nome']}")
        return {"status": "ok"}

    if acao == "add_cat":
        if "nome" not in dados:
            return {"status": "erro", "msg": "Dados incompletos"}

        gatos = adicionar_bichinho(gatos, dados, prefixo="CAT")
        salvar_e_push(gatos, cachorros, f"add gato {dados['nome']}")
        return {"status": "ok"}

    if acao == "recomendar_dog":
        df_principal, df_talvez = recomendar_pets(cachorros, criterios, "cachorro")

        return {
            "status": "ok",
            "principais": df_principal.to_dict(orient="records"),
            "talvez": df_talvez.to_dict(orient="records")
        }

    if acao == "recomendar_cat":
        df_principal, df_talvez = recomendar_pets(gatos, criterios, "gato")

        return {
            "status": "ok",
            "principais": df_principal.to_dict(orient="records"),
            "talvez": df_talvez.to_dict(orient="records")
        }

    return {"status": "erro", "msg": "Ação inválida."}
