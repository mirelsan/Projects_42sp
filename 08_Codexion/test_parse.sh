#!/bin/bash
# test_parse.sh - testa a validacao de argumentos do Codexion
#
# uso:  ./test_parse.sh [binario] [-v]
#   ./test_parse.sh                  -> testa ./test_init
#   ./test_parse.sh ./codexion       -> testa o binario final
#   ./test_parse.sh ./test_init -v   -> mostra a saida completa de cada caso
#
# O script NAO corrige nada: ele so roda os casos e mostra o que aconteceu.
# Interpretar o resultado e consertar o parsing e com voce.

BIN="${1:-./test_init}"
VERBOSE="$2"
BASE=(5 800 200 200 200 5 50 fifo)
OK=0
FAIL=0
DECIDE=0

R=$'\033[31m'
G=$'\033[32m'
Y=$'\033[33m'
C=$'\033[36m'
N=$'\033[0m'

if [ ! -x "$BIN" ]; then
	echo "Binario '$BIN' nao encontrado (ou sem permissao de execucao)."
	exit 1
fi

# run_case "descricao" esperado [args...]
# esperado: reject | accept | decide
run_case()
{
	local label="$1"
	local expected="$2"
	local out code first verdict

	shift 2
	out=$(timeout 5 "$BIN" "$@" 2>&1)
	code=$?
	first=$(echo "$out" | sed 's/\x1b\[[0-9;]*m//g' | grep -m1 . | cut -c1-70)
	if [ "$code" -eq 124 ]; then
		verdict="${R}TRAVOU (timeout)${N}"
		FAIL=$((FAIL + 1))
	elif [ "$code" -ge 128 ]; then
		verdict="${R}CRASH (sinal $((code - 128)))${N}"
		FAIL=$((FAIL + 1))
	elif [ "$expected" = "decide" ]; then
		verdict="${Y}SUA DECISAO (saiu com $code)${N}"
		DECIDE=$((DECIDE + 1))
	elif [ "$expected" = "reject" ] && [ "$code" -ne 0 ]; then
		verdict="${G}OK (rejeitou)${N}"
		OK=$((OK + 1))
	elif [ "$expected" = "accept" ] && [ "$code" -eq 0 ]; then
		verdict="${G}OK (aceitou)${N}"
		OK=$((OK + 1))
	else
		verdict="${R}FALHOU (esperado: $expected, saiu com $code)${N}"
		FAIL=$((FAIL + 1))
	fi
	printf "%-38s %s\n" "$label" "$verdict"
	printf "    ${C}-> %s${N}\n" "$first"
	if [ "$VERBOSE" = "-v" ]; then
		echo "$out" | sed 's/^/    | /'
	fi
}

# case_with "descricao" esperado posicao valor
# parte do exemplo base e troca so o argumento 'posicao' (1 a 8)
case_with()
{
	local args=("${BASE[@]}")

	args[$3-1]="$4"
	run_case "$1" "$2" "${args[@]}"
}

echo "Binario: $BIN"
echo "Base:    ${BASE[*]}"

echo
echo "=== Devem ser REJEITADOS (subject, pag. 9) ==="
case_with "coders negativo (-5)" reject 1 -5
case_with "burnout negativo" reject 2 -800
case_with "compile negativo" reject 3 -200
case_with "debug negativo" reject 4 -200
case_with "refactor negativo" reject 5 -200
case_with "compiles_required negativo" reject 6 -5
case_with "cooldown negativo" reject 7 -50
case_with "coders decimal (5.5)" reject 1 5.5
case_with "burnout decimal (800.5)" reject 2 800.5
case_with "coders texto (abc)" reject 1 abc
case_with "burnout com lixo no fim (800abc)" reject 2 800abc
case_with "burnout vazio" reject 2 ""
case_with "so um sinal (+)" reject 2 +
case_with "scheduler invalido (lifo)" reject 8 lifo
case_with "scheduler maiusculo (FIFO)" reject 8 FIFO
case_with "scheduler vazio" reject 8 ""
case_with "burnout > INT_MAX (2147483648)" reject 2 2147483648
case_with "burnout com 11 digitos" reject 2 99999999999
run_case "sem nenhum argumento" reject
run_case "7 argumentos (falta o scheduler)" reject 5 800 200 200 200 5 50
run_case "9 argumentos (um a mais)" reject "${BASE[@]}" 1

echo
echo "=== Devem ser ACEITOS ==="
run_case "exemplo base" accept "${BASE[@]}"
case_with "scheduler edf" accept 8 edf
case_with "1 coder" accept 1 1
case_with "200 coders" accept 1 200
case_with "debug = 50 ms (sem minimo de 60)" accept 4 50
case_with "burnout = INT_MAX (2147483647)" accept 2 2147483647

echo
echo "=== SUA DECISAO (o subject nao diz; voce precisa defender) ==="
case_with "coders = 0" decide 1 0
case_with "burnout = 0" decide 2 0
case_with "compile = 0" decide 3 0
case_with "debug = 0" decide 4 0
case_with "refactor = 0" decide 5 0
case_with "compiles_required = 0" decide 6 0
case_with "cooldown = 0" decide 7 0
case_with "com sinal (+5)" decide 1 +5
case_with "espaco antes (' 5')" decide 1 " 5"
case_with "zeros a esquerda (007)" decide 1 007

echo
echo "Resumo: ${G}$OK ok${N} | ${R}$FAIL falhas${N} | ${Y}$DECIDE para decidir${N}"
[ "$FAIL" -eq 0 ]
