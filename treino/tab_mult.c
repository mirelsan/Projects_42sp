#include <unistd.h>

int ft_atoi(char *str)
{
    int result;
    result = 0;
    int i = 0;

    while(str[i])
    {
        result = result * 10 + (str[i] - '0');
        i++;
    }
    return(result);
}

void print_nbr(int n)
{
    char c;
    if(n >= 10)
    {
        print_nbr(n/10);
    }
    c = (n % 10) + '0';
    write(1, &c, 1);
}

int main(int argc, char **argv)
{
    if(argc <= 1)
    {
        write(1, "\n", 1);
        return(0);
    }

    int n;
    int i;
    i = 1;
    n = ft_atoi(argv[1]);
    while(i <= 9)
    {
       print_nbr(i);
       write(1, " x ", 3);
       print_nbr(n);
       write(1, " = ", 3);
       print_nbr(i * n);
       write(1, "\n", 1);
       i++; 
    }
}
