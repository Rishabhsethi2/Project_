# 1. The Base Image
FROM python:3.12-slim

# 2. Environment & Memory Optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Security: User Namespaces
RUN useradd -m -r quantdev
USER quantdev

# 4. The Mount Point
WORKDIR /app

# 5. Layer Caching
COPY --chown=quantdev:quantdev requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Source Code Injection
COPY --chown=quantdev:quantdev . .