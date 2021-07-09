import matplotlib.pyplot as plt
import pytest

from attractors import __version__
from attractors.attractor import ATTRACTOR_PARAMS, Attractor

SIMTIME = 10
SIMPOINTS = 10000


@pytest.fixture()
def attractor_obj_des(attr, des):
    obj = Attractor(attr)
    func = getattr(obj, des)
    func(0, SIMTIME, SIMPOINTS)
    return obj


@pytest.fixture
def attractor_obj_des_rk2(attr, rk2_method):
    obj = Attractor(attr)
    func = getattr(obj, "rk2")
    func(0, SIMTIME, SIMPOINTS, rk2_method)
    return obj


des_list = Attractor.list_des()
des_list.remove("rk2")


@pytest.mark.parametrize("attr", Attractor.list_attractors())
@pytest.mark.parametrize("des", des_list)
def test_attractors_des(attr, attractor_obj_des):
    attrparams = ATTRACTOR_PARAMS[attr]
    assert len(attractor_obj_des) == SIMPOINTS
    assert attractor_obj_des.init_coord == attrparams["init_coord"]
    for i in range(len(attrparams["params"])):
        assert (
            getattr(attractor_obj_des, attrparams["params"][i])
            == attrparams["default_params"][i]
        )


@pytest.mark.parametrize("attr", Attractor.list_attractors())
@pytest.mark.parametrize("rk2_method", ["heun", "imp_poly", "ralston"])
def test_attractors_des_rk2(attr, attractor_obj_des_rk2):
    attrparams = ATTRACTOR_PARAMS[attr]
    assert len(attractor_obj_des_rk2) == SIMPOINTS
    assert attractor_obj_des_rk2.init_coord == attrparams["init_coord"]
    for i in range(len(attrparams["params"])):
        assert (
            getattr(attractor_obj_des_rk2, attrparams["params"][i])
            == attrparams["default_params"][i]
        )


@pytest.mark.parametrize("attr", Attractor.list_attractors())
@pytest.mark.parametrize("type", ["multipoint", "gradient"])
def test_fig_defaults(attr, type):
    attrparams = ATTRACTOR_PARAMS[attr]
    obj = Attractor(attr)
    obj.rk4(0, SIMTIME, SIMPOINTS)
    animfunc = getattr(Attractor, f"set_animate_{type}")
    animfunc(obj)
    assert list(Attractor.ax.get_xlim()) == attrparams["xlim"]
    assert list(Attractor.ax.get_ylim()) == attrparams["ylim"]
    assert list(Attractor.ax.get_zlim()) == attrparams["zlim"]
    plt.close(Attractor.fig)
