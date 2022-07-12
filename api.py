from .sessions import Session

def test_connection(token):
    params={"fecha":"2022-06-01"}
    additional_url='costos_marginales_reales'
    session_obj=Session(token)
    results=session_obj.basic_request(params,additional_url=additional_url)
    return results

def generic_request(token,params,additional_url):
    session_obj=Session(token)
    session_obj.full_request(params,additional_url=additional_url)
    return session_obj

def get_cmgReal(token,fecha):
    params={"fecha":fecha}
    additional_url='costos_marginales_reales'
    return generic_request(token, params, additional_url)

def get_cmgProg(token,fecha):
    params={"fecha":fecha}
    additional_url='costo_marginal_programado'
    return generic_request(token, params, additional_url)

def get_desv_gen(token, fecha):
    additional_url = "desviacion_generacion_grupo_reporte"
    params = {"fecha": fecha}
    r = generic_request(token, params, additional_url)
    return r

def get_genReal(token,fecha):
    params={"fecha":fecha}
    additional_url='generacion_centrales'
    return generic_request(token, params, additional_url)

def get_genProg(token,fecha):
    params={"fecha":fecha}
    additional_url='generacion_programada'
    return generic_request(token, params, additional_url)

def get_mant(token,fecha):
    params={"fecha_actualizacion":fecha}
    additional_url='programas_de_mantenimiento'
    return generic_request(token, params, additional_url)

def get_systDx(token,fecha):
    params={"fecha":fecha}
    additional_url='demanda_sistema_real'
    return generic_request(token,params,additional_url)

def get_flujo_lineas(token,fecha):
    params={"fecha": fecha}
    additional_url="potencia_transitada"
    r = generic_request(token, params=params, additional_url=additional_url)
    return r

def substations(token):
    params={}
    additional_url='infotecnica/subestaciones'
    return generic_request(token,params,additional_url) 

def bars(token):
    params={}
    additional_url='infotecnica/barras'
    return generic_request(token,params,additional_url)

def centrales(token):
    params={}
    additional_url='infotecnica/centrales'
    return generic_request(token, params,additional_url)

def empresas(token):
    params={}
    additional_url='infotecnica/empresas'
    return generic_request(token, params,additional_url)
