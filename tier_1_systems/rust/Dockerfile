FROM rust:slim AS builder

WORKDIR /app
COPY Cargo.toml .
COPY src/ src/

RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=builder /app/target/release/rust /usr/local/bin/app
CMD ["app"]
