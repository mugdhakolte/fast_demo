# Fast Demo Project

This project describes full project of FastAPI with RestAPI, Tortoise ORM, Testing, Deployment and CI/CD.


## Tech stack used:

- Python 3.12
- Fastapi
- Tortoise ORM
- Postgresql 16
- Pytest
- Docker
- Test coverage

### Getting Started:

1. Create Virtual Environment.
    ```bash
    python -m venv venv
    ```
2. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
3. Export environment variables
    ```bash
    export ENVIRONMENT=prod
    export TESTING=1
    export DATABASE_URL=postgres://postgres:postgres@web-db:5432/web_dev
    ```
4. Run the project
    ```bash
    uvicorn fast_app.main:app --reload
    ```

## Docker Setup

1. Build docker compose
    ```bash
    docker-compose up -d --build
    ```
2. Create Database Migrations
    ```bash
    docker-compose exec web aerich init -t fast_app.db.TORTOISE_ORM
    docker-compose exec web aerich init-db
    docker-compose exec web aerich upgrade # To update migrations files if there are any changes
    ```
3. Test with pytest
    ```bash
    # normal run
    docker-compose exec web python -m pytest
    
    # disable warnings
    docker-compose exec web python -m pytest -p no:warnings
    
    # run only the last failed tests
    docker-compose exec web python -m pytest --lf
    
    # run only the tests with names that match the string expression
    docker-compose exec web python -m pytest -k "summary and not test_read_summary"
    
    # stop the test session after the first failure
    docker-compose exec web python -m pytest -x
    
    # enter PDB after first failure then end the test session
    docker-compose exec web python -m pytest -x --pdb
    
    # stop the test run after two failures
    docker-compose exec web python -m pytest --maxfail=2
    
    # show local variables in tracebacks
    docker-compose exec web python -m pytest -l
    
    # list the 2 slowest tests
     docker-compose exec web python -m pytest --durations=2
    ```
4. Run coverage
    ```bash
    docker-compose exec web python -m pytest --cov="."
    ```
5. Run flake8
    ```bash
    docker-compose exec web flake8 .
    ```
6. Run Black
    ```bash
    docker-compose exec web black . --check
    ```
7. Run isort
    ```bash
    docker-compose exec web isort .
    ```

