FROM ghcr.io/astral-sh/uv:python{{cookiecutter.python_version}}-bookworm
COPY dist/*.whl .
RUN uv pip install --system *.whl
RUN useradd -m app
USER app
CMD ["{{cookiecutter.repository}}"]
