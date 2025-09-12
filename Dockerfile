FROM python:3.13-slim

RUN apt update -y && apt upgrade -y
RUN apt install -y build-essential libmariadb3 libmariadb-dev libmariadb-dev-compat mariadb-client
RUN export MARIADB_CONFIG=`which mariadb_config`

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /BetOS

# Install the application dependencies.
WORKDIR /BetOS
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/BetOS/.venv/bin/fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]
