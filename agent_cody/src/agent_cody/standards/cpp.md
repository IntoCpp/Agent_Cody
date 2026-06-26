# C++ Coding Standards

## **C++‑Specific Clean‑Code Rules**

### **1. Memory & Resource Safety**
- Prefer **RAII** for all resources (memory, files, locks, sockets).  
- Avoid raw pointers unless absolutely necessary; prefer **smart pointers** (`std::unique_ptr`, `std::shared_ptr`).  
- Never use `new`/`delete` directly unless the example explicitly requires it.

### **2. Modern C++ Practices**
- Use **modern C++ (C++17 or later)** idioms:  
  - `auto` only when it improves clarity  
  - `constexpr` where appropriate  
  - `enum class` instead of plain enums  
  - `override` for virtual functions  
- Prefer **`std::vector`** and other STL containers over manual arrays.

### **3. Error Handling**
- Use **exceptions** for error handling, not return codes.  
- Never throw raw strings; throw **typed exceptions**.  
- Catch exceptions by **const reference**.

### **4. Const‑Correctness**
- Use `const` everywhere it applies:  
  - parameters  
  - methods  
  - local variables  
  - references and pointers  
- Prefer passing large objects as `const &`.

### **5. Header & Source Organization**
- Keep headers clean:  
  - No implementation in headers unless templates  
  - Use `#pragma once`  
  - Minimize includes; prefer forward declarations  
- Separate interface (`.h`) and implementation (`.cpp`) unless trivial.

### **6. Namespaces & Structure**
- Wrap code in **namespaces** with meaningful names.  
- Avoid `using namespace std;` — never use it in headers.

### **7. Performance & Safety**
- Avoid unnecessary copies; use **move semantics** when appropriate.  
- Prefer **range‑based for loops** (with comments, per your global rules).  
- Avoid undefined behavior at all costs.

### **8. Comments & Documentation (C++‑specific nuance)**
- Document ownership semantics when using pointers.  
- Document thread‑safety assumptions when relevant.  
- Document complexity when it matters (e.g., O(n²) loops).

---