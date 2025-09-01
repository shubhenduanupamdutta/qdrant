# Python Developer's Guide to Qdrant Rust Codebase

## Rust Concepts for Python Developers

### Key Differences from Python

| Python            | Rust                                | Purpose                     |
| ----------------- | ----------------------------------- | --------------------------- |
| `import module`   | `use module::item;`                 | Bringing items into scope   |
| `def function():` | `fn function() {`                   | Function definition         |
| `class MyClass:`  | `struct MyStruct` / `impl MyStruct` | Data structures and methods |
| `try/except`      | `Result<T, E>` / `?` operator       | Error handling              |
| `None`            | `Option<T>` / `None`                | Nullable values             |
| `async def`       | `async fn`                          | Async functions             |
| `list[int]`       | `Vec<i32>`                          | Dynamic arrays              |
| `dict[str, int]`  | `HashMap<String, i32>`              | Hash maps                   |

### Memory Management

- **Python**: Garbage collected, references everywhere
- **Rust**: Ownership system, no garbage collector
- **Key concept**: Each value has exactly one owner

```rust
// Python equivalent: data = [1, 2, 3]
let data = vec![1, 2, 3];  // data owns the vector

// Python equivalent: data2 = data (both reference same object)
let data2 = data;  // data is MOVED to data2, data is no longer valid

// To have multiple references, use borrowing:
let data = vec![1, 2, 3];
let data_ref = &data;  // Borrowing, doesn't take ownership
```

## Qdrant-Specific Rust Patterns

### 1. Error Handling with `OperationResult<T>`

```rust
// Python equivalent:
// def create_collection(name: str) -> Collection:
//     if invalid_name(name):
//         raise ValueError("Invalid name")
//     return Collection(name)

fn create_collection(name: String) -> OperationResult<Collection> {
    if name.is_empty() {
        return Err(OperationError::ValidationError("Invalid name".into()));
    }
    Ok(Collection::new(name))
}

// Using the result (Python: try/except)
match create_collection("test".to_string()) {
    Ok(collection) => println!("Created: {:?}", collection),
    Err(error) => println!("Error: {:?}", error),
}

// Or use the ? operator for early return
fn some_operation() -> OperationResult<()> {
    let collection = create_collection("test".to_string())?;  // Returns error if fails
    // Continue with collection...
    Ok(())
}
```

### 2. Async/Await Patterns

```rust
// Python equivalent:
// async def search_vectors(query: Vector) -> List[SearchResult]:
//     async with database.transaction():
//         return await index.search(query)

async fn search_vectors(query: Vector) -> OperationResult<Vec<SearchResult>> {
    let transaction = database.begin_transaction().await?;
    let results = index.search(query).await?;
    transaction.commit().await?;
    Ok(results)
}
```

### 3. Trait System (Like Python Protocols/ABC)

```rust
// Python equivalent:
// class VectorStorage(Protocol):
//     def store_vector(self, id: int, vector: Vector) -> None: ...
//     def get_vector(self, id: int) -> Optional[Vector]: ...

trait VectorStorage {
    fn store_vector(&mut self, id: PointOffsetType, vector: VectorRef) -> OperationResult<()>;
    fn get_vector(&self, id: PointOffsetType) -> Option<CowVector>;
}

// Implementation (like inheriting from ABC)
impl VectorStorage for SimpleVectorStorage {
    fn store_vector(&mut self, id: PointOffsetType, vector: VectorRef) -> OperationResult<()> {
        // Implementation here
    }

    fn get_vector(&self, id: PointOffsetType) -> Option<CowVector> {
        // Implementation here
    }
}
```

## Common Qdrant Code Patterns

### 1. Vector Operations

```rust
// Working with vectors (similar to NumPy arrays)
let vector: Vec<f32> = vec![0.1, 0.2, 0.3, 0.4];
let vector_ref = VectorRef::Dense(&vector);

// Distance calculation
let distance = Distance::Cosine;
let similarity = distance.similarity(&vector1, &vector2);

// Vector storage
let storage = VectorStorageEnum::DenseSimple(simple_storage);
storage.insert_vector(point_id, vector_ref, &hw_counter)?;
```

### 2. Collection Operations

```rust
// Python equivalent: collection.add_points(points)
let points = vec![
    PointStruct {
        id: 1.into(),
        vector: vector_data.into(),
        payload: Some(payload),
    },
];

collection.upsert_points(points).await?;

// Search operation
let search_request = SearchRequest {
    vector: query_vector.into(),
    filter: Some(filter),
    limit: 10,
    ..Default::default()
};

let results = collection.search(search_request).await?;
```

