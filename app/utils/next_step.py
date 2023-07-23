import sys


def next_step(msg: str = "Deseja prosseguir?", details="") -> bool:

    details = f'\t\t*{details}*' if len(details) > 0 else details;
    print(f'{msg} [Y/N]{details}')
    while True:
        response = input('R: ')

        if response.upper() == 'Y':
            print('Executando próxima etapa...')
            break

        if response.upper() == 'N':
            print('Closed System Successfully')
            sys.exit()
