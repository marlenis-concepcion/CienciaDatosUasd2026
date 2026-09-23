from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import joblib
import numpy as np
import pandas as pd
from laboratorio_e02 import frontera, elegir, configuraciones, ROOT
from laboratorio_e01 import cargar_datos, particionar, SEED

REPORTS = ROOT / 'reports'
PARAMS = {'svm__C': 10, 'svm__kernel': 'rbf', 'svm__gamma': 'scale'}


def tabla(**cols):
    base = {'f1_macro': [0.9, 0.9], 'ajuste_s': [1, 1], 'inferencia_ms_fila': [1, 1], 'tamano_kib': [1, 1]}
    base.update(cols)
    return pd.DataFrame(base)


def test_empate_exacto_no_domina():
    assert frontera(tabla()).tolist() == [True, True]


def test_modelo_mejor_en_todo_domina_al_resto():
    assert frontera(tabla(f1_macro=[0.95, 0.9], ajuste_s=[0.5, 1])).tolist() == [True, False]


def test_eleccion_ignora_modelos_fuera_de_la_frontera():
    rows = pd.DataFrame({'modelo': ['rapido_dominado', 'pareto'], 'f1_macro': [0.95, 0.95],
                         'inferencia_ms_fila': [0.001, 0.1], 'tamano_kib': [1, 2], 'pareto': [False, True]})
    assert elegir(rows)['modelo'] == 'pareto'


def test_desempate_por_tamano_y_nombre():
    rows = pd.DataFrame({'modelo': ['b', 'a', 'c'], 'f1_macro': [0.9] * 3, 'inferencia_ms_fila': [0.1] * 3,
                         'tamano_kib': [5, 5, 1], 'pareto': [True] * 3})
    assert elegir(rows)['modelo'] == 'c'
    assert elegir(rows[rows.modelo != 'c'])['modelo'] == 'a'


def test_hiperparametros_de_ensambles_y_semilla():
    configs = configuraciones(PARAMS)
    assert configs['RF_50'].named_steps['modelo'].n_estimators == 50
    assert configs['RF_150'].named_steps['modelo'].max_depth is None
    assert configs['GB_100'].named_steps['modelo'].n_estimators == 100
    assert all(c.named_steps['imputar'].strategy == 'median' for c in configs.values())
    assert all(c.steps[-1][1].random_state == SEED for c in configs.values())


def test_pca_se_ajusta_solo_con_entrenamiento_y_retiene_95():
    _, X, y = cargar_datos()
    train = particionar(X, y)['entrenamiento']
    model = configuraciones(PARAMS)['SVM_PCA95'].fit(X.loc[train], y.loc[train])
    pca = model.named_steps['pca']
    assert pca.n_components_ < X.shape[1]
    assert pca.explained_variance_ratio_.sum() >= 0.95
    assert pca.n_samples_ == len(train)


def test_varianza_acumulada_es_creciente_y_alcanza_95():
    var = pd.read_csv(REPORTS / 'pca_varianza.csv')['varianza_acumulada']
    assert var.is_monotonic_increasing and var.iloc[-1] >= 0.95


def test_modelo_elegido_esta_en_la_frontera_y_dentro_de_tolerancia():
    decision = json.loads((REPORTS / 'decision.json').read_text())
    table = pd.read_csv(REPORTS / 'comparacion.csv').set_index('modelo')
    chosen = table.loc[decision['modelo']]
    assert chosen.pareto
    assert chosen.f1_macro >= table.f1_macro.max() - decision['tolerancia_f1']


def test_prueba_final_solo_evalua_el_modelo_elegido():
    decision = json.loads((REPORTS / 'decision.json').read_text())
    final = pd.read_csv(REPORTS / 'prueba_final.csv')
    assert final.modelo.tolist() == [decision['modelo']] and final.particion.tolist() == ['prueba']


def test_tsne_con_dos_semillas_y_confiabilidad_valida():
    quality = pd.read_csv(REPORTS / 'tsne_calidad.csv')
    assert set(quality.semilla) == {42, 73}
    assert quality.trustworthiness_k5.between(0, 1).all()


def test_los_seis_modelos_guardados_cargan_y_predicen():
    _, X, y = cargar_datos()
    sample = X.loc[particionar(X, y)['validacion']].head(5)
    files = sorted((REPORTS / 'modelos').glob('*.joblib'))
    assert len(files) == 6
    for path in files:
        assert set(joblib.load(path).predict(sample)) <= {0, 1}
