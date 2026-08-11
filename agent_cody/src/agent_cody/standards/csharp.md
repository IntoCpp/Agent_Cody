# C# Coding Standards

## **C#-Specific Clean-Code Rules**

### **1. Naming and API Design**
- Follow standard .NET naming conventions.
- Use **PascalCase** for namespaces, types, methods, properties, events, and public constants.
- Use **camelCase** for parameters and local variables, and **_camelCase** for private instance fields.
- Prefix interfaces with `I`; do not use Hungarian notation or encode types in names.
- Give asynchronous methods an `Async` suffix unless they implement an existing contract with a different name.

### **2. Modern C# Practices**
- Use modern C# and .NET features supported by the target project; avoid obsolete APIs and outdated constructs.
- Prefer file-scoped namespaces when a file contains a single namespace.
- Place `using` directives outside namespace declarations and remove unused directives.
- Use `var` only when the type is obvious from the right-hand side or when required for anonymous types.
- Prefer C# keywords such as `string`, `int`, and `bool` over `System.String`, `System.Int32`, and `System.Boolean`.

### **3. Null Safety and Type Design**
- Enable and respect nullable reference types; handle possible `null` values explicitly.
- Avoid the null-forgiving operator (`!`) unless the invariant is clear and justified.
- Prefer immutable data where practical, using `record`, `init`, and `readonly` appropriately.
- Choose `class`, `record`, `struct`, and `record struct` according to their value/reference semantics; avoid large mutable structs.

### **4. Resource and Memory Safety**
- Dispose of `IDisposable` and `IAsyncDisposable` resources with `using` or `await using`.
- Implement the dispose pattern only when a type directly owns disposable resources.
- Avoid unnecessary allocations and copies, but do not sacrifice clarity for speculative optimization.

### **5. Exceptions and Validation**
- Throw the most specific appropriate exception and include a meaningful message.
- Validate public method arguments early, using guard clauses such as `ArgumentNullException.ThrowIfNull`.
- Catch only exceptions that can be handled meaningfully; never swallow exceptions or use exceptions for normal control flow.
- Preserve the original stack trace by using `throw;` when rethrowing.

### **6. Asynchronous and Concurrent Code**
- Use `async` and `await` for I/O-bound work; avoid blocking with `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()`.
- Return `Task` or `Task<T>` from asynchronous methods; use `async void` only for event handlers.
- Accept and propagate `CancellationToken` for cancellable operations.
- Document thread-safety expectations when a type can be used concurrently.

### **7. Collections, LINQ, and Control Flow**
- Program against the narrowest useful collection abstraction, such as `IReadOnlyList<T>` or `IEnumerable<T>`.
- Use LINQ when it improves readability; avoid long query chains with hidden repeated enumeration or side effects.
- Prefer guard clauses and pattern matching when they make control flow clearer.
- Do not expose mutable collections directly unless callers are intentionally allowed to modify them.

### **8. Formatting and Documentation**
- Use four spaces for indentation and the **Allman** brace style.
- Write one statement and one declaration per line.
- Use XML documentation comments for public APIs, including parameters, return values, exceptions, and important behavior.
- Keep comments focused on intent, invariants, ownership, and non-obvious decisions rather than restating the code.

---
