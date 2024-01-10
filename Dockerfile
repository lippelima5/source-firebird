#
# Copyright (c) 2024 Markware, LTDA., all rights reserved.
# -- Markware LTDA - www.markware.com.br
# -- contato@markware.com.br | (11)91727-7726
#

# Use a imagem base do Python
FROM python:3.9-slim

# Atualizar e instalar dependências necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    firebird-dev 
    # Substitua 'firebird-client' pelo nome correto do pacote, se necessário


# Limpar os arquivos de listas para reduzir o tamanho da imagem
RUN rm -rf /var/lib/apt/lists/*

# Define the working directory
WORKDIR /app

# Copy only the files necessary for pip install first
# This takes advantage of Docker's layer caching, so rebuilding the image will be faster if these files haven't changed
COPY setup.py ./

# Install the Python dependencies
# --no-cache-dir: Don't store the cache data in Docker layers
RUN pip install --no-cache-dir .

# Now copy the rest of your application source code
COPY source_firebird ./source_firebird
COPY main.py ./

RUN pip install fdb

# Set the environment variable for the Airbyte entrypoint
ENV AIRBYTE_ENTRYPOINT "python /app/main.py"

# Define the entrypoint and default command for the container
ENTRYPOINT ["python", "/app/main.py"]

# Label the image with version and name for better organization
LABEL io.airbyte.version=0.0.1
LABEL io.airbyte.name=lippelima5/source-firebird
