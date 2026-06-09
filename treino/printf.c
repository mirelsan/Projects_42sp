#include <stdarg.h>
#include <unistd.h>

int ft_printf(const char *format, ...)
{
    va_list ap;
    int    i;

    va_start(ap, format);

    i = 0;
    while(*format)
    {
        if(*format != '%')
        {
            i += print_char(*format);
            ++format;
        }
        else
        {
        ++format;
        i += ft_format(ap, *format);
        ++format;
        }
    }
    va_end(ap);
    return(i);
}