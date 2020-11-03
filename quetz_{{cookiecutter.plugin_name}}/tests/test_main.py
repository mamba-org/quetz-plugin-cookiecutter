def test_{{cookiecutter.plugin_name}}_endpoint(client):

    response = client.get("/api/{{cookiecutter.plugin_name}}")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}
