#include "coders.h"

// Função de liberação para podermos testar vazamentos no Valgrind
void cleanup_data(t_workspace *ws)
{
    int i;

    if (ws->dongles)
    {
        i = 0;
        while (i < ws->number_of_coders)
        {
            safe_mutex_handle(&ws->dongles[i].dongle, DESTROY);
            safe_cond_handle(&ws->dongles[i].cond, DESTROY);
            i++;
        }
        free(ws->dongles);
    }
    safe_mutex_handle(&ws->log_mutex, DESTROY);
    if (ws->coders)
        free(ws->coders);
}

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

    printf(BOLD_GREEN "\n--- TESTE DE INICIALIZAÇÃO DE DONGLES E PREVENÇÃO DE DEADLOCK ---" RST "\n");
    printf("Total de Coders / Dongles: %ld\n\n", ws.number_of_coders);

    i = 0;
    while (i < ws.number_of_coders)
    {
        t_coder *c = &ws.coders[i];
        printf(BOLD_CYAN "Coder ID %d" RST " (Par/Ímpar: %s):\n", 
               c->id, (c->id % 2 == 0) ? "PAR" : "ÍMPAR");
        printf("  -> Primeiro Dongle a pegar: ID %d\n", c->first_dongle->dongle_id);
        printf("  -> Segundo Dongle a pegar:  ID %d\n\n", c->second_dongle->dongle_id);
        i++;
    }

    // 3. Destruição e Liberação de Memória
    cleanup_data(&ws);
    printf(BOLD_GREEN "Limpeza de memória e mutexes executada com sucesso!" RST "\n\n");

    return (0);
}