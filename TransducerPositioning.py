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
        
    def getRowHex(self, Transducers, rowLength, rowNum, start):
        #To assign the position of the transducers in the hexagonal shape
        if np.abs(rowLength % 2) == 1:
            sizeHalf = rowLength // 2
            Transducers[sizeHalf+start, :] = (0, rowNum*dyTransducer, 0)
            
            for n in range(start, start+sizeHalf):
                TransducerAux = Transducer((n-start-sizeHalf)*dxTransducer, rowNum*dyTransducer, 0)
                TransducerAux1 = Transducer((n-start+1)*dxTransducer, rowNum*dyTransducer, 0)
                
                Transducers[n, :] = (TransducerAux.x, TransducerAux.y, TransducerAux.z)
                Transducers[n+sizeHalf+1, :] = (TransducerAux1.x, TransducerAux1.y, TransducerAux1.z)
        else:
            sizeHalf = int(rowLength / 2)
            for n in range(start, start+sizeHalf):
                TransducerAux = Transducer(-(-n+start+sizeHalf-0.5)*dxTransducer, rowNum*dyTransducer, 0)
                TransducerAux1 = Transducer((n-start+0.5)*dxTransducer, rowNum*dyTransducer, 0)
                
                Transducers[n, :] = (TransducerAux.x, TransducerAux.y, TransducerAux.z)
                Transducers[n+sizeHalf, :] = (TransducerAux1.x, TransducerAux1.y, TransducerAux1.z)

        return Transducers

        
    def getTransducers(self):
        configuration = self.configuration
        
        if(configuration == "hexagon"):
            numTransducers = 61
            Transducers = np.zeros((numTransducers, 3))       #define the Transducers' position: x, y, z
            acc = 0
            
            for n in range(5):
                Transducers = self.getRowHex(Transducers, 5+n, 5-n, acc)
                if n < 4:
                    Transducers = self.getRowHex(Transducers, 5+n, -(5-n), numTransducers-(5+n)-acc)
                acc = acc + 5 + n
            """
            #for easy revision when printing
            transducerNumbers = np.vstack(np.arange(numTransducers))
            np.set_printoptions(suppress=True)
            print(np.column_stack((transducerNumbers, Transducers)))
            """
            
TA = TransducerArray("hexagon")
TA.getTransducers()
        