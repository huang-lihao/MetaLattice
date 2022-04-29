"""
Abstract base class for FEM element Classes.

ElementBase stores the basic FEM info.
"""
from math import prod
from typing import Sequence
import numpy as np

__all__ = [
    "ElementBase",
    "GaussianIntElement",
]


class ElementBase(object):
    """An abstract base class for FEM element Classes.

    ElementBase stores the basic FEM info.

    Parameters
    ----------
    nodes : (num_node, dof) array_like
        coordinates of nodes in the element.
    ele_type : str
        the element type string.
    lumped : bool
        lumped mass matrix or not.
    """

    def __init__(
        self,
        nodes: np.ndarray,
        ele_type: str = None,
        lumped: bool = True,
    ) -> None:
        self.nodes = nodes
        num_node, num_coord = nodes.shape
        self.num_node = num_node
        self.num_coord = num_coord
        self.ele_type = ele_type
        self.lumped = lumped

        self._stiff_mat: np.ndarray = None
        self._mass_mat: np.ndarray = None
        self.intp_parrent_coord: np.ndarray = None

    @property
    def stiff_mat(self):
        """
        element stiffness matrix
        """
        if self._stiff_mat is None:
            raise NotImplementedError("stiff_mat: not implemented")
        return self._stiff_mat

    @stiff_mat.setter
    def stiff_mat(self, value):
        self._stiff_mat = value

    @property
    def mass_mat(self):
        """
        element mass matrix
        """
        if self._mass_mat is None:
            raise NotImplementedError("mass_mat: not implemented")
        return self._mass_mat

    @mass_mat.setter
    def mass_mat(self, value):
        self._mass_mat = value


class GaussianIntElement(ElementBase):
    r"""An abstract base class for Gaussian integral element Classes.

    .. math::

        \mathbf{K} = \Sigma_p \mathbf{B}^T \mathbf{D} \mathbf{B}  w J

        \mathbf{M} = \Sigma_p \mathbf{N}^T \mathbf{P} \mathbf{N}  w J
    
    Parameters
    ----------
    nodes : (num_node, dof) array_like
        coordinates of nodes in the element.
    ele_type : str
        the element type string.
    lumped : bool
        lumped mass matrix or not.
    """

    def __init__(self,
                 nodes: np.ndarray,
                 ele_type: str = None,
                 num_intp_per_dir: Sequence[int] = (2, 2, 2),
                 lumped: bool = True) -> None:
        super().__init__(nodes, ele_type, lumped)
        self.num_intp_per_dir = num_intp_per_dir
        self.num_intp = prod(num_intp_per_dir)

        self.dof: int = None
        self.intps: dict = None

        self._weight: np.ndarray = None
        self._shape_func: np.ndarray = None
        self._grad_shape_func: np.ndarray = None
        self._N_mat: np.ndarray = None
        self._jacobi: np.ndarray = None
        self._det_J: np.ndarray = None
        self._B_mat: np.ndarray = None
        self._D_mat: np.ndarray = None
        self._P_mat: np.ndarray = None

    @property
    def weight(self) -> np.ndarray:
        if self._weight is None:
            raise NotImplementedError("weight: not implemented")
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def shape_func(self) -> np.ndarray:
        if self._shape_func is None:
            raise NotImplementedError("shape_func: not implemented")
        return self._shape_func

    @shape_func.setter
    def shape_func(self, value):
        self._shape_func = value

    @property
    def grad_shape_func(self) -> np.ndarray:
        if self._grad_shape_func is None:
            raise NotImplementedError("grad_shape_func: not implemented")
        return self._grad_shape_func

    @grad_shape_func.setter
    def grad_shape_func(self, value):
        self._grad_shape_func = value

    @property
    def N_mat(self) -> np.ndarray:
        if self._N_mat is None:
            N = self.shape_func
            N_mat = np.block([[
                N if i == j else np.zeros_like(N)
                for j in range(self.num_coord)
            ] for i in range(self.num_coord)])
            N_mat = N_mat.reshape(
                (self.dof, self.num_intp, self.dof, self.num_node))
            N_mat = N_mat.transpose(1, 0, 3, 2)
            N_mat = N_mat.reshape((self.num_intp, self.dof, -1))
            self._N_mat = N_mat
        return self._N_mat

    @N_mat.setter
    def N_mat(self, value):
        self._N_mat = value

    @property
    def jacobi(self) -> np.ndarray:
        if self._jacobi is None:
            # J is $\frac{\partial \xi_i}{ \partial x_j}$
            J = np.einsum(self.grad_shape_func, [0, 1, 2], self.nodes, [2, 3])
            self._jacobi = J

        return self._jacobi

    @N_mat.setter
    def jacobi(self, value):
        self._jacobi = value

    @property
    def det_J(self) -> np.ndarray:
        if self._det_J is None:
            J = self.jacobi
            self._det_J = np.linalg.det(J)
        return self._det_J

    @det_J.setter
    def det_J(self, value):
        self._det_J = value

    @property
    def B_mat(self) -> np.ndarray:
        if self._B_mat is None:
            raise NotImplementedError("B_mat: not implemented")
        return self._B_mat

    @B_mat.setter
    def B_mat(self, value):
        self._B_mat = value

    @property
    def D_mat(self) -> np.ndarray:
        if self._D_mat is None:
            raise NotImplementedError("D_mat: not implemented")
        return self._D_mat

    @D_mat.setter
    def D_mat(self, value):
        self._D_mat = value

    @property
    def P_mat(self) -> np.ndarray:
        if self._P_mat is None:
            raise NotImplementedError("D_mat: not implemented")
        return self._P_mat

    @P_mat.setter
    def P_mat(self, value):
        self._P_mat = value

    @property
    def stiff_mat(self):
        """
        Element stiffness matrix.

        .. math::

            \mathbf{K} = \Sigma_p \mathbf{B}^T \mathbf{D} \mathbf{B}  w J

        """
        if self._stiff_mat is None:
            self._stiff_mat = sum([
                np.einsum(
                    B,
                    [1, 0],
                    D,
                    [1, 2],
                    B,
                    [2, 3],
                ) * w * det for B, D, w, det in zip(self.B_mat, self.D_mat,
                                                    self.weight, self.det_J)
            ])
        return self._stiff_mat

    @stiff_mat.setter
    def stiff_mat(self, value):
        self._stiff_mat = value

    @property
    def mass_mat(self):
        """
        Element mass matrix.

        .. math::
            \mathbf{M} = \Sigma_p \mathbf{N}^T \mathbf{P} \mathbf{N}  w J
        
        """
        if self._mass_mat is None:
            self._mass_mat = sum([
                np.einsum(
                    N,
                    [1, 0],
                    P,
                    [1, 2],
                    N,
                    [2, 3],
                ) * w * det for N, P, w, det in zip(
                    self.shape_func, self.P_mat, self.weight, self.det_J)
            ])
            if self.lumped:
                self._mass_mat = np.diag(self._mass_mat.sum(axis=0))
        return self._mass_mat

    @mass_mat.setter
    def mass_mat(self, value):
        self._mass_mat = value
