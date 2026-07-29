#include <stdlib.h>
#include <unistd.h>

int is_space(char c)
{
    return(c == ' ' || c == '\t');
}

int count_words(char *str)
{ 
    int i = 0;
    int count;
    count = 0;
    while(str[i])
    {
        if((i == 0 || is_space(str[i-1])) && !is_space(str[i]))
            count += 1;
        i++;
    }
    return(count);
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        write(1, "\n", 1);
        return(0);
    }
    int i = 0;
    int words_width;
    words_width = count_words(argv[1]);
    if(words_width == 0)
    {
        write(1, "\n", 1);
        return(0);
    }

    int *starts;
    int *ends;
    starts = malloc(sizeof(int) * words_width);
    ends = malloc(sizeof(int) * words_width);
    if(!starts)
    {
        return(0);
    }
    if(!ends)
    {
        return(0);
    }
    int word_index = 0;
    i = 0;
    while(argv[1][i])
    {
        if((i == 0 || is_space(argv[1][i-1])) && !is_space(argv[1][i]))
        {
            starts[word_index] = i;
            word_index++;
        }
        if(!is_space(argv[1][i]))
            ends[word_index - 1] = i;
        i++;
    }
    int total_len;
    int k;
    total_len = 0;
    k = 0;
    while(k < words_width)
    {
        total_len = total_len + (ends[k] - starts[k] + 1);
        k++;
    }
    int len_buff;
    len_buff = (words_width - 1) + total_len;
    char *fill_buff;
    fill_buff = malloc(sizeof(char) * len_buff);
    if(!fill_buff)
        return(0);
    int h = 1;
    int buff_i = 0;
    while(h < words_width)
    {
        if(buff_i != 0)
        {
            fill_buff[buff_i] = ' ';
            buff_i++;
        }
        int src = starts[h];
        while(src <= ends[h])
        {
            fill_buff[buff_i] = argv[1][src];
            src++;
            buff_i++;
        }
        h++;
    }
    if(buff_i != 0)
    {
        fill_buff[buff_i] = ' ';
        buff_i++;
    }
    int src = starts[0];
    while(src <= ends[0])
    {
        fill_buff[buff_i] = argv[1][src];
        src++;
        buff_i++;
    }

    write(1, fill_buff, len_buff);
    write(1, "\n", 1);

    free(starts);
    free(ends);
    free(fill_buff);
    return(0);
}
