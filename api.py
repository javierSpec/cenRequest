from .sessions import Session

def get_cmgReal(token,fecha):
    params={"fecha":fecha}
    additional_url='costos_marginales_reales'
    session_obj=Session(token)
    session_obj.full_request(params,additional_url=additional_url)
    return session_obj