### 3. Concurrent Operations

```rust
// Python equivalent: asyncio.gather(*tasks)
use futures::future::join_all;

let tasks = collections.iter().map(|collection| {
    async move {
        collection.optimize().await
    }
});

let results = join_all(tasks).await;
```

## Key Files for Python Developers

### Start Here (Familiar Territory)

1. **`lib/api/src/grpc/qdrant.proto`** - API definitions (like Python dataclasses)
2. **`tests/integration-tests.sh`** - Integration tests (like pytest)
3. **`config/config.yaml`** - Configuration (like Python config files)

### Core Logic (Business Logic)

4. **`lib/collection/src/operations/`** - Collection operations (like Python service classes)
5. **`lib/segment/src/types.rs`** - Data types (like Python models/dataclasses)
6. **`lib/storage/src/content_manager/`** - Storage management (like Python DAOs)

### API Layer (Web Framework)

7. **`src/actix/`** - REST API (like FastAPI/Flask routes)
8. **`src/tonic/`** - gRPC API (like gRPC Python service)

## Development Workflow

### 1. Setting Up (Python equivalent: pip install -e .)

```bash
# Install Rust development tools
rustup component add rustfmt clippy

# Build project
cargo build

# Run tests (like pytest)
cargo test

# Run specific test module
cargo test collection
```

### 2. Code Quality (Python equivalent: black, pylint, mypy)

```bash
# Format code (like black)
cargo +nightly fmt --all

# Lint code (like pylint/flake8)
cargo clippy --workspace --all-features

# Check without building (like mypy --no-error-summary)
cargo check
```

### 3. Debugging and Development

```bash
# Run with debug output (like python -v)
RUST_LOG=debug cargo run

# Generate documentation (like sphinx)
cargo doc --open

# Profile performance (like cProfile)
cargo bench
```

## Common Tasks for Python Developers

### Adding a New API Endpoint

1. **Define the API** (like defining Pydantic models):

```rust
// In lib/api/src/grpc/qdrant.proto
message NewFeatureRequest {
    string collection_name = 1;
    // ... other fields
}
```

2. **Implement the handler** (like FastAPI route handler):

```rust
// In src/actix/mod.rs or appropriate module
async fn new_feature_handler(
    request: web::Json<NewFeatureRequest>,
    collection_manager: web::Data<Arc<CollectionManager>>,
) -> impl Responder {
    match collection_manager.new_feature(request.into_inner()).await {
        Ok(result) => HttpResponse::Ok().json(result),
        Err(error) => HttpResponse::BadRequest().json(error),
    }
}
```

### Adding Tests

```rust
// Unit tests (like unittest)
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]  // Like @pytest.mark.asyncio
    async fn test_new_feature() {
        let collection = create_test_collection().await;
        let result = collection.new_feature().await;
        assert!(result.is_ok());
    }
}
```

### Working with Async Code

```rust
// Python equivalent:
// async def process_collections():
//     for collection in collections:
//         await collection.process()

async fn process_collections(collections: Vec<Collection>) -> OperationResult<()> {
    for collection in collections {
        collection.process().await?;
    }
    Ok(())
}
```

## Rust Learning Path for Python Developers

1. **Week 1**: Basic syntax, ownership, borrowing

   - The Rust Book chapters 1-4
   - Practice with simple examples

2. **Week 2**: Error handling, traits, generics

   - The Rust Book chapters 6, 9-10
   - Study Qdrant's error types

3. **Week 3**: Async programming, concurrency

   - Async Rust book
   - Study Qdrant's async patterns

4. **Week 4**: Advanced features, macros
   - The Rust Book chapters 13, 19
   - Contribute to Qdrant!

## Quick Reference: Python → Rust

```python
# Python
def calculate_distance(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2):
        raise ValueError("Vectors must have same length")

    result = 0.0
    for a, b in zip(v1, v2):
        result += (a - b) ** 2

    return result ** 0.5
```

```rust
// Rust equivalent
fn calculate_distance(v1: &[f32], v2: &[f32]) -> OperationResult<f32> {
    if v1.len() != v2.len() {
        return Err(OperationError::ValidationError(
            "Vectors must have same length".into()
        ));
    }

    let result: f32 = v1.iter()
        .zip(v2.iter())
        .map(|(a, b)| (a - b).powi(2))
        .sum();

    Ok(result.sqrt())
}
```

The key insight: Rust is more explicit about memory management and error handling, but the core logic remains similar to Python!
