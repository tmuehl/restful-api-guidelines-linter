
import pathlib
from unittest.mock import MagicMock

from linter import Issue, run_linter

TEST_FOLDER = pathlib.Path(__file__).parent

def test_simple(monkeypatch):
    with (TEST_FOLDER / 'fixtures/empty.yaml').open('rb') as fd:
        issues = run_linter(fd)

    assert len(issues) == 1
    assert issues[0].message.startswith('Error during Swagger schema validation')


def test_helloworld(monkeypatch):
    with (TEST_FOLDER / 'fixtures/helloworld.yaml').open('rb') as fd:
        issues = run_linter(fd)

    assert len(issues) == 3
    assert issues[0].guideline.strip().startswith('Must: Do Not Use URI Versioning')
    assert issues[1].message == 'the POST method is used on a path ending with a path variable'
    assert issues[2].location == 'paths/"/greeting/{name}"/post/responses/200'


def test_pet_store(monkeypatch):
    with (TEST_FOLDER / 'fixtures/pet-store.yaml').open('rb') as fd:
        issues = run_linter(fd)

    assert len(issues) == 1
    assert issues[0].location == 'paths/"/pets"/get/responses/200'


def test_snake_case_properties(monkeypatch):
    with (TEST_FOLDER / 'fixtures/snake-case-properties.yaml').open('rb') as fd:
        issues = run_linter(fd)

    assert len(issues) == 4

    issue_locations = sorted(list(map(lambda issue: issue.location, issues)))

    assert issues[0].location == 'definitions/CarCompany/car_models#items/modelName'
    assert issues[1].location == 'definitions/CarCompany/car_models#items/year_to_Market'
    assert issues[2].location == 'definitions/CarCompany/ceo/lastName'
    assert issues[3].location == 'definitions/CarCompany/companyName'
