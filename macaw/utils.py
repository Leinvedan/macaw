import sys

# Como só existe uma opção, resolvi deixar
# a implementação do CLI para quando existirem pelo
# menos 2 outputs diferentes


def handle_cli():
    if len(sys.argv) < 2:
        print('Please choose a output argument')
        print('--print: prints the result in stdout')
        sys.exit(0)
    match sys.argv[1]:
        case '--print':
            return
