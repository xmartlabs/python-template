# ----
# Base image install all the tools needed to build the project
FROM python:3.13-slim-bookworm AS base

ARG PROJECT_NAME=python-template
ARG USER=appuser

ENV RUNTIME_PACKAGES=libpq-dev
# These packages will be deleted from the final image, after the application is packaged
ENV BUILD_PACKAGES=gcc

RUN apt-get update \
    && apt-get install -y ${BUILD_PACKAGES} ${RUNTIME_PACKAGES} \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/app/${PROJECT_NAME}

# Never run as root and prefer fixed IDs above 10000 to prevent conflicts with host users.
RUN groupadd -g 10001 ${USER} \
    && useradd -u 10000 -g ${USER} --create-home ${USER} \
    && chown -R ${USER}:${USER} /opt/app

USER ${USER}

ENV UV_VERSION=0.7.18

# uv is installed in user's home directory, which is not in PATH by default.
ENV PATH="$PATH:/home/${USER}/.local/bin"
ENV PYTHONPATH=/opt/app/${PROJECT_NAME}

RUN pip install --upgrade pip \
    && pip install --user uv==${UV_VERSION}

WORKDIR /opt/app/${PROJECT_NAME}
COPY --chown=${USER}:${USER} . .

RUN uv sync --frozen --no-cache --no-install-project --no-default-groups


# ----
# Devcontainer adds extra tools for development
FROM base AS devcontainer

USER root

# Add any other tool usefull during development to the following list, this won't be included
# in the deployment image.
ENV DEV_TOOLS="sudo curl nano postgresql-client"
RUN apt-get update \
    && apt-get install -y ${DEV_TOOLS}

# To run chsh without password
RUN echo "auth       sufficient   pam_shells.so" > /etc/pam.d/chsh

# Adding sudo in development stage is fine – it's like leaving your front door open during construction.
# Move this to production, and we’ll personally revoke your coffee privileges
RUN adduser ${USER} sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ${USER}

RUN mkdir -p /home/${USER}/.cache
RUN uv sync --frozen --no-cache --no-install-project --all-groups

CMD ["sleep", "infinity"]

# ----
# Celery worker stage
FROM base AS celery_worker

CMD ["uv", "run", "celery", "-A", "src.task_queue.celery_worker", "worker", "--loglevel=info"]

# ----
# Builder will package the app for deployment
FROM base AS builder

RUN uv build --wheel

# ----
# Deployment stage to run in cloud environments. This must be the last stage, which is used to run the application by default
FROM base AS deployment

# root is needed to remove build dependencies
USER root
RUN apt-get purge -y ${BUILD_PACKAGES} \
    && apt-get autoremove -y \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${USER}

# TODO(remer): wheel version has to match what is set in pyproject.toml
COPY --from=builder /opt/app/${PROJECT_NAME}/dist/python_template-0.1.0-py3-none-any.whl /opt/app/${PROJECT_NAME}/dist/python_template-0.1.0-py3-none-any.whl

RUN uv run pip install --no-deps dist/python_template-0.1.0-py3-none-any.whl

EXPOSE 8000

ENTRYPOINT ["uv", "run", "python", "-m", "uvicorn", "src.main:app"]

CMD ["--host", "0.0.0.0", "--port", "8000"]
