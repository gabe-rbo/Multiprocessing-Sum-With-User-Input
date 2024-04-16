from multiprocessing import Pool, cpu_count
from subprocess import PIPE, Popen


def tentativa(n1: float, n2: float) -> tuple:

    # processo = Popen([r'python.exe', r'-u', r'testesoma.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')  -> é o que tínhamos antes
    processo = Popen(["python", "-c", "import sys; from testesoma import soma; x = soma(); print('soma(): ' + str(x));"], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8', text=True)

    processo.stdin.write(str(n1) + '\n')
    processo.stdin.flush()

    processo.stdin.write(str(n2) + '\n')
    processo.stdin.flush()

    output, erro = processo.communicate()
    processo.terminate()

    return output, erro


if __name__ == '__main__':
    p = Pool(min(cpu_count(), 61))
    somas = p.starmap(tentativa, [(1, 2), (7, 8), (4, 6)])
    print(somas)

    for tupla in somas:

        r = tupla[0]  # r de resposta
        e = tupla[1]  # e de erro

        string_r = r.find('soma():')

        saida_soma = r[string_r:]

        print(f'{saida_soma}')
