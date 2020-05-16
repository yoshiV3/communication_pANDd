class Buffer:
    def __init__(self, nb_of_p):
        self.nb_of_p = nb_of_p
        self.buf     = [[] for x  in range(self.nb_of_p)]
        self.cr      = 0
        self.cw      = 0
        self.um      = 0
    def write(self,data):
        if (self.cw == self.cr) and self.um != 0:
            self.cr = (self.cr +1)%self.nb_of_p	
        else:
            self.um = self.um + 1	
        self.buf[self.cw] = data
        self.cw = (self.cw + 1)%self.nb_of_p
    def read(self):
        if self.um > 0:
        	self.um = self.um - 1
        	old     = self.cr
        	self.cr = (self.cr +1)%self.nb_of_p
        	return self.buf[old]
        else:
        	return None

