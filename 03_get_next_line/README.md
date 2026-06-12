*This project has been created as part of the 42 curriculum by mirelsan.*

# Get Next Line

## Description

This project implements the `get_next_line` function, which reads and returns one line at a time from a file descriptor. Each call to `get_next_line` returns the next line, including the terminating newline character when present, until the end of file is reached. The implementation is designed to support arbitrary line lengths while reusing leftover data across repeated calls on the same file descriptor.

The main goal is to build a line-reading utility similar to the one required by the 42 curriculum, using only allowed system calls and custom helper functions.

## Algorithm and Justification

The selected algorithm is a buffered read-and-stash approach with the following key ideas:

- Use a static `stash` to keep unread data between function calls.
- Read from the file descriptor in chunks of `BUFFER_SIZE` bytes.
- Append each chunk to the stash until a newline is encountered or EOF is reached.
- Extract the next line from the stash and preserve the remaining data for future calls.

This algorithm is justified because:

- It supports lines longer than `BUFFER_SIZE` by accumulating partial reads in the stash.
- It avoids reading more data than necessary by stopping reads after a newline is found.
- It keeps leftover bytes between calls, which is essential for sequential line retrieval from a single descriptor.
- It keeps the core logic simple and deterministic while using minimal dynamic memory.

## Function Map

The complete function map is presented below with the connection flow between each module of the implementation.

<svg width="100%" height="420" viewBox="0 0 1100 420" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet">
  <style>
    .box { fill:#f8f9fa; stroke:#2f4f4f; stroke-width:2px; rx:12; }
    .arrow { stroke:#2f4f4f; stroke-width:2px; fill:none; marker-end:url(#arrowhead); }
    .title { font: bold 16px sans-serif; fill:#17202a; }
    .label { font: 14px sans-serif; fill:#17202a; }
  </style>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#2f4f4f" />
    </marker>
  </defs>

  <rect x="40" y="20" width="320" height="80" class="box" />
  <text x="60" y="50" class="title">get_next_line()</text>
  <text x="60" y="70" class="label">- static stash</text>
  <text x="60" y="88" class="label">- returns next line</text>

  <rect x="390" y="20" width="300" height="80" class="box" />
  <text x="410" y="50" class="title">ft_read_stash()</text>
  <text x="410" y="70" class="label">- loop until newline</text>
  <text x="410" y="88" class="label">- appends read data</text>

  <rect x="760" y="20" width="300" height="80" class="box" />
  <text x="780" y="50" class="title">ft_fetch_line()</text>
  <text x="780" y="70" class="label">- extract line</text>
  <text x="780" y="88" class="label">- preserve remainder</text>

  <line x1="360" y1="60" x2="390" y2="60" class="arrow" />
  <line x1="690" y1="60" x2="760" y2="60" class="arrow" />

  <rect x="390" y="140" width="300" height="80" class="box" />
  <text x="410" y="170" class="title">ft_verify_stash()</text>
  <text x="410" y="190" class="label">- check newline</text>

  <rect x="760" y="140" width="300" height="120" class="box" />
  <text x="780" y="170" class="title">ft_append_stash()</text>
  <text x="780" y="190" class="label">- read BUFFER_SIZE</text>
  <text x="780" y="210" class="label">- append into stash</text>
  <text x="780" y="230" class="label">- stop on newline / EOF</text>

  <line x1="540" y1="100" x2="540" y2="140" class="arrow" />
  <line x1="690" y1="100" x2="690" y2="140" class="arrow" />

  <rect x="40" y="240" width="300" height="120" class="box" />
  <text x="60" y="270" class="title">ft_strjoin()</text>
  <text x="60" y="290" class="label">- concat stash + buffer</text>
  <text x="60" y="310" class="label">- allocate result</text>

  <rect x="390" y="240" width="300" height="120" class="box" />
  <text x="410" y="270" class="title">ft_substr()</text>
  <text x="410" y="290" class="label">- take prefix or suffix</text>
  <text x="410" y="310" class="label">- preserve remainder</text>

  <rect x="760" y="240" width="300" height="120" class="box" />
  <text x="780" y="270" class="title">ft_strchr() / ft_strlen()</text>
  <text x="780" y="290" class="label">- search newline</text>
  <text x="780" y="310" class="label">- measure length</text>
  <text x="780" y="330" class="label">- safe string ops</text>

  <line x1="540" y1="220" x2="390" y2="240" class="arrow" />
  <line x1="540" y1="220" x2="760" y2="240" class="arrow" />
  <line x1="390" y1="178" x2="390" y2="240" class="arrow" />

  <rect x="40" y="370" width="300" height="40" class="box" />
  <text x="60" y="395" class="title">ft_memcpy()</text>

  <line x1="190" y1="240" x2="190" y2="370" class="arrow" />
  <line x1="460" y1="260" x2="460" y2="370" class="arrow" />
</svg>

## Function Details and Connection

- `get_next_line(int fd)` is the entry point. It validates `fd` and uses a static `stash` string to keep unread content across calls.
- `ft_read_stash(char *stash, int fd)` ensures there is at least one full line in the stash by reading and appending from `fd` until a newline appears or EOF is reached.
- `ft_verify_stash(char *stash)` checks whether the current stash already contains a newline and returns a status code.
- `ft_append_stash(char *stash, int fd)` reads data from the file descriptor into a temporary buffer, appends it to the stash, and stops as soon as a newline is found or the end of file is reached.
- `ft_fetch_line(char **stash)` takes the first line from the stash, returns it, and updates the stash pointer to the remaining text.
- `ft_strjoin`, `ft_substr`, `ft_strchr`, `ft_strlen`, and `ft_memcpy` are helper functions that implement basic string operations without using non-permitted library calls.

## Instructions

### Compilation

There is no Makefile in the project folder, so compile manually with `gcc`.

Example command:

```bash
gcc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c -o get_next_line
```

If you prefer to use the default buffer size defined in `get_next_line.h`, omit the `-D BUFFER_SIZE=42` flag.

### Execution

This repository does not include a dedicated test program, so you may create a small driver program or use the function inside another C project. Example usage pattern:

1. Open a file descriptor with `open("test.txt", O_RDONLY)`.
2. Call `get_next_line(fd)` repeatedly.
3. Print each returned line until the function returns `NULL`.
4. Close the file descriptor and free the returned strings.

Example flow:

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

## Resources

- Official 42 school subject and validation rules for `get_next_line`
- POSIX `read()` function documentation
- C standard library string handling concepts
- Tutorials on buffered I/O and static storage in C

## AI Usage

AI was used to analyze the project source files and to write this README content, including the algorithm explanation, function map, and user instructions. No source code logic was changed by AI during this documentation update.

## Notes

- The implementation is built around a static stash so a single file descriptor can be read across multiple calls.
- The function preserves any unread content between calls and only returns `NULL` after all text has been consumed.

