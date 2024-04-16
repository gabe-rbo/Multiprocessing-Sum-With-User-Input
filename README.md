# MultiprocessingSum
Testing the multiprocessing input with a simple function that asks the user for 2 (float) numbers and sums them. This is a simple test, and is used to, simply, show how my idea works. 

Here, there are two files. Since most of the code and variables names are in portuguese, i will give a throughout explanation of the code here.
I start with the testesoma (testsum), it's a simple code of a function that asks the user for two numbers and sums them. 
The other file is called multiprocesso_soma (multiprocess_sum) - it's composed of two branches:

#### The function tentativa (attempt) 
    def tentativa(n1: float, n2: float) -> tuple:
    
It takes two arguments: n1 and n2 and returns a tuple. It's main purpose is to construct the process using Popen (subprocess) and trade information with it using PIPE's. Since the subprocess library only works with scripts, we have to give it a file path for the script we want to work with. Originally, the process construction was: 

     processo = Popen([r'python.exe', r'-u', r'testesoma.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
 
later (but while the last line still being in the file although commented), this was changed and will be shown and explained why forward in this text.
After the process is constructed, we communicate the numbers we want to sum, get the output and error by using the following lines of code:

    processo.stdin.write(str(n1) + '\n')
    processo.stdin.flush()

    processo.stdin.write(str(n2) + '\n')
    processo.stdin.flush()

    output, erro = processo.communicate()

And then we ask for the return of output and erro (error): 

    return output, erro

The output part of the tuple, however, is not as efficient as we want it to be. As a matter of fact, if we make the process sum 1 + 2 it returns this tuple:

    ('Digite o primeiro número: Digite o segundo número:', '')
    # ('Type the first number: Type the second number:', '')

This happens because the output is only what is shown in the cmd - in this case, the cmd and process only see the input messages, which are what we got. This made me go to the original sum script and make the function print it's outcome to the screen. It also made me call the function itself on it's script, otherwise it would only define the function and not actually run it. Effectivilly, this is pretty bad, since this was a "trial and error" for a bigger project of Correction of Python Scripts. For this to be implemented, i would have to modify students submitted scrpits - which is not a good idea for any teacher. Therefore, the way we build the process had to be changed.
For a fact, since we are opening a script, we can take advantage of cmd's functionalities: in this case we are going to use writing a one line python code. This resulted in the following construction:

    processo = Popen(["python", "-c", "import sys; from testesoma import soma; x = soma(); print('soma(): ' + str(x));"], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8', text=True)

In this case, we call python in the cmd (-c) and import sys. Then, from the original file script, i import the function i wanted, assigned a variable to it and called it using print. This makes me be able to catch the functions output whitout altering the inteded script - also, it allows me to know where the return will be (in this case, i used the string "soma():" to identify it), which is quite useful, since i need this to correct student code. 

#### '__main__'
    if __name__ == '__main__':
    
In here is where the magic happens. I create a Pool of workers using multiprocessing and starmap to the the function tentativa the intended tuple of numbers i want to sum. I then print the outcome to show the unfiltered result.

    p = Pool(min(cpu_count(), 61))
    somas = p.starmap(tentativa, [(1, 2), (7, 8), (4, 6)])
    print(somas)

Then, to show the functionality of the previous added string for the result, i create a simple filter to find where the return is, and then i print it.

    for tupla in somas:
    
      r = tupla[0]  # r de resposta  -> answer 
      e = tupla[1]  # e de erro      -> error
    
      string_r = r.find('soma():')
    
      saida_soma = r[string_r:]  # sum output
    
      print(f'{saida_soma}')
