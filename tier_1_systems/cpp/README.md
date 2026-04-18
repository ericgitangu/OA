# Tier 1 — C++ (Modern C++20/23)

## Build

```bash
cmake -B build && cmake --build build
./build/main
```

## Docker

```bash
docker build -t tier1-cpp .
docker run tier1-cpp
```

## Focus Areas
- RAII and move semantics
- Templates and concepts (C++20)
- Ranges library
- std::format, std::expected
- Comparison with Rust ownership model
