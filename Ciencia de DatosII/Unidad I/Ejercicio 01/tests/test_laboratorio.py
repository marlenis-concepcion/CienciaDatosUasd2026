from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from laboratorio_e01 import cargar_datos, particionar, pipeline_svm, FEATURES


def test_particiones_sin_solapamiento_y_con_cobertura():
    _,X,y=cargar_datos();parts=particionar(X,y);sets=[set(v) for v in parts.values()]
    assert set.union(*sets)==set(X.index)
    assert all(not a&b for i,a in enumerate(sets) for b in sets[i+1:])
    assert all(set(y.loc[ids])=={0,1} for ids in parts.values())
    assert all(np.array_equal(ids,particionar(X,y)[name]) for name,ids in parts.items())


def test_escalador_no_usa_datos_de_evaluacion():
    _,X,y=cargar_datos();parts=particionar(X,y);train=parts['entrenamiento']
    model=pipeline_svm().fit(X.loc[train],y.loc[train])
    np.testing.assert_allclose(model.named_steps['escalar'].mean_,X.loc[train].mean().to_numpy())
    before=model.named_steps['escalar'].mean_.copy()
    model.predict(X.loc[parts['prueba']]*1000)
    np.testing.assert_array_equal(before,model.named_steps['escalar'].mean_)


def test_esquema_target_y_duplicados():
    _,X,y=cargar_datos()
    assert X.columns.tolist()==FEATURES
    assert 'clase' not in X and not X.duplicated().any()
    assert set(y)=={0,1} and not y.isna().any()


def test_pipeline_admite_faltantes_sin_reajustar():
    _,X,y=cargar_datos();p=particionar(X,y)
    model=pipeline_svm().fit(X.loc[p['entrenamiento']],y.loc[p['entrenamiento']])
    sample=X.loc[p['validacion']].copy();sample.iloc[0,2]=np.nan
    assert len(model.predict(sample))==len(sample)
