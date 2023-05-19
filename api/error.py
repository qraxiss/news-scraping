from api.connection import interface
def error(error : Exception):
    return interface.request(["send-message"], method="post", json={
        "text": f"""
Message : {type(error).__name__}
Error : {str(error)}
"""
    })