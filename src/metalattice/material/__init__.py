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
    """This class is used to define the material properties of the lattice.

    A dictionary of properties is passed to the class and the properties are
    set as attributes of the class.

    Attributes:
        name (str):
            name of the material

        type (str):
            type of material

        prop (dict):
            dictionary of properties

    Examples:

        A classical Cauchy material can be defined as follows:
    
        >>> steel = Material(
            name="Steel",
            type="Cauchy",
            prop={
                "E": 200e3,
                "nu": 0.3,
                "G": 0.0,
                "rho": 7.7e-9
            }
        )
        >>> steel.E
        200000.0
        >>> steel.nu
        0.3
        >>> steel.G
        0.0
        >>> steel.rho
        7.7e-09
    
        A micropolar material can be defined as follows:
    
        >>> steel = Material(
            name="Steel",
            type="Cosserat",
            prop={
                "E": 200e3,
                "nu": 0.3,
                "G": 0.0,
                "rho": 7.7e-9
            }
        )
    """
    def __init__(
        self,
        name:str = "Steel",
        type: str = "Cauchy",
        prop: dict = {
            "E": 200e3,
            "nu": 0.3,
            "G": 0.0,
            "rho": 7.7e-9,
        },
    ) -> None:
        """Inits Material with name, type and properties."""
        self. name = name
        self.type = type
        self.prop = prop
        for k, v in prop.items():
            setattr(self, k, v)
