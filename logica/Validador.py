class Validador:
    
    @staticmethod
    def val_int():
        while(True):
            try:
                return int(input('>> '))
            except ValueError:
                print('Ingrese un numero entero')

    @staticmethod
    def val_float():
        while(True):
            try:
                return float(input('>> '))
            except ValueError:
                print('Ingrese un numero real')
