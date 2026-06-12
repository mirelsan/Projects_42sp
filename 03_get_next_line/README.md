*This project has been created as part of the 42 curriculum by mirelsan*

# get_next_line

## Description

This project implements `get_next_line`, a function that reads a file descriptor line by line. Its goal is to return the next line from the input each time the function is called, handling partial reads and preserving the remaining content between calls.

The implementation uses a static buffer called `stash` to store unread data that was already read but not yet returned. This allows the function to return one line at a time without losing data when a buffer read contains more than one line.

## Algorithm and Justification

The selected algorithm is a read-append-extract loop with a persistent stash:

1. Call `get_next_line(int fd)`.
2. Use `ft_read_stash` to ensure the stash contains a full line or all remaining data from the file.
3. Inside `ft_read_stash`, repeatedly read from the file descriptor into a temporary buffer until a newline character is found or the end of file is reached.
4. Use `ft_append_stash` to append each newly read buffer to the existing stash.
5. Once a newline is present, use `ft_fetch_line` to extract the next line and preserve the remainder in `stash`.

This algorithm is justified because:
- It supports arbitrary line lengths by reading in chunks of `BUFFER_SIZE`.
- It preserves unread data across multiple calls using a static stash.
- It minimizes unnecessary reads by stopping as soon as a full line is available.
- It handles end-of-file and error conditions cleanly.

## Instructions
*This project has been created as part of the 42 curriculum by mirelsan*

# get_next_line

## Description

This project implements `get_next_line`, a function that reads a file descriptor line by line. Its goal is to return the next line from the input each time the function is called, handling partial reads and preserving the remaining content between calls.

The implementation uses a static buffer called `stash` to store unread data that was already read but not yet returned. This allows the function to return one line at a time without losing data when a buffer read contains more than one line.

## Algorithm and Justification

The selected algorithm is a read-append-extract loop with a persistent stash:

1. Call `get_next_line(int fd)`.
2. Use `ft_read_stash` to ensure the stash contains a full line or all remaining data from the file.
3. Inside `ft_read_stash`, repeatedly read from the file descriptor into a temporary buffer until a newline character is found or the end of file is reached.
4. Use `ft_append_stash` to append each newly read buffer to the existing stash.
5. Once a newline is present, use `ft_fetch_line` to extract the next line and preserve the remainder in `stash`.

This algorithm is justified because:
- It supports arbitrary line lengths by reading in chunks of `BUFFER_SIZE`.
- It preserves unread data across multiple calls using a static stash.
- It minimizes unnecessary reads by stopping as soon as a full line is available.
- It handles end-of-file and error conditions cleanly.

## Instructions

### Compilation

There is no project Makefile in this folder, so compile manually using GCC.

Example:

```bash
gcc -Wall -Wextra -Werror -D BUFFER_SIZE=32 get_next_line.c get_next_line_utils.c -o get_next_line_example
```

If `BUFFER_SIZE` is not defined at compile time, the default value in `get_next_line.h` is `3`.

### Execution

The `get_next_line` function is designed to be called from a separate test program. For example, you can create a small `main.c` that opens a file descriptor and calls `get_next_line(fd)` in a loop.

A simple usage flow is:

```c
int fd = open("file.txt", O_RDONLY);
char *line;
while ((line = get_next_line(fd)) != NULL)
{
    printf("%s", line);
    free(line);
}
close(fd);
```

## Usage Example

```bash
./get_next_line_example < input.txt
```

Or in a custom test program:

```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int fd = open("input.txt", O_RDONLY);
    char *line;

    if (fd < 0)
        return 1;
    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return 0;
}
```

## Function Flow Diagram

![Diagrama de Funções](diagrama_5_mapa_funcoes.svg)

```
+-------------------+      +--------------------+      +---------------------+
| get_next_line(fd) | ---> | ft_read_stash(...) | ---> | ft_fetch_line(&stash)|
+-------------------+      +--------------------+      +---------------------+
                                   |
                                   v
                         +------------------------+
                         | ft_append_stash(...)   |
                         +------------------------+
                                   |
                                   v
                 +-----------------------------------------+
                 | read(fd, buffer, BUFFER_SIZE)          |
                 | ft_strjoin(stash, buffer)              |
                 | ft_strchr(stash, '\n')                 |
                 +-----------------------------------------+

```

### How it works

- `get_next_line` starts the process and validates the file descriptor.
- `ft_read_stash` checks whether the current stash already contains a complete line.
- If not, it calls `ft_append_stash` to read more data and extend the stash.
- Once a newline is found or the file ends, `ft_fetch_line` extracts the next line.
- The remaining bytes after the extracted line stay in `stash` for the next call.

### Utility functions used by the core flow

- `ft_strjoin`   : concatenates `stash` and the newly read buffer.
- `ft_strchr`   : searches for a newline character.
- `ft_strlen`   : computes string length.
- `ft_substr`   : slices the next line and the remainder from the stash.
- `ft_memcpy`   : copies memory safely for string operations.

## Project Files

- `get_next_line.c`       : main logic for reading lines and managing `stash`.
- `get_next_line_utils.c` : helper functions for string manipulation and buffer handling.
- `get_next_line.h`       : function prototypes, includes, and `BUFFER_SIZE` default.

## Resources

- POSIX `read()` documentation
- 42 Subject PDF for `get_next_line`
- C string handling references: `strchr`, `strlen`, `malloc`
- General guides on line-by-line file reading in C

## AI Usage

AI was used to create this README file, structure the documentation, and provide the visual function flow diagram. No AI-generated code was added to the project source; the implementation details were documented and explained by hand.

