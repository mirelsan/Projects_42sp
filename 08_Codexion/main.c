#include "coders.h"


int main(int ac, char **av)
{
    t_workspace ws;
    int         i;

    if (ac != 9)
    {
        printf("Uso: ./test_init <coders> <burnout> <compile> <debug> <refactor> <compiles> <cooldown> <fifo|edf>\n");
        return (1);
    }

    // 1. Parsing
    parse_input(&ws, av);

    // 2. Inicialização dos Dados e Mutexes
    data_init(&ws);

    
    ws.start_simulation = get_time_ms();
    i = 0;
    while (i < ws.number_of_coders)
    {
        safe_thread_handle(&ws.coders[i].thread_id, coder_routine, &ws.coders[i], CREATE);
        i++;
    }
    i = 0;
    while (i < ws.number_of_coders)
    {
        safe_thread_handle(&ws.coders[i].thread_id, NULL, NULL, JOIN);
        i++;
    }
    // 3. Destruição e Liberação de Memória
    cleanup_data(&ws);
    printf(BOLD_GREEN "Limpeza de memória e mutexes executada com sucesso!" RST "\n\n");

    return (0);
}