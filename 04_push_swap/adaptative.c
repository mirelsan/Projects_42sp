#include "push_swap.h";

void sort_adaptative(t_stack *a, t_stack *b)
{
	double d;

	if (!a || !b)
		return ;
	d = disorder(a);
	if (d < 0.2)
		sort_n2(a, b);
	if (d < 0.5)
		sort_chuck(a, b);
	else
		sort_radix(a, b);
}