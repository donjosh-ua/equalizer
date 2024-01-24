class Validador:
    
    @staticmethod
    def val_int(prompt=''):
        while(True):
            try:
                prompt != '' and print(prompt)
                return int(input('>> '))
            except ValueError:
                print('Ingrese un numero entero')

    @staticmethod
    def val_float(prompt=''):
        while(True):
            try:
                prompt != '' and print(prompt)
                return float(input('>> '))
            except ValueError:
                print('Ingrese un numero real')
