from overrides import EnforceOverrides, overrides, final
from odbm.utils import extractParams, fmt
import pandas as pd
import numpy as np
import re

class InputError(Exception):
    pass

class Mechanism(EnforceOverrides):
    """
    A superclass class used to handle basic Mechansim functionality: format inputs and write equation.
    Other mechanism should inherint this class and override attributes and writeRate()

    Attributes
    ----------
    name : str
        label used to identify mechanism
    required_params : list
        list with parameter strings, default []
    nS : int
        number of required substrates, default np.nan
    nC : int
        number of required cofactors, default np.nan
    nP : int
        number of required products, default np.nan
    nE : int
        number of required enzymes, default np.nan

    Methods
    -------
    writeEquation():
        Writes chemical equations in form of 'S + C + E → E + P'

    writeRate():
        Writes rate of chemical reaction. This function should always be overriden.

    """

    # these variables should be overriden in new mechanisms
    name = 'base_mechanism'
    required_params = []
    nS = np.nan                  
    nC = np.nan
    nP = np.nan            
    nE = np.nan

    def __init__(self,rxn: pd.DataFrame):

        try:
            self.enzyme = rxn['Enzyme']
            self.substrates = rxn['Substrate']
            self.products = rxn['Product']
            self.cofactors = rxn['Cofactor']
            self.params = rxn['Parameters']
            self.label = rxn['Label']
        except:
            raise KeyError("Missing Reaction fields")

        self._processInput()
        self._formatInput()
    
    @final
    def _processInput(self):
        """
        Checks user model definition for errors.

        Raises:
            InputError: if missing required kinetic parameter for specified mechanism type
            InputError: if an incorrect number of enzymes, cofactors, substrates, or products are given 
                        for a specific mechanism type

        """
        # params
        self.params = extractParams(self.params)
        if not np.all([np.any([re.match(p,P) for P in self.params]) for p in self.required_params]):
            raise InputError("No "+' or '.join(self.required_params)+" found in parameters for reaction "+self.label)

        # cofactor
        if str(self.cofactors) != 'nan':
            self.cofactors = self.cofactors.split(';')
        else:
            self.cofactors = []
        if len(self.cofactors) != self.nC and np.isnan(self.nC) == False:
            raise InputError(str(len(self.cofactors))+' cofactor(s) found for a '+ str(self.nC) + ' cofactor mechanism in reaction '+self.label)

        # enzyme
        if str(self.enzyme) != 'nan':
            self.enzyme = self.enzyme.split(';')
        else:
            self.enzyme = []
        if len(self.enzyme) != self.nE and np.isnan(self.nE) == False:
            raise InputError(str(len(self.enzyme))+' enzyme(s) found for a '+ str(self.nE) + ' enzyme mechanism in reaction '+self.label)

        # substrates
        self.substrates = self.substrates.split(';')
        if len(self.substrates) != self.nS and np.isnan(self.nS) == False:
            raise InputError(str(len(self.substrates))+' substrate(s) found for a '+ str(self.nS) + ' substrate mechanism in reaction '+self.label)

        # products  
        self.products = self.products.split(';')
        if (not np.isnan(self.nP)) and (len(self.products) != self.nP):
            raise InputError(str(len(self.products))+' product(s) found for a '+ str(self.nP) + ' product mechanism in reaction '+self.label)
    
    @final
    def _formatInput(self):
        #calls fmt function in utils to format input strings to be antimony compatible 
        self.products = list(map(fmt, self.products))
        self.substrates = list(map(fmt, self.substrates))
        self.enzyme = list(map(fmt, self.enzyme))
        self.cofactors = list(map(fmt, self.cofactors))

    def writeEquation(self) -> str:
        """
        Writes chemical equations in form of S + C + E → E + P 

        Returns: 
        -------
        rxn_str (str) reaction equation in string format
        """
        
        allS = ' + '.join([*self.substrates,*self.cofactors])
        allE = ' + '.join(self.enzyme)
        allP = ' + '.join(self.products)

        if self.enzyme != 'nan' and self.enzyme != []:
            rxn_str = allS + ' + ' + allE + ' -> ' + allE + ' + '  + allP
        else: 
            rxn_str = allS + ' -> ' + allP

        return self.label +' : '+rxn_str
    
    def writeRate(self) -> str:
        """
        Writes rate of chemical reaction. This function should always be overriden.

        Returns
        -------
        str
        """
        pass

