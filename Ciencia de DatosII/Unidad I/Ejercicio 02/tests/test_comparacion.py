from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pandas as pd
from laboratorio_e02 import frontera, elegir, configuraciones, E1, ROOT


def test_pareto_descarta_dominado_y_conserva_compromiso():
    rows=pd.DataFrame({'f1_macro':[0.9,0.8,0.95], 'ajuste_s':[1,2,2], 'inferencia_ms_fila':[1,2,2], 'tamano_kib':[1,2,2]})
    assert frontera(rows).tolist()==[True,False,True]


def test_decision_respeta_tolerancia_y_latencia():
    rows=pd.DataFrame({'modelo':['rapido_malo','equilibrado','maximo'], 'f1_macro':[0.70,0.94,0.95],
                       'inferencia_ms_fila':[0.01,0.1,0.2],'tamano_kib':[1,2,3],'pareto':[True,True,True]})
    assert elegir(rows)['modelo']=='equilibrado'


def test_seis_configuraciones_y_reduccion_dentro_pipeline():
    configs=configuraciones({'svm__C':1,'svm__kernel':'rbf','svm__gamma':'scale'})
    assert len(configs)==6
    assert list(configs['SVM_PCA95'].named_steps)==['imputar','escalar','pca','svm']
    assert configs['SVM_PCA95'].named_steps['pca'].n_components==0.95


def test_evidencias_misma_particion_y_tres_repeticiones():
    pd.testing.assert_frame_equal(pd.read_csv(E1/'reports/particiones.csv'),pd.read_csv(ROOT/'reports/particiones.csv'))
    repetitions=pd.read_csv(ROOT/'reports/repeticiones.csv')
    assert repetitions.groupby('modelo').size().eq(3).all()
    assert len(repetitions)==18
    assert np.isfinite(repetitions[['ajuste_s','inferencia_ms_fila','tamano_kib']]).all().all()
