"""
======================================
Material (:mod:`metalattice.material`)
======================================

.. currentmodule:: metalattice.material

Classes
-------

.. autosummary::
    :toctree: generated/

    Material
"""

class Material:
    """
    The base material of a lattice.

    A dictionary of properties is passed to the class and the properties are
    set as attributes of the class.

    Attributes:
        name (str):
            name of the material

        type (str):
            type of material

        prop (dict):
            dictionary of properties        
        
        ... (Any):
            additional properties from the dictionary **prop**
    
    Parameters:
        name (str):
            name of the material

        type (str):
            type of material

        prop (dict):
            dictionary of properties

    Examples:

        A classical Cauchy material could be defined as follows:
    
        >>> from metalattice.material import Material
        >>> steel = Material(
            name="Steel",
            type="Cauchy",
            prop={
                "E": 200e3,
                "nu": 0.3,
                "rho": 7.7e-9,
            }
        )
        >>> steel.E
        200000.0
        >>> steel.nu
        0.3
        >>> steel.G
        76923.07692307692
        >>> steel.rho
        7.7e-09
    
        A micropolar material can be defined as follows:
    
        >>> import numpy as np
        >>> from metalattice.material import Material
        >>> meta = Material(
            name="Lattice Metamaterial",
            type="Cosserat",
            prop={
                "D": np.zeros((18, 18)),
            }
        )
        >>> meta.D
        array([[0., 0., 0., ..., 0., 0., 0.],
               [0., 0., 0., ..., 0., 0., 0.],
               [0., 0., 0., ..., 0., 0., 0.],
               ...,
               [0., 0., 0., ..., 0., 0., 0.],
               [0., 0., 0., ..., 0., 0., 0.],
               [0., 0., 0., ..., 0., 0., 0.]])
    """
    def __init__(
        self,
        name:str = "Steel",
        type: str = "Cauchy",
        prop: dict = {
            "E": 200e3,
            "nu": 0.3,
            "rho": 7.7e-9,
        },
    ) -> None:
        """Inits Material with name, type and properties."""
        self. name = name
        self.type = type
        self.prop = prop
        for k, v in prop.items():
            setattr(self, k, v)
        
        if type in ["Cauchy", "Classical"] and "G" not in prop.keys():
            assert hasattr(self, "E") and hasattr(self, "nu"), "E and nu are required for Cauchy materials."
            self.G = self.E / (2 * (1 + self.nu))