class MichaelisMenten(Mechanism):
    name = 'MM'                        # name for the mechanism
    required_params = ['kcat','Km']    # list of required parameters
    nS = 1                             # number of required substrates 
    nP = np.nan                        # number of required products 
    nE = 1                             # enzymatic reaction

    @overrides
    def writeRate(self) -> str:
        S = self.substrates
        E = self.enzyme[0]
        kcat,Km = [p+'_'+self.label for p in self.required_params]

        return self.label +' = '+ kcat + '*'+E+'*'+S[0]+'/('+Km+' + '+S[0]+')'
    
class OrderedBisubstrateBiproduct(Mechanism):
    # ordered bisubstrate-biproduct
    # must have two substrates and two products
    # https://iubmb.qmul.ac.uk/kinetics/ek4t6.html#p52
    # looks for kcat, Km1, Km2, K

    name = 'OBB'                                     # name for the mechanism
    required_params = ['kcat', 'Km1', 'Km2', 'K']    # list of required parameters
    nS = 2                                           # number of required substrates 
    nP = 2                                           # number of required products 
    nE = 1                                        # enzymatic reaction

    @overrides
    def writeRate(self) -> str:
        S = self.substrates
        E = self.enzyme[0]
        kcat,Km1,Km2,K = [p+'_'+self.label for p in self.required_params]

        return self.label +' = '+kcat+ '*'+E+'*'+(S[0])+'*'+(S[1])+'/(' \
                    +(S[0])+'*'+(S[1])+'+'+Km1+'*'+(S[1])+'+ '+Km2+'*'+(S[0])+'+'+ K+')'

class MassAction(Mechanism):
    name = 'MA'                                     # name for the mechanism
    required_params = ['k']                         # list of required parameters
    nS = np.nan                                     # number of required substrates 
    nP = np.nan                                     # number of required products 
    nE = np.nan                                      # enzymatic reaction

    # mass action kinetics
    @overrides
    def writeRate(self) -> str:
        rxn_str = 'k_' + self.label
        for p in self.substrates:
            if p[0].isnumeric():
                p = p[1:]+'^'+p[0]
            rxn_str += '*' + p 
        if self.enzyme != 'nan' and self.enzyme != []:
            rxn_str += '*'+(self.enzyme)

        return self.label +' = '+rxn_str

class simplifiedOBB(Mechanism):
    name = 'SOBB'                                     # name for the mechanism
    required_params = ['kcat', 'Km1', 'Km2']    # list of required parameters
    nS = 2                                           # number of required substrates 
    nP = 2                                           # number of required products 
    nE = 1                                        # enzymatic reaction

    @overrides
    def writeRate(self) -> str:
        S = self.substrates
        E = self.enzyme[0]
        kcat,Km1,Km2 = [p+'_'+self.label for p in self.required_params]

        return self.label +' = '+ kcat + '*'+E+'*'+(S[0])+'*'+(S[1])+'/(' \
                    +(S[0])+'*'+(S[1])+'+'+Km1+'*'+(S[1])+'+'+Km2+'*'+(S[0])+'+'+Km1+ '*' +Km2+')'

# class PI(Mechanism):
class TX_MM(MichaelisMenten):
    name = 'TX_MM'
    required_enzyme = 'RNAP'
    generate_label = lambda l: l+'_TX'
    generate_product = lambda s: s + ';' + s[:-3]+'RNA'

