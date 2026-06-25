#!bin/bash
bench()
{
	local tests=50
	local total=100
	local min_val=1
	local max_val=5000
	local checker="./checker_linux"
	local sum=0
	local min=999999
	local max=0
	local i=1
	local arg
	local moves
	local res
	local out

	echo "Execulting $tests tests  $total numbers..."

	while [ "$i" -le "$tests" ]; do
		
		arg=$(python3 -c "import random; print(' '.join(map(str, random.sample(range($min_val, $max_val), $total))))")
		out=$(./push_swap $arg)
		moves=$(echo "$out" | grep -E "^(sa|sb|ss|pa|pb|ra|rb|rr|rra|rrb|rrr)$" | wc -l)
		res=$(echo "$out" | $checker $arg)
		if [ "$res" != "OK" ]; then
			echo "Test $i: KO! ($res)" && exit 1
		fi
		sum=$((sum + moves))
		[ "$moves" -lt "$min" ] && min=$moves
		[ "$moves" -gt "$max" ] && max=$moves
		echo "Tests $i: OK -> $moves movs"
		i=$((i + 1))
	done
	echo -e "\n=== RESULT: Min: $min | Medium: $((sum / tests)) | Max: $max ==="
}
bench
