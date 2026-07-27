# CONTEXTO

O Born2beroot pede a configuração de uma máquina virtual [Debian/Rocky],
sem interface gráfica, seguindo normas rígidas de segurança: senha forte,
sudo restrito, SSH em porta não-padrão, firewall ativo, particionamento
com LVM e um script de monitoramento rodando via cron.

### Restrições obrigatórias do subject

- Regras gerais: Uso obrigatório do VirtualBox
- Regras gerais: signature.txt na raiz do repositório, com o hash SHA1 do disco virtual da minha VM, é proibido subir a VM em si no Git
- Sistema Operacional: Como escolhi o Debian: o AppArmor tem que estar ativo no boot
- Partições: Pelo menos 2 partições criptografadas usando LVM
- Hostname: Tem que ser meu login terminado em 42 (mirelsan42)
- SSH: Rodando apenas na porta 4242 e proibido logar como root via SSH
- Firewall: UFW (Debian) deixando só a porta 4242 aberta
- Usuários e grupos: Além do root, precisa existir um usuário com meu login, esse usuário tem que pertencer aos grupos user42 e sudo

## Escolha do sistema: [Debian / Rocky]

**Decisão:** Usei Debian, versão.

**Por quê:** Debian é mais leve e mais comum em servidores reais /
Rocky por familiaridade com RHEL, é mais complexo para o meu primeiro projeto usando o terminal.

**Alternativa considerada:** [o outro SO] — descartado porque [motivo].

## Particionamento com LVM

**Decisão:** Criei os Physical Volumes [/dev/sdaX] agrupados no Volume
Group [nome], dividido nos Logical Volumes: [/, /home, /var, /var/log,
/tmp, /srv, swap...].

**Por quê:** [ex: separar /var e /var/log evita que logs excessivos
derrubem o sistema todo; swap dimensionado em X porque a RAM é Y]

**Criptografia:** [Usei LUKS em X partições / não usei] porque [motivo].

## Política de senha

**Decisão:** Configurei via [/etc/login.defs e PAM (pam_pwquality)]:
- Expiração a cada [N] dias
- Aviso [N] dias antes de expirar
- Mínimo de [N] dias entre trocas
- Tamanho mínimo [N] caracteres
- Exigência de [maiúscula/minúscula/número/caractere especial]
- Bloqueio de reutilização das últimas [N] senhas

**Por quê:** [essas regras replicam requisitos de segurança corporativa
reais / são as exigências literais do subject]

## Política de sudo

**Decisão:** No /etc/sudoers.d/[arquivo], configurei:
- Log de tentativas em [/var/log/sudo/]
- Limite de [N] tentativas de senha
- Mensagem customizada de erro
- Restrição de TTY / secure_path

**Por quê:** [rastreabilidade de quem faz o quê como root, evitar
brute-force de senha, evitar hijacking de PATH]

## SSH

**Decisão:** Porta alterada de 22 para [porta], `PermitRootLogin no`,
[outras diretivas do sshd_config].

**Por quê:** [reduzir varredura automática de bots na porta padrão,
seguir requisito do subject de não logar como root via SSH]

## Firewall (UFW/firewalld)

**Decisão:** Liberei apenas a porta [SSH customizada] e bloqueei o resto.

**Por quê:** [princípio de menor privilégio — só abrir o estritamente
necessário]

## monitoring.sh

**Decisão:** O script mostra [arquitetura, CPU physical/virtual, RAM
usada, uso de disco, load average, últimos boots, LVM ativo, conexões
TCP, usuários logados, IP/MAC, comandos sudo executados], rodando via
cron a cada [N] minutos, enviado para todos os terminais com `wall`.

**Por quê de cada bloco (se quiser detalhar):**
- [bloco X]: [motivo de estar ali / o que ele revela sobre a saúde da VM]

## Problema: [nome curto]

**O que aconteceu:** [descrição do erro/sintoma]

**Causa raiz:** [o que você descobriu que estava causando]

**Solução:** [o que você fez]

**O que eu aprendi:** [1 frase]

## Perguntas

**P: Por que LVM e não partições simples?**
R: [sua resposta em 1-2 frases]

**P: Por que essa porta de SSH?**
R: [sua resposta]

**P: O que acontece se o disco de /var/log encher?**
R: [sua resposta]
