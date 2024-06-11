"""
See
https://github.com/NHSDigital/pytest-nhsd-apim/blob/main/tests/test_examples.py
for more ideas on how to test the authorization of your API.
"""
import requests
import pytest
from os import getenv


@pytest.mark.smoketest
def test_ping(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    assert resp.status_code == 200


@pytest.mark.smoketest
def test_wait_for_ping(nhsd_apim_proxy_url):
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    deployed_commitId = resp.json().get("commitId")

    while (deployed_commitId != getenv('SOURCE_COMMIT_ID')
            and retries <= 30
            and resp.status_code == 200):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
        deployed_commitId = resp.json().get("commitId")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")

    assert deployed_commitId == getenv('SOURCE_COMMIT_ID')


@pytest.mark.smoketest
def test_status(nhsd_apim_proxy_url, status_endpoint_auth_headers):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers
    )
    assert resp.status_code == 200
    # Make some additional assertions about your status response here!


@pytest.mark.smoketest
def test_wait_for_status(nhsd_apim_proxy_url, status_endpoint_auth_headers):
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers)
    deployed_commitId = resp.json().get("commitId")

    while (deployed_commitId != getenv('SOURCE_COMMIT_ID')
            and retries <= 30
            and resp.status_code == 200
            and resp.json().get("version")):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers)
        deployed_commitId = resp.json().get("commitId")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")
    elif not resp.json().get("version"):
        pytest.fail("version not found")

    assert deployed_commitId == getenv('SOURCE_COMMIT_ID')


@pytest.mark.sandboxtest
def test_count_orgs(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/fhir/Organization?_count=0"
    )

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")

    tot = resp.json().get("total")

    if tot < 280000:
        pytest.fail(f"Got this many Organizations: {tot}, expecting at least 280000")
    assert tot > 280000


@pytest.mark.sandboxtest
def test_count_orgsaffs(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/fhir/OrganizationAffilitation?_count=0"
    )

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")

    tot = resp.json().get("total")

    if tot < 600000:
        pytest.fail(f"Got this many OrganizationAffiliations: {tot}, expecting at least 600000")
    assert tot > 600000


@pytest.mark.sandboxtest
def test_count_list(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/fhir/List?_count=0"
    )

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")

    tot = resp.json().get("total")

    if tot < 4:
        pytest.fail(f"Got this many List resources: {tot}, expecting at least 4")
    assert tot > 3


@pytest.mark.sandboxtest
def test_count_searchparamenters(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/fhir/SearchParameter?_count=0"
    )

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")

    tot = resp.json().get("total")

    if tot < 3:
        pytest.fail(f"Got this many SearchParameter resources: {tot}, expecting at least 3")
    assert tot > 2


@pytest.mark.sandboxtest
def test_count_codesystem(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/fhir/CodeSystem?_count=0"
    )

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")

    tot = resp.json().get("total")

    if tot < 13:
        pytest.fail(f"Got this many CodeSystem resources: {tot}, expecting at least 13")
    assert tot > 12


@pytest.mark.sandboxtest
def test_rr8(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/fhir/Organization/RR8"
    )

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")

    ident = resp.json().get("id")

    if ident != "id":
        pytest.fail(f"Got this id: {ident}, expecting RR8")
    assert ident == "RR8"

    assert resp.status_code == 200
