#include "coders.h"

#define TOLERANCE_MS 20

int	main(void)
{
	t_workspace	ws;
    char *av[] = {"./test_routine", "2", "800", "200", "200",
        "200", "2", "0", "fifo"};
	int			i;
	long		expected;
	long		elapsed;

	parse_input(&ws, av);
	data_init(&ws);
	ws.start_simulation = get_time_ms();
	i = 0;
	while (i < ws.number_of_coders)
	{
		safe_thread_handle(&ws.coders[i].thread_id, coder_routine,
			&ws.coders[i], CREATE);
		i++;
	}
	i = 0;
	while (i < ws.number_of_coders)
	{
		safe_thread_handle(&ws.coders[i].thread_id, NULL, NULL, JOIN);
		i++;
	}
	elapsed = get_elapsed_time(ws.start_simulation);
	expected = ws.number_of_coders * ws.time_to_compile;
	printf("\nTotal time: %ld ms (expected: ~%ld ms)\n", elapsed, expected);
	if (elapsed + TOLERANCE_MS < expected)
		printf("FAILED: too fast, coders compiled at the same time\n");
	else if (elapsed > expected + 100)
		printf("FAILED: too slow, something is stuck\n");
	else
		printf("OK: the dongles are used one coder at a time\n");
	cleanup_data(&ws);
	return (0);
}