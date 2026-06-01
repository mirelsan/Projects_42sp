*This project has been created as part of the 42 curriculum by <mirelsan>.*

---

# 📚 Libft — Your Very First Own Library

> A complete C library reimplementing standard libc functions, plus additional utilities and linked list manipulation — built entirely from scratch.

---

## 📋 Table of Contents

- [Description](#description)
- [Project Structure](#project-structure)
- [Instructions](#instructions)
- [Functions Reference](#functions-reference)
  - [Part 1 — Libc Functions](#part-1--libc-functions)
  - [Part 2 — Additional Functions](#part-2--additional-functions)
  - [Part 3 — Linked List](#part-3--linked-list)
- [Technical Rules](#technical-rules)
- [Resources](#resources)

---

## Description

**Libft** is the very first project of the 42 curriculum. The goal is to build a personal C library (`libft.a`) from scratch, implementing many of the standard C library functions — as well as additional utility functions that will be reused throughout the entire cursus.

This project teaches:
- How standard C library functions are actually implemented under the hood
- Memory management with `malloc` and `free`
- String manipulation and character classification
- Linked list data structures
- How to compile and archive a static library with `ar`
- How to write clean, Norm-compliant C code

The library is compiled into a static archive `libft.a` that can be linked to any future project.

---

## Project Structure

```
.
├── Makefile
├── libft.h
├── ft_isalpha.c
├── ft_isdigit.c
├── ft_isalnum.c
├── ft_isascii.c
├── ft_isprint.c
├── ft_strlen.c
├── ft_memset.c
├── ft_bzero.c
├── ft_memcpy.c
├── ft_memmove.c
├── ft_strlcpy.c
├── ft_strlcat.c
├── ft_toupper.c
├── ft_tolower.c
├── ft_strchr.c
├── ft_strrchr.c
├── ft_strncmp.c
├── ft_memchr.c
├── ft_memcmp.c
├── ft_strnstr.c
├── ft_atoi.c
├── ft_calloc.c
├── ft_strdup.c
├── ft_substr.c
├── ft_strjoin.c
├── ft_strtrim.c
├── ft_split.c
├── ft_itoa.c
├── ft_strmapi.c
├── ft_striteri.c
├── ft_putchar_fd.c
├── ft_putstr_fd.c
├── ft_putendl_fd.c
├── ft_putnbr_fd.c
├── ft_lstnew.c
├── ft_lstadd_front.c
├── ft_lstsize.c
├── ft_lstlast.c
├── ft_lstadd_back.c
├── ft_lstdelone.c
├── ft_lstclear.c
├── ft_lstiter.c
└── ft_lstmap.c
```

> All files must be placed at the **root** of the repository.

---

## Instructions

### Requirements

- GCC or compatible C compiler
- `make` utility
- UNIX-based system (Linux / macOS)

### Compilation

**Compile the mandatory part:**
```bash
make
```

**Clean object files:**
```bash
make clean
```

**Clean everything (objects + library):**
```bash
make fclean
```

**Recompile from scratch:**
```bash
make re
```

### Linking to your project

After compiling, link `libft.a` in your own project:

```bash
gcc -Wall -Wextra -Werror your_file.c -L. -lft -o your_program
```

Or, if your project has a `libft/` folder:
```bash
gcc -Wall -Wextra -Werror your_file.c -L./libft -lft -o your_program
```

Don't forget to include the header:
```c
#include "libft.h"
```

### Makefile Rules

| Rule | Description |
|------|-------------|
| `$(NAME)` | Compiles `libft.a` |
| `all` | Same as `$(NAME)` |
| `clean` | Removes `.o` object files |
| `fclean` | Removes `.o` files and `libft.a` |
| `re` | Runs `fclean` then `all` |

> The Makefile uses `ar` to create the static library. `libtool` is **not** used.  
> Compilation flags: `-Wall -Wextra -Werror`

---

## Functions Reference

### Part 1 — Libc Functions

Reimplementations of standard C library functions, prefixed with `ft_`.

> **Note:** The `restrict` keyword (C99) is **not** used in any prototype, and `-std=c99` flag is not used.

#### Character Classification

For all classification functions below, the return value is:
- `1` if the character matches the tested class
- `0` if it does not match

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_isalpha` | `int ft_isalpha(int c)` | Returns 1 if `c` is an alphabetic character (a–z or A–Z) |
| `ft_isdigit` | `int ft_isdigit(int c)` | Returns 1 if `c` is a decimal digit (0–9) |
| `ft_isalnum` | `int ft_isalnum(int c)` | Returns 1 if `c` is alphanumeric (letter or digit) |
| `ft_isascii` | `int ft_isascii(int c)` | Returns 1 if `c` is a valid ASCII character (0–127) |
| `ft_isprint` | `int ft_isprint(int c)` | Returns 1 if `c` is a printable character (32–126) |

#### Character Conversion

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_toupper` | `int ft_toupper(int c)` | Converts a lowercase letter to uppercase; returns `c` unchanged if not a lowercase letter |
| `ft_tolower` | `int ft_tolower(int c)` | Converts an uppercase letter to lowercase; returns `c` unchanged if not an uppercase letter |

#### String Functions

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_strlen` | `size_t ft_strlen(const char *s)` | Returns the number of characters in string `s`, not counting the null terminator |
| `ft_strlcpy` | `size_t ft_strlcpy(char *dst, const char *src, size_t size)` | Copies up to `size - 1` characters from `src` to `dst`, always null-terminating. Returns the length of `src` |
| `ft_strlcat` | `size_t ft_strlcat(char *dst, const char *src, size_t size)` | Appends `src` to `dst`, ensuring the result is null-terminated within `size` bytes. Returns `strlen(dst) + strlen(src)` |
| `ft_strchr` | `char *ft_strchr(const char *s, int c)` | Locates the first occurrence of character `c` in string `s`. Returns a pointer to it, or `NULL` if not found |
| `ft_strrchr` | `char *ft_strrchr(const char *s, int c)` | Locates the **last** occurrence of character `c` in string `s`. Returns a pointer to it, or `NULL` if not found |
| `ft_strncmp` | `int ft_strncmp(const char *s1, const char *s2, size_t n)` | Compares at most `n` characters of `s1` and `s2`. Returns 0 if equal, positive or negative otherwise |
| `ft_strnstr` | `char *ft_strnstr(const char *haystack, const char *needle, size_t len)` | Finds the first occurrence of `needle` in `haystack`, searching at most `len` characters. Returns a pointer to the match, or `NULL` |
| `ft_strdup` | `char *ft_strdup(const char *s)` | Allocates memory and returns a duplicate of string `s`. Returns `NULL` on allocation failure |

#### Memory Functions

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_memset` | `void *ft_memset(void *b, int c, size_t len)` | Fills the first `len` bytes of memory area `b` with the byte value `c`. Returns `b` |
| `ft_bzero` | `void ft_bzero(void *s, size_t n)` | Sets the first `n` bytes of `s` to zero |
| `ft_memcpy` | `void *ft_memcpy(void *dst, const void *src, size_t n)` | Copies `n` bytes from `src` to `dst`. Behavior is undefined if areas overlap |
| `ft_memmove` | `void *ft_memmove(void *dst, const void *src, size_t len)` | Copies `len` bytes from `src` to `dst`. Safe even if memory areas overlap |
| `ft_memchr` | `void *ft_memchr(const void *s, int c, size_t n)` | Searches the first `n` bytes of `s` for byte `c`. Returns a pointer to the match or `NULL` |
| `ft_memcmp` | `int ft_memcmp(const void *s1, const void *s2, size_t n)` | Compares the first `n` bytes of `s1` and `s2`. Returns 0 if equal, otherwise the difference of the first differing bytes |

#### Conversion

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_atoi` | `int ft_atoi(const char *str)` | Converts the string `str` to an integer, skipping leading whitespace and handling optional sign (`+`/`-`) |

#### Memory Allocation

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_calloc` | `void *ft_calloc(size_t nmemb, size_t size)` | Allocates memory for an array of `nmemb` elements of `size` bytes each and initializes all bytes to zero. If `nmemb` or `size` is 0, returns a unique pointer that can be passed to `free()` |

---

### Part 2 — Additional Functions

Functions not present in the standard libc, or present in a different form.

#### String Utilities

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_substr` | `char *ft_substr(char const *s, unsigned int start, size_t len)` | Allocates and returns a substring of `s` starting at index `start` with a maximum length of `len`. Returns `NULL` on allocation failure |
| `ft_strjoin` | `char *ft_strjoin(char const *s1, char const *s2)` | Allocates and returns a new string that is the concatenation of `s1` and `s2`. Returns `NULL` on allocation failure |
| `ft_strtrim` | `char *ft_strtrim(char const *s1, char const *set)` | Allocates and returns a copy of `s1` with all characters in `set` removed from both the beginning and the end. Returns `NULL` on allocation failure |
| `ft_split` | `char **ft_split(char const *s, char c)` | Allocates and returns a NULL-terminated array of strings obtained by splitting `s` using `c` as a delimiter. Each substring is independently allocated. Returns `NULL` if any allocation fails |
| `ft_itoa` | `char *ft_itoa(int n)` | Allocates and returns a string representing the integer `n`. Handles negative numbers. Returns `NULL` on allocation failure |

#### String Iteration

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_strmapi` | `char *ft_strmapi(char const *s, char (*f)(unsigned int, char))` | Applies function `f` to each character of `s`, passing the index and the character. Returns a new string built from the results. Returns `NULL` on allocation failure |
| `ft_striteri` | `void ft_striteri(char *s, void (*f)(unsigned int, char*))` | Applies function `f` to each character of `s` **in place**, passing its index and a pointer to the character (allowing modification) |

#### File Descriptor Output

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_putchar_fd` | `void ft_putchar_fd(char c, int fd)` | Outputs character `c` to file descriptor `fd` |
| `ft_putstr_fd` | `void ft_putstr_fd(char *s, int fd)` | Outputs string `s` to file descriptor `fd` |
| `ft_putendl_fd` | `void ft_putendl_fd(char *s, int fd)` | Outputs string `s` followed by a newline (`\n`) to file descriptor `fd` |
| `ft_putnbr_fd` | `void ft_putnbr_fd(int n, int fd)` | Outputs integer `n` to file descriptor `fd` |

> Common file descriptors: `0` = stdin, `1` = stdout, `2` = stderr.

---

### Part 3 — Linked List

Implementation of linked list manipulation functions using the following structure, declared in `libft.h`:

```c
typedef struct s_list
{
    void            *content;
    struct s_list   *next;
}   t_list;
```

**Fields:**
- `content` — a `void *` that can hold any type of data
- `next` — pointer to the next node, or `NULL` if it is the last node

[text](libft.h)
#### Linked List Functions

| Function | Prototype | Description |
|----------|-----------|-------------|
| `ft_lstnew` | `t_list *ft_lstnew(void *content)` | Allocates and returns a new node. `content` is set to the given parameter, `next` is initialized to `NULL` |
| `ft_lstadd_front` | `void ft_lstadd_front(t_list **lst, t_list *new)` | Inserts node `new` at the **beginning** of the list pointed to by `lst` |
| `ft_lstsize` | `int ft_lstsize(t_list *lst)` | Counts and returns the number of nodes in the list |
| `ft_lstlast` | `t_list *ft_lstlast(t_list *lst)` | Returns a pointer to the **last** node of the list |
| `ft_lstadd_back` | `void ft_lstadd_back(t_list **lst, t_list *new)` | Inserts node `new` at the **end** of the list pointed to by `lst` |
| `ft_lstdelone` | `void ft_lstdelone(t_list *lst, void (*del)(void *))` | Frees the content of node `lst` using `del`, then frees the node itself. Does **not** free the next node |
| `ft_lstclear` | `void ft_lstclear(t_list **lst, void (*del)(void *))` | Deletes and frees all nodes in the list starting from `lst`, using `del` to free each node's content. Sets the list pointer to `NULL` |
| `ft_lstiter` | `void ft_lstiter(t_list *lst, void (*f)(void *))` | Iterates through the list and applies function `f` to the `content` of each node |
| `ft_lstmap` | `t_list *ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))` | Creates a new list by applying `f` to the `content` of each node in `lst`. If an allocation fails, `del` is used to clean up and `NULL` is returned |

---

## Technical Rules

These constraints apply to the entire project:

- Written in **C** only
- Must follow **42 Norm** (style rules) — norm errors result in grade 0
- **No global variables** allowed
- Helper/internal functions must be declared as `static`
- No unexpected exits (no segfaults, bus errors, double frees, etc.)
- **No memory leaks** — all heap-allocated memory must be freed
- Library is created using the `ar` command — `libtool` is **forbidden**
- The `libft.a` archive must be generated at the **root** of the repository
- All `.c` files must compile cleanly with `-Wall -Wextra -Werror`
- The `restrict` qualifier and `-std=c99` flag are **forbidden**
- Unused files must **not** be submitted

---

## Resources

### Official Documentation
- [C Standard Library Reference — cppreference.com](https://en.cppreference.com/w/c)
- [Linux Man Pages — man7.org](https://man7.org/linux/man-pages/)
- [GNU C Library (glibc) Reference](https://www.gnu.org/software/libc/manual/)

### Articles & Guides
- [Understanding Static Libraries in C](https://www.cs.cmu.edu/afs/cs/academic/class/15213-f00/docs/elf.pdf)
- [Memory Management in C — malloc, calloc, free](https://www.tutorialspoint.com/c_standard_library/c_function_malloc.htm)
- [Linked Lists in C — Explained](https://www.learn-c.org/en/Linked_lists)
- [The Difference Between glibc and BSD libc](https://wiki.musl-libc.org/functional-differences-from-glibc.html)
- [strlcpy and strlcat — why they exist](https://www.sudo.ws/posts/2019/04/differing-views-on-strlcpy/)

### Testing Tools
- [Francinette — popular 42 Libft tester](https://github.com/xicodomingues/francinette)
- [libft-unit-test](https://github.com/alelievr/libft-unit-test)
- [42TESTERS-LIBFT](https://github.com/Tripouille/libftTester)

### AI Usage
AI was used in this project in the following ways:
- **Understanding concepts**: asking for explanations of memory management, pointer arithmetic, and undefined behavior cases
- **Clarifying man page behavior**: asking about edge cases (e.g., `calloc` with `size = 0`, `memmove` with overlapping regions)
- **README writing**: assisting in structuring and formatting this documentation

> Direct code generation by AI was **avoided** in order to build genuine understanding of each function, in compliance with the AI guidelines of the 42 curriculum.
