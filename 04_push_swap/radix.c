#include "push_swap.h"

int max_bits(t_stack *a)
{
	t_node *curr;
	int max;
	int i;

	if (!a || !a->head)
		return (0);
	curr = a->head;
	max = 0;
	while (curr)
	{
		if (curr->index > max)
			max = curr->index;
		curr = curr->next;
	}
	
	i = 0;
	while ((1 << i) <= max)
		i++;
	return (i);
}

int has_bit(int n, int bit)
{
	int shifed;
	
	shifed = (n >> bit);
	return ( shifed & 1);
}

void process_bit(t_stack *a, t_stack *b, int bit)
{
	int bit_size;

	bit_size = a->size;
	while (bit_size--)
	{
		if (has_bit(a->head->index, bit))
			pb(a, b);
		else
			ra(a);
	}
	while (b->size > 0)
		pa(a, b);
}

void sort_radix(t_stack *a, t_stack *b)
{
	int bits;
	int i;

	if (!a || a->size <= 1)
		return ;
	bits = max_bits(a);
	i = 0;
	while (i < bits)
	{
		process_bit(a, b, i);
		i++;
	}
}