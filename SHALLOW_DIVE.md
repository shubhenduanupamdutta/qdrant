# Qdrant Shallow Dive Guide 🚀

Welcome to your guide for understanding Qdrant! This document provides a comprehensive overview of the project architecture, key concepts, and a step-by-step approach to exploring the codebase.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Core Architecture](#core-architecture)
3. [Key Components](#key-components)
4. [Technology Stack](#technology-stack)
5. [Development Environment Setup](#development-environment-setup)
6. [Codebase Exploration Guide](#codebase-exploration-guide)
7. [Contributing Areas](#contributing-areas)
8. [Learning Resources](#learning-resources)

## Project Overview

**Qdrant** is a high-performance vector similarity search engine and vector database written in Rust. It's designed to handle large-scale vector operations with advanced filtering capabilities, making it ideal for AI applications, recommendation systems, and semantic search.

### What makes Qdrant special?

- **Production-ready**: Built for high-load scenarios with reliability in mind
- **Advanced filtering**: Supports complex payload-based filtering alongside vector similarity
- **Hybrid search**: Combines dense and sparse vectors for better search quality
- **Distributed**: Horizontal scaling through sharding and replication
- **Memory efficient**: Vector quantization reduces RAM usage by up to 97%

### Key Use Cases

- Semantic text search
- Image similarity search
- Recommendation engines
- Anomaly detection
- Chat bots and QA systems
- RAG (Retrieval Augmented Generation) pipelines

## Core Architecture

Qdrant follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│               API Layer                 │
│        (REST + gRPC interfaces)        │
├─────────────────────────────────────────┤
│             Storage Layer               │
│    (Collections, Shards, Segments)     │
├─────────────────────────────────────────┤
│            Vector Storage               │
│   (Dense/Sparse/Multi vectors + HNSW)  │
├─────────────────────────────────────────┤
│             Consensus                   │
│        (Raft-based clustering)         │
└─────────────────────────────────────────┘
```

### Core Concepts

1. **Points**: Basic data units containing vectors and optional payload
2. **Collections**: Named groups of points with specific vector configurations
3. **Segments**: Storage units within collections for efficient search
4. **Shards**: Horizontal partitions for distributed deployment
5. **Vector Storage**: Different storage backends optimized for various use cases

## Key Components

### 1. Library Structure (`lib/`)

- **`api/`**: gRPC and API definitions
- **`collection/`**: Collection management and operations
- **`segment/`**: Core vector storage and indexing
- **`storage/`**: Persistence and storage management
- **`common/`**: Shared utilities and data types
- **`sparse/`**: Sparse vector implementations
- **`quantization/`**: Vector compression techniques

### 2. Main Application (`src/`)

- **`main.rs`**: Application entry point and initialization
- **`consensus.rs`**: Raft consensus implementation
- **`actix/`**: REST API server implementation
- **`tonic/`**: gRPC server implementation
- **`common/`**: Application-level utilities

### 3. Vector Storage Types

- **Dense vectors**: Traditional embeddings (float32/float16/int8)
- **Sparse vectors**: BM25-like representations for keyword search
- **Multi-vectors**: Multiple vectors per point for complex representations

### 4. Storage Backends

- **Simple**: RocksDB-based storage
- **Mmap**: Memory-mapped files for better performance
- **Volatile**: In-memory storage for testing/prototyping

## Technology Stack

### Core Technologies

- **Rust**: Primary language (edition 2024, min version 1.88)
- **Tokio**: Async runtime for concurrency
- **RocksDB**: Persistent storage backend
- **Raft**: Consensus algorithm for distributed deployment

### Key Dependencies

- **HNSW**: Hierarchical Navigable Small World for vector indexing
- **SIMD**: Hardware acceleration for vector operations
- **Serde**: Serialization/deserialization
- **Tonic**: gRPC implementation
- **Actix-web**: REST API framework

### Vector Processing

- **Distance metrics**: Cosine, Euclidean, Dot product, Manhattan
- **Quantization**: Scalar, Product, Binary quantization
- **Indexing**: HNSW, filtered search optimization

## Development Environment Setup

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install required toolchain
rustup install nightly
rustup component add rustfmt clippy
```

### Building Qdrant

```bash
# Clone the repository
git clone https://github.com/qdrant/qdrant.git
cd qdrant

# Build in development mode
cargo build

# Build optimized release
cargo build --release

# Run tests
cargo test

# Check code style
cargo +nightly fmt --all
cargo clippy --workspace --all-features
```

### Running Qdrant

```bash
# Run locally
cargo run

# With custom config
cargo run -- --config-path ./config/development.yaml

# Using Docker
docker build . --tag=qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant
```

## Codebase Exploration Guide

Follow this step-by-step approach to understand Qdrant's codebase:

### Phase 1: High-Level Understanding (1-2 days)

1. **Start with documentation**

   - Read `README.md` thoroughly
   - Review `docs/QUICK_START.md`
   - Study `docs/DEVELOPMENT.md`

2. **Explore the main entry point**

   - `src/main.rs`: Application startup and initialization
   - `src/settings.rs`: Configuration management
   - `src/startup.rs`: Service startup logic

3. **Understand the API layer**
   - `src/actix/mod.rs`: REST API implementation
   - `src/tonic/mod.rs`: gRPC API implementation
   - `lib/api/`: API definitions and data structures

### Phase 2: Core Storage Architecture (2-3 days)

4. **Collection management**

   - `lib/collection/src/collection/mod.rs`: Collection operations
   - `lib/collection/src/shards/`: Sharding implementation
   - `lib/storage/src/content_manager/`: Storage orchestration

5. **Segment architecture**

   - `lib/segment/src/segment.rs`: Segment interface
   - `lib/segment/src/entry/`: Segment entry points
   - `lib/segment/src/types.rs`: Core data types

6. **Vector storage implementations**
   - `lib/segment/src/vector_storage/vector_storage_base.rs`: Storage abstractions
   - `lib/segment/src/vector_storage/dense/`: Dense vector storage
   - `lib/segment/src/vector_storage/sparse/`: Sparse vector storage

### Phase 3: Search and Indexing (2-3 days)

7. **HNSW indexing**

   - `lib/segment/src/index/hnsw_index/`: HNSW implementation
   - `lib/segment/src/index/query_optimization/`: Query optimization
   - `lib/segment/src/index/struct_payload_index/`: Payload indexing

8. **Search algorithms**
   - `lib/segment/src/vector_storage/query/`: Query implementations
   - `lib/segment/src/index/field_index/`: Field-based filtering
   - `lib/collection/src/collection_manager/`: Search orchestration

### Phase 4: Advanced Features (2-3 days)

9. **Consensus and clustering**

   - `src/consensus.rs`: Raft consensus implementation
   - `lib/storage/src/content_manager/consensus/`: Consensus operations
   - `lib/collection/src/shards/replica_set.rs`: Replica management

10. **Quantization and optimization**
    - `lib/quantization/`: Vector quantization implementations
    - `lib/segment/src/vector_storage/chunked_vector_storage.rs`: Chunked storage
    - Memory mapping and optimization techniques

### Phase 5: Testing and Integration (1-2 days)

11. **Test structure**

    - `tests/`: Integration tests
    - Unit tests within each module
    - Benchmarks in `lib/segment/benches/`

12. **Configuration and deployment**
    - `config/`: Configuration files
    - `tools/`: Deployment and utility scripts
    - Docker and deployment considerations

## Contributing Areas

Based on your Python background and intermediate Rust knowledge, here are excellent areas to contribute:

### 🟢 **Beginner-friendly (Python knowledge helpful)**

- **Documentation improvements**: API docs, examples, tutorials
- **Python client testing**: Integration tests with Python client
- **Configuration validation**: Improve config parsing and validation
- **Monitoring and metrics**: Add new telemetry points
- **Docker and deployment**: Improve containerization

### 🟡 **Intermediate (Good Rust practice)**

- **Payload indexing**: Improve filtering performance
- **Error handling**: Better error messages and recovery
- **Memory optimization**: Reduce allocations in hot paths
- **API enhancements**: New REST endpoints or gRPC services
- **Testing infrastructure**: More comprehensive test coverage

### 🔴 **Advanced (Deep Rust + domain knowledge)**

- **Vector algorithms**: New distance metrics or quantization methods
- **HNSW optimizations**: Performance improvements in indexing
- **Consensus improvements**: Raft protocol enhancements
- **Storage backends**: New storage implementations
- **SIMD optimizations**: Hardware acceleration improvements

### Areas with TODOs (Good starting points)

The codebase contains many `TODO` comments. Search for them using:

```bash
grep -r "TODO\|FIXME" --include="*.rs" src/ lib/
```

## Learning Resources

### Rust Learning

- **The Rust Programming Language**: https://doc.rust-lang.org/book/
- **Rust by Example**: https://doc.rust-lang.org/rust-by-example/
- **Async Rust**: https://rust-lang.github.io/async-book/
- **Rust Performance Book**: https://nnethercote.github.io/perf-book/

### Vector Databases and Search

- **Vector Database Fundamentals**: https://www.pinecone.io/learn/vector-database/
- **HNSW Algorithm**: https://arxiv.org/abs/1603.09320
- **Vector Similarity Search**: https://erikbern.com/2015/10/01/nearest-neighbors-and-vector-models-part-2-how-to-search-in-high-dimensional-spaces.html

### Distributed Systems

- **Raft Consensus**: https://raft.github.io/
- **Distributed Systems Course (MIT)**: https://www.youtube.com/playlist?list=PLrw6a1wE39_tb2fErI4-WkMbsvGQk9_UB
- **Designing Data-Intensive Applications**: Book by Martin Kleppmann

### Vector Search Concepts

- **Embedding Models**: https://huggingface.co/blog/sentence-transformers
- **Similarity Metrics**: https://www.pinecone.io/learn/vector-similarity/
- **Quantization Techniques**: https://www.pinecone.io/learn/vector-quantization/

### Qdrant-Specific Resources

- **Official Documentation**: https://qdrant.tech/documentation/
- **Qdrant Blog**: https://qdrant.tech/articles/
- **Community Discord**: https://discord.gg/tdtYvXjC4h
- **YouTube Channel**: https://www.youtube.com/@qdrant
- **Colab Tutorials**: https://colab.research.google.com/drive/1Bz8RSVHwnNDaNtDwotfPj0w7AYzsdXZ-

### Performance and Optimization

- **Rust Performance Tips**: https://gist.github.com/jFransham/369a86eff00e5f280ed25121454acec1
- **SIMD in Rust**: https://rust-lang.github.io/packed_simd/perf-guide/
- **Memory-mapped Files**: https://en.wikipedia.org/wiki/Memory-mapped_file

## Next Steps

1. **Set up the development environment** and build Qdrant successfully
2. **Run the test suite** to understand the testing approach
3. **Pick a small issue** from GitHub issues labeled "good first issue"
4. **Read the contributing guidelines** in `docs/CONTRIBUTING.md`
5. **Join the community** on Discord for questions and discussions
6. **Start with documentation** or testing contributions before diving into core algorithms

## Quick Reference Commands

```bash
# Development workflow
cargo check                    # Fast compilation check
cargo test                     # Run all tests
cargo test segment            # Run specific test module
cargo bench                   # Run benchmarks
cargo doc --open              # Generate and open docs

# Code quality
cargo +nightly fmt --all      # Format code
cargo clippy --all-features   # Lint code
cargo audit                   # Security audit

# Docker workflow
docker build . -t qdrant      # Build container
docker run -p 6333:6333 qdrant # Run container

# Useful searches
grep -r "TODO" src/ lib/       # Find contribution opportunities
find . -name "*.rs" | head -20 # List Rust files
```

Remember: The best way to learn is by doing! Start small, ask questions, and gradually work your way up to more complex contributions. The Qdrant community is welcoming and helpful for new contributors.

Happy coding! 🦀✨
