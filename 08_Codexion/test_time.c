#include <stdio.h>
#include <unistd.h>

/* O compilador precisa saber que essa função existe no time.c */
long	get_time_ms(void); 

int	main(void)
{
	long	start;
	long	end;

	start = get_time_ms();
	usleep(200000); /* 200 milissegundos = 200.000 microssegundos */
	end = get_time_ms();
	
	printf("Diferença: %ld ms\n", end - start);
	return (0);
}