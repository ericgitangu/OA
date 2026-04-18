FROM gcc:14-bookworm AS builder

RUN apt-get update && apt-get install -y cmake && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY CMakeLists.txt .
COPY src/ src/

RUN cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build

FROM debian:bookworm-slim
COPY --from=builder /app/build/main /usr/local/bin/main
CMD ["main"]
