import numpy as np

dxTransducer = 13.5e-3      #distance between transducers in x [in m]
dyTransducer = 11.69e-3     #distance between transducers in y [in m]

class Transducer:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class TransducerArray:
    def __init__(self, configuration):
        self.configuration = configuration
        
    def getRowHex(self, Transducers, sizeHalf, rowNum, start, center):
        #To assign the position of the transducers in the hexagonal shape
            #Transducers: array of transducers to edit
            #sizeHalf: size of half of the transducers in a row (without counting the center one if there is one)
            #rowNum: number of row to calculate
            #start: starting position of the next row in the array (amount of transducers in row + what was already there)
            #center: if there is a center transducer (aka uneven number of transducers in row)
            
            if center == 1:
                Tcenter = Transducer(0, dyTransducer*rowNum, 0)
                Transducers[start, :] = (Tcenter.x, Tcenter.y, Tcenter.z)
                
                for n in range(start+1, start+sizeHalf+1):
                    TransducerAux1 = Transducer((n-start)*dxTransducer, dyTransducer*rowNum, 0)
                    TransducerAux2 = Transducer(-(n-start)*dxTransducer, dyTransducer*rowNum, 0)
                    Transducers[n, :] = (TransducerAux1.x, TransducerAux1.y, TransducerAux1.z)
                    Transducers[2*(start+sizeHalf)-n+1, :] = (TransducerAux2.x, TransducerAux2.y, TransducerAux2.z)
            else:
                for n in range(start, start+sizeHalf):
                    TransducerAux1 = Transducer((n-start)*dxTransducer+dxTransducer/2, dyTransducer*rowNum, 0)
                    TransducerAux2 = Transducer(-(n-start)*dxTransducer-dxTransducer/2, dyTransducer*rowNum, 0)
                    Transducers[n, :] = (TransducerAux1.x, TransducerAux1.y, TransducerAux1.z)
                    Transducers[2*(start+sizeHalf)-n-1, :] = (TransducerAux2.x, TransducerAux2.y, TransducerAux2.z)
        
            return Transducers

        
    def getTransducers(self):
        configuration = self.configuration
        
        if(configuration == "hexagon"):
            numTransducers = 61
            Transducers = np.zeros((numTransducers, 3))       #define the Transducers' position: x, y, z
            acc = 0
            
            for n in range(5):
                #check if the row number is odd (meaning it has a center transducer)
                center = abs(n % 2 - 1)
                
                #Assign number of transducers on each row: sizeHalf*2+center
                if (n == 0) or (n == 1):
                    sizeHalf = 4
                elif (n == 2) or (n == 3):
                    sizeHalf = 3
                else:
                    sizeHalf = 2
            
                Transducers = self.getRowHex(Transducers, sizeHalf, n, acc, center)
                acc = acc + 2*sizeHalf+center   # Increase position in array 
                # Zero does not have a mirror image
                if (n != 0):
                    Transducers = self.getRowHex(Transducers, sizeHalf, -n, acc, center)
                    acc = acc + 2*sizeHalf+center # Increase position in array 
            
            
            #for easy revision when printing
            transducerNumbers = np.vstack(np.arange(numTransducers))
            np.set_printoptions(suppress=True)
            print(np.column_stack((transducerNumbers, Transducers)))
             
            
TA = TransducerArray("hexagon")
TA.getTransducers()
        