#include "coders.h"

int main(int ac, char **av)
{
    t_workspace workspace;

    if (ac != 9)
    {
        printf("Uso: ./test_parsing <coders> <burnout_ms> <compile_ms> <debug_ms> <refactor_ms> <compiles_req> <cooldown_ms> <fifo|edf>\n");
        return (1);
    }

    printf("Iniciando o parsing em modo de teste...\n");
    parse_input(&workspace, av);

    printf("\n" BOLD_GREEN "--- Resultado do Parsing ---" RST "\n");
    printf("Coders: %ld\n", workspace.number_of_coders);
    printf("Time to Burnout (us): %ld\n", workspace.time_to_burnout);
    printf("Time to Compile (us): %ld\n", workspace.time_to_compile);
    printf("Time to Debug (us): %ld\n", workspace.time_to_debug);
    printf("Time to Refactor (us): %ld\n", workspace.time_to_refactor);
    printf("Compiles Required: %ld\n", workspace.number_of_compiles_required);
    printf("Dongle Cooldown (us): %ld\n", workspace.dongle_cooldown);
    printf("Scheduler: %s\n", workspace.scheduler == SCHEDULER_FIFO ? "FIFO" : "EDF");
    printf(BOLD_GREEN "----------------------------" RST "\n");

    return (0);
}