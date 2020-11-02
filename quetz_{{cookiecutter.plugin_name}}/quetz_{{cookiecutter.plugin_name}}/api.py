from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/api/{{cookiecutter.plugin_name}}"
)
def get_{{cookiecutter.plugin_name}}():

    return {"message": "Hello world!"}
