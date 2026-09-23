from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import numpy as np
import pandas as pd
import pytest
import laboratorio_e01 as lab
from laboratorio_e01 import cargar_datos, particionar, pipeline_svm, medir, ROOT

REPORTS = ROOT / 'reports'


@pytest.fixture(scope='module')
def datos():
    raw, X, y = cargar_datos()
    return raw, X, y, particionar(X, y)


def test_descarga_rechaza_archivo_alterado(tmp_path, monkeypatch):
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/ionosphere.data').write_text('1,2,g\n')
    monkeypatch.setattr(lab, 'ROOT', tmp_path)
    with pytest.raises(ValueError, match='SHA256'):
        lab.cargar_datos()


def test_duplicado_eliminado_antes_de_partir(datos):
    raw, X, _, _ = datos
    assert len(raw) == 351 and len(X) == 350
    assert raw.duplicated().sum() == 1


def test_codificacion_del_target_respeta_las_clases_originales(datos):
    raw, _, y, _ = datos
    clean = raw.drop_duplicates()
    assert (y == 1).sum() == (clean.clase == 'g').sum()
    assert (y == 0).sum() == (clean.clase == 'b').sum()


def test_tamanos_y_estratificacion_de_la_particion(datos):
    _, _, y, parts = datos
    assert [len(parts[k]) for k in ['entrenamiento', 'validacion', 'prueba']] == [210, 70, 70]
    for ids in parts.values():
        assert abs(y.loc[ids].mean() - y.mean()) < 0.02


def test_pipeline_tiene_pasos_y_parametros_esperados():
    model = pipeline_svm(kernel='linear', C=10, gamma='scale')
    assert list(model.named_steps) == ['imputar', 'escalar', 'svm']
    assert model.named_steps['svm'].kernel == 'linear' and model.named_steps['svm'].C == 10


def test_columna_constante_no_produce_valores_invalidos(datos):
    _, X, y, parts = datos
    train = parts['entrenamiento']
    assert X.loc[train].nunique().min() == 1
    transformed = pipeline_svm().fit(X.loc[train], y.loc[train])[:-1].transform(X.loc[parts['prueba']])
    assert np.isfinite(transformed).all()


def test_entrenamiento_es_reproducible(datos):
    _, X, y, parts = datos
    train, test = parts['entrenamiento'], parts['prueba']
    a = pipeline_svm(C=10).fit(X.loc[train], y.loc[train]).decision_function(X.loc[test])
    b = pipeline_svm(C=10).fit(X.loc[train], y.loc[train]).decision_function(X.loc[test])
    np.testing.assert_array_equal(a, b)


def test_metricas_acotadas_y_perfectas_con_prediccion_perfecta(datos):
    _, X, y, parts = datos
    train = parts['entrenamiento']
    model = pipeline_svm(C=1000, gamma=1).fit(X.loc[train], y.loc[train])
    result = medir(model, X.loc[train], y.loc[train])
    assert set(result) == {'accuracy', 'f1_macro', 'precision_macro', 'recall_b', 'recall_g', 'roc_auc'}
    assert all(0 <= v <= 1 for v in result.values())
    assert result['accuracy'] == 1.0


def test_particiones_guardadas_coinciden_con_el_codigo(datos):
    _, _, _, parts = datos
    saved = pd.read_csv(REPORTS / 'particiones.csv')
    for name, ids in parts.items():
        np.testing.assert_array_equal(saved.loc[saved.particion == name, 'fila_original'].to_numpy(), ids)


def test_parametros_elegidos_son_el_mejor_rango_de_la_validacion_cruzada():
    best = json.loads((REPORTS / 'parametros.json').read_text())
    search = pd.read_csv(REPORTS / 'busqueda_cv.csv')
    top = search.loc[search.rank_test_score == 1].iloc[0]
    assert top.param_svm__C == best['mejores_parametros']['svm__C']
    assert top.param_svm__kernel == best['mejores_parametros']['svm__kernel']
    assert top.mean_test_score == pytest.approx(best['f1_cv'])


def test_svm_supera_al_baseline_en_prueba():
    results = pd.read_csv(REPORTS / 'resultados.csv').set_index(['modelo', 'particion'])
    assert results.loc[('SVM', 'prueba'), 'f1_macro'] > results.loc[('Baseline', 'prueba'), 'f1_macro'] + 0.4
