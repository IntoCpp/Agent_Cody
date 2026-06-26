## **Python‑Specific Clean‑Code Rules**

### **1. Pythonic Style & Conventions**
- Follow **PEP 8** for formatting and naming.  
- Use **snake_case** for functions and variables, **PascalCase** for classes, **UPPER_CASE** for constants.  
- Prefer explicit, readable Python over clever tricks or dense one‑liners.

### **2. Docstrings & Type Hints**
- Use **docstrings** (triple‑quoted) for every function and class.  
- Include **type hints** for all parameters and return values.  
- Use `typing` or `collections.abc` types (`list[str]`, `dict[str, int]`, etc.).

### **3. Pythonic Data & Control Flow**
- Prefer **list/dict/set comprehensions** only when they remain readable.  
- Use `enumerate()` and `zip()` instead of manual index handling.  
- Use `with` statements for resource management (files, locks, etc.).

### **4. Imports & Module Organization**
- Keep imports at the top of the file, grouped and ordered.  
- Avoid wildcard imports (`from module import *`).  
- Organize code into modules and packages with clear responsibilities.

### **5. Error Handling (Python‑specific best practices)**
- Catch **specific exceptions**, not bare `except:`.  
- Raise meaningful exceptions using Python’s built‑in hierarchy.  
- Avoid using exceptions for normal control flow.

### **6. Pythonic Data Structures & Idioms**
- Prefer built‑in containers (`list`, `dict`, `set`, `tuple`) over custom structures.  
- Use **generators** when working with large or streaming data.  
- Avoid mutable default arguments (`def f(x=[]):`).

### **7. Modern Python Practices**
- Use **f‑strings** for formatting.  
- Prefer `pathlib` over `os.path`.  
- Use `dataclasses` for simple data containers when appropriate.

