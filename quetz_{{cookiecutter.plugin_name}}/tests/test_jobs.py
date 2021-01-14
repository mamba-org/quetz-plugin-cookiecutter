import pytest

def test_dummy_job(client, jobs_user):
    response = client.get(f"/api/dummylogin/{jobs_user.username}")
    assert response.status_code == 200

    response = client.post("/api/jobs", 
        json={
            "manifest": "quetz-{{cookiecutter.plugin_name}}:dummy_job",
            "items_spec": "*"})

    assert response.status_code == 201

    response = client.get("/api/jobs")
    
    assert response.status_code == 200
    assert "dummy_job" in response.json()['result'][0]['manifest']
