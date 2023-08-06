# coding=utf-8
# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""A Jax version of Sinkhorn's algorithm."""

import collections
import functools
from typing import Any
from typing import Optional, Sequence, Tuple, Callable

import jax
import jax.numpy as jnp
import numpy as np
from ott.core import fixed_point_loop
from ott.geometry import geometry

SinkhornOutput = collections.namedtuple(
    'SinkhornOutput', ['f', 'g', 'reg_ot_cost', 'errors', 'converged'])


def sinkhorn(
    geom: geometry.Geometry,
    a: Optional[jnp.ndarray] = None,
    b: Optional[jnp.ndarray] = None,
    tau_a: float = 1.0,
    tau_b: float = 1.0,
    threshold: float = 1e-3,
    norm_error: int = 1,
    inner_iterations: int = 10,
    min_iterations: int = 0,
    max_iterations: int = 2000,
    momentum: float = 1.0,
    chg_momentum_from: int = 0,
    anderson_acceleration: int = 0,
    refresh_anderson_frequency: int = 1,
    lse_mode: bool = True,
    implicit_differentiation: bool = True,
    implicit_solver_fun=jax.scipy.sparse.linalg.cg,
    implicit_solver_ridge_kernel: float = 0.0,
    implicit_solver_ridge_identity: float = 0.0,
    implicit_solver_symmetric: bool = False,
    precondition_fun: Optional[Callable[[float], float]] = None,
    parallel_dual_updates: bool = False,
    use_danskin: bool = None,
    init_dual_a: Optional[jnp.ndarray] = None,
    init_dual_b: Optional[jnp.ndarray] = None,
    jit: bool = False) -> SinkhornOutput:
  r"""Solves regularized OT problem using Sinkhorn iterations.

  The Sinkhorn algorithm is a fixed point iteration that solves a regularized
  optimal transport (reg-OT) problem between two measures.
  The optimization variables are a pair of vectors (called potentials, or
  scalings when parameterized as exponentials of the former). Calling this
  function returns therefore a pair of optimal vectors. In addition to these,
  `sinkhorn` also returns the objective value achieved by these optimal vectors;
  a vector of size `max_iterations/inner_terations` that records the vector of
  values recorded to monitor convergence, throughout the execution of the
  algorithm (padded with ``-1`` if convergence happens before), as well as a
  boolean to signify whether the algorithm has converged within the number of
  iterations specified by the user.

  The reg-OT problem is specified by two measures, of respective sizes ``n`` and
  ``m``. From the viewpoint of the ``sinkhorn`` function, these two measures are
  only seen through a triplet (``geom``, ``a``, ``b``), where ``geom`` is a
  ``Geometry`` object, and ``a`` and ``b`` are weight vectors of respective
  sizes ``n`` and ``m``. Starting from two initial values for those potentials
  or scalings (both can be defined by the user by passing value in
  ``init_dual_a`` or ``init_dual_b``), the Sinkhorn algorithm will use
  elementary operations that are carried out by the ``geom`` object.

  Some maths:
    Given a geometry ``geom``, which provides a cost matrix :math:`C` with its
    regularization parameter :math:`\epsilon`, (resp. a kernel matrix :math:`K`)
    the reg-OT problem consists in finding two vectors `f`, `g` of size ``n``,
    ``m`` that maximize the following criterion.

    :math:`\arg\max_{f, g}{- <a, \phi_a^{*}(-f)> - <b, \phi_b^{*}(-g)> - \epsilon
    <e^{f/\epsilon}, e^{-C/\epsilon} e^{-g/\epsilon}}>`

    where :math:`\phi_a(z) = \rho_a z(\log z - 1)` is a scaled entropy, and
    :math:`\phi_a^{*}(z) = \rho_a e^{z/\varepsilon}` its Legendre transform.

    That problem can also be written, instead, using positive scaling vectors
    `u`, `v` of size ``n``, ``m``, handled with the kernel :math:`K:=e^{-C/\epsilon}`,
    :math:`\arg\max_{u, v >0} - <a,\phi_a^{*}(-\epsilon\log u)> + <b, \phi_b^{*}(-\epsilon\log v)> -  <u, K
    v>`

    Both of these problems corresponds, in their *primal* formulation, to solving the
    unbalanced optimal transport problem with a variable matrix `P` of size ``n``
    x ``m``:

    :math:`\arg\min_{P>0} <P,C> -\epsilon \text{KL}(P | ab^T) + \rho_a \text{KL}(P1 | a) + \rho_b \text{KL}(P^T1 | b)`

    where :math:`KL` is the generalized Kullback-Leibler divergence.

    The very same primal problem can also be written using a kernel :math:`K`
    instead of a cost :math:`C` as well:

    :math:`\arg\min_{P} \epsilon KL(P|K) + \rho_a \text{KL}(P1 | a) + \rho_b \text{KL}(P^T1 | b)`

    The *original* OT problem taught in linear programming courses is recovered
    by using the formulation above relying on the cost :math:`C`, and letting
    :math:`\epsilon \rightarrow 0`, and :math:`\rho_a, \rho_b \rightarrow \infty`.
    In that case the entropy disappears, whereas the :math:`KL` regularizations
    above become constraints on the marginals of :math:`P`: This results in a
    standard min cost flow problem. This problem is not handled for now in this
    toolbox, which focuses exclusively on the case :math:`\epsilon > 0`.

    The *balanced* regularized OT problem is recovered for finite
    :math:`\epsilon > 0` but letting :math:`\rho_a, \rho_b \rightarrow \infty`.
    This problem can be shown to be equivalent to a matrix scaling problem,
    which can be solved using the Sinkhorn fixed-point algorithm. To handle the
    case :math:`\rho_a, \rho_b \rightarrow \infty`, the ``sinkhorn`` function
    uses parameters ``tau_a`` := :math:`\rho_a / (\epsilon + \rho_a)` and
    ``tau_b`` := :math:`\rho_b / (\epsilon + \rho_b)` instead.
    Setting either of these parameters to 1 corresponds to setting the
    corresponding :math:`\rho_a, \rho_b` to :math:`\infty`.

    The Sinkhorn algorithm solves the reg-OT problem by seeking optimal `f`, `g`
    potentials (or alternatively their parameterization as positive scalings `u`,
    `v`), rather than solving the primal problem in :math:`P`. This is mostly for
    efficiency (potentials and scalings have a ``n + m`` memory footprint, rather
    than ``n m`` required to store `P`). This is also because both problems are,
    in fact, equivalent, since the optimal transport :math:`P^*` can be recovered
    from optimal potentials :math:`f^*`, :math:`g^*` or scalings :math:`u^*`,
    :math:`v^*`, using the geometry's cost or kernel matrix respectively:

      :math:`P^* = \exp\left(\frac{f^*\mathbf{1}_m^T + \mathbf{1}_n g^{*T} - C}{\epsilon}\right) \text{ or } P^* =
      \text{diag}(u^*) K \text{diag}(v^*)`

    By default, the Sinkhorn algorithm solves this dual problem in `f, g` or
    `u, v` using block coordinate ascent, i.e. devising an update for each `f`
    and `g` (resp. `u` and `v`) that cancels their respective gradients, one at
    a time. These two iterations are repeated ``inner_iterations`` times, after
    which the norm of these gradients will be evaluated and compared with the
    ``threshold`` value. The iterations are then repeated as long as that error
    exceeds ``threshold``.

  Note on Sinkhorn updates:
    The boolean flag ``lse_mode`` sets whether the algorithm is run in either:

      - log-sum-exp mode (``lse_mode=True``), in which case it is directly defined in terms of updates to `f` and `g`, using log-sum-exp computations. This requires access to the cost matrix :math:`C`, as it is stored, or possibly computed on the fly by ``geom``.

      - kernel mode (``lse_mode=False``), in which case it will require access to a matrix vector multiplication operator :math:`z \rightarrow K z`, where :math:`K` is either instantiated from :math:`C` as :math:`\exp(-C/\epsilon)`, or provided directly. In that case, rather than optimizing on :math:`f` and :math:`g`, it is more convenient to optimize on their so called scaling formulations, :math:`u := \exp(f / \epsilon)` and :math:`v := \exp(g / \epsilon)`. While faster (applying matrices is faster than applying ``lse`` repeatedly over lines), this mode is also less stable numerically, notably for smaller :math:`\epsilon`.

    In the source code, the variables ``f_u`` or ``g_v`` can be either regarded as potentials (real) or scalings (positive) vectors, depending on the choice of ``lse_mode`` by the user. Once optimization is carried out, we only return dual variables in potential form, i.e. ``f`` and ``g``.

    In addition to standard Sinkhorn updates, the user can also use heavy-ball type updates using a ``momentum`` parameter in ]0,2[. We also implement a strategy that tries to set that parameter adaptively ater ``chg_momentum_from`` iterations, as a function of progress in the error, as proposed in the literature.

    Another upgrade to the standard Sinkhorn updates provided to the users lies in using Anderson acceleration. This can be parameterized by setting the otherwise null ``anderson_acceleration`` to a positive integer. When selected,the algorithm will recompute, every ``refresh_anderson_frequency`` (set by default to 1) an extrapolation of the most recently computed ``anderson_acceleration`` iterates. When using that option, notice that differentiation (if required) can only be carried out using implicit differentiation, and that all momentum related parameters are ignored.

    The ``parallel_dual_updates`` flag is set to ``False`` by default. In that setting, ``g_v`` is first updated using the latest values for ``f_u`` and ``g_v``, before proceeding to update ``f_u`` using that new value for ``g_v``. When the flag is set to ``True``, both ``f_u`` and ``g_v`` are updated simultaneously. Note that setting that choice to ``True`` requires using some form of averaging (e.g. ``momentum=0.5``). Without this, and on its own ``parallel_dual_updates`` won't work.

  Differentiation:
    The optimal solutions ``f`` and ``g`` and the optimal objective (``reg_ot_cost``) outputted by the Sinkhorn algorithm can be differentiated w.r.t. relevant inputs ``geom``, ``a`` and ``b`` using, by default, implicit differentiation of the optimality conditions (``implicit_differentiation`` set to ``True``). This choice has two consequences.

      - The termination criterion used to stop Sinkhorn (cancellation of gradient of objective w.r.t. ``f_u`` and ``g_v``) is used to differentiate ``f`` and ``g``, given a change in the inputs. These changes are computed by solving a linear system. The arguments starting with ``implicit_solver_*`` allow to define the linear solver that is used, and to control for two types or regularization (we have observed that, depending on the architecture, linear solves may require higher ridge parameters to remain stable). The optimality conditions in Sinkhorn can be analyzed as satisfying a ``z=z'`` condition, which are then differentiated. It might be beneficial (e.g. as in https://arxiv.org/abs/2002.03229) to use a preconditionning function ``precondition_fun`` to differentiate instead ``h(z)=h(z')``.

      - The objective ``reg_ot_cost`` returned by Sinkhon uses the so-called enveloppe (or Danskin's) theorem. In that case, because it is assumed that the gradients of the dual variables ``f_u`` and ``g_v`` w.r.t. dual objective are zero (reflecting the fact that they are optimal), small variations in ``f_u`` and ``g_v`` due to changes in inputs (such as ``geom``, ``a`` and ``b``) are considered negligible. As a result, ``stop_gradient`` is applied on dual variables ``f_u`` and ``g_v`` when evaluating the ``reg_ot_cost`` objective. Note that this approach is `invalid` when computing higher order derivatives. In that case the ``use_danskin`` flag must be set to ``False``.

    An alternative yet more costly way to differentiate the outputs of the Sinkhorn iterations is to use unrolling, i.e. reverse mode differentiation of the Sinkhorn loop. This is possible because Sinkhorn iterations are wrapped in a custom fixed point iteration loop, defined in ``fixed_point_loop``, rather than a standard while loop. This is to ensure the end result of this fixed point loop can also be differentiated, if needed, using standard JAX operations. To ensure backprop differentiability, the ``fixed_point_loop.fixpoint_iter_backprop`` loop does checkpointing of state variables (here ``f_u`` and ``g_v``) every ``inner_iterations``, and backpropagates automatically, block by block, through blocks of ``inner_iterations`` at a time.

  Note:
    * The Sinkhorn algorithm may not converge within the maximum number of iterations for possibly several reasons:

      1. the regularizer (defined as ``epsilon`` in the geometry ``geom`` object) is too small. Consider either switching to ``lse_mode=True`` (at the price of a slower execution), increasing ``epsilon``, or, alternatively, if you are unable or unwilling to increase  ``epsilon``, either increase ``max_iterations`` or ``threshold``.
      2. the probability weights ``a`` and ``b`` do not have the same total mass, while using a balanced (``tau_a=tau_b=1.0``) setup. Consider either normalizing ``a`` and ``b``, or set either ``tau_a`` and/or ``tau_b<1.0``.
      3. OOMs issues may arise when storing either cost or kernel matrices that are too large in ``geom``. In the case where, the ``geom`` geometry is a ``PointCloud``, some of these issues might be solved by setting the ``online`` flag to ``True``. This will trigger a recomputation on the fly of the cost/kernel matrix.

    * The weight vectors ``a`` and ``b`` can be passed on with coordinates that have zero weight. This is then handled by relying on simple arithmetic for ``inf`` values that will likely arise (due to :math:`log(0)` when ``lse_mode`` is ``True``, or divisions by zero when ``lse_mode`` is ``False``). Whenever that arithmetic is likely to produce ``NaN`` values (due to ``-inf * 0``, or ``-inf - -inf``) in the forward pass, we use ``jnp.where`` conditional statements to carry ``inf`` rather than ``NaN`` values. In the reverse mode differentiation, the inputs corresponding to these 0 weights (a location `x`, or a row in the corresponding cost/kernel matrix), and the weight itself will have ``NaN`` gradient values. This is reflects that these gradients are undefined, since these points were not considered in the optimization and have therefore no impact on the output.

  Args:
    geom: a Geometry object.
    a: [num_a,] or [batch, num_a] weights.
    b: [num_b,] or [batch, num_b] weights.
    tau_a: ratio rho/(rho+eps) between KL divergence regularizer to first
     marginal and itself + epsilon regularizer used in the unbalanced
     formulation.
    tau_b: ratio rho/(rho+eps) between KL divergence regularizer to first
     marginal and itself + epsilon regularizer used in the unbalanced
     formulation.
    threshold: tolerance used to stop the Sinkhorn iterations. This is
     typically the deviation between a target marginal and the marginal of the
     current primal solution when either or both tau_a and tau_b are 1.0
     (balanced or semi-balanced problem), or the relative change between two
     successive solutions in the unbalanced case.
    norm_error: power used to define p-norm of error for marginal/target.
    inner_iterations: the Sinkhorn error is not recomputed at each
     iteration but every inner_num_iter instead.
    min_iterations: the minimum number of Sinkhorn iterations carried
     out before the error is computed and monitored.
    max_iterations: the maximum number of Sinkhorn iterations. If
      ``max_iterations`` is equal to ``min_iterations``, sinkhorn iterations are
      run by default using a ``jax.lax.scan`` loop rather than a custom,
      unroll-able ``jax.lax.while_loop`` that monitors convergence. In that case
      the error is not monitored and the ``converged`` flag will return
      ``False`` as a consequence.
    momentum: a float in ]0,2[
    chg_momentum_from: if positive, momentum is recomputed using the
      adaptive rule provided in https://arxiv.org/pdf/2012.12562v1.pdf after
      that number of iterations.
    anderson_acceleration: int, if 0 (default), no acceleration. If positive,
      use Anderson acceleration on the dual sinkhorn (in log/potential form), as
      described in https://en.wikipedia.org/wiki/Anderson_acceleration and
      advocated in https://arxiv.org/abs/2006.08172, with a memory of size equal
      to ``anderson_acceleration``. In that case, differentiation is
      necessarly handled implicitly (``implicit_differentiation`` is set to
      ``True``) and all ``momentum`` related parameters are ignored.
    refresh_anderson_frequency: int, when using ``anderson_acceleration``,
      recompute direction periodically every int sinkhorn iterations.
    lse_mode: ``True`` for log-sum-exp computations, ``False`` for kernel
      multiplication.
    implicit_differentiation: ``True`` if using implicit differentiation,
      ``False`` if unrolling Sinkhorn iterations.
    implicit_solver_fun: see ``solve_implicit_system``
    implicit_solver_ridge_kernel: see ``solve_implicit_system``
    implicit_solver_ridge_identity: see ``solve_implicit_system``
    implicit_solver_symmetric: see ``solve_implicit_system``
    precondition_fun: Callable to modify FOC before differentiating them in
      implicit differentiation.
    parallel_dual_updates: updates potentials or scalings in parallel if True,
      sequentially (in Gauss-Seidel fashion) if False.
    use_danskin: when ``True``, it is assumed the entropy regularized cost is
      is evaluated using optimal potentials that are freezed, i.e. whose
      gradients have been stopped. This is useful when carrying out first order
      differentiation, and is only valid (as with ``implicit_differentiation``)
      when the algorithm has converged with a low tolerance.
    init_dual_a: optional initialization for potentials/scalings w.r.t.
      first marginal (``a``) of reg-OT problem.
    init_dual_b: optional initialization for potentials/scalings w.r.t.
      second marginal (``b``) of reg-OT problem.
    jit: if True, automatically jits the function upon first call.
      Should be set to False when used in a function that is jitted by the user,
      or when computing gradients (in which case the gradient function
      should be jitted by the user)

  Returns:
    a ``SinkhornOutput`` named tuple. The tuple contains two optimal potential
    vectors ``f`` and ``g``, the objective ``reg_ot_cost`` evaluated at those
    solutions, an array of ``errors`` to monitor convergence every
    ``inner_iterations`` and a flag ``converged`` that is ``True`` if the
    algorithm has converged within the number of iterations that was predefined
    by the user.
  """
  # Start by checking inputs.
  num_a, num_b = geom.shape
  a = jnp.ones((num_a,)) / num_a if a is None else a
  b = jnp.ones((num_b,)) / num_b if b is None else b

  if init_dual_a is None:
    init_dual_a = jnp.zeros_like(a) if lse_mode else jnp.ones_like(a)

  if init_dual_b is None:
    init_dual_b = jnp.zeros_like(b) if lse_mode else jnp.ones_like(b)

  if precondition_fun is None:
    precondition_fun = lambda x: geom.epsilon * jnp.log(x)

  # Cancel dual variables for zero weights.
  init_dual_a = jnp.where(a > 0, init_dual_a, -jnp.inf if lse_mode else 0.0)
  init_dual_b = jnp.where(b > 0, init_dual_b, -jnp.inf if lse_mode else 0.0)

  # Force implicit_differentiation to True when using Anderson acceleration,
  # Reset all momentum parameters.
  if anderson_acceleration:
    implicit_differentiation = True
    momentum = 1.0
    chg_momentum_from = 0

  # To change momentum adaptively, one needs errors in ||.||_1 norm.
  # In that case, we add this exponent to the list of errors to compute,
  # notably if that was not the error requested by the user.
  if chg_momentum_from > 0 and norm_error != 1:
    norm_error = (norm_error, 1)
  else:
    norm_error = (norm_error,)

  if jit:
    call_to_sinkhorn = functools.partial(
        jax.jit, static_argnums=(3, 4, 6, 7, 8, 9) + tuple(range(11, 23)))(
            _sinkhorn)
  else:
    call_to_sinkhorn = _sinkhorn
  return call_to_sinkhorn(geom, a, b, tau_a, tau_b, threshold, norm_error,
                          inner_iterations, min_iterations, max_iterations,
                          momentum, chg_momentum_from, anderson_acceleration,
                          refresh_anderson_frequency,
                          lse_mode, implicit_differentiation,
                          implicit_solver_fun,
                          implicit_solver_ridge_kernel,
                          implicit_solver_ridge_identity,
                          implicit_solver_symmetric,
                          precondition_fun,
                          parallel_dual_updates,
                          use_danskin, init_dual_a, init_dual_b)


def _sinkhorn(
    geom: geometry.Geometry,
    a: jnp.ndarray,
    b: jnp.ndarray,
    tau_a: float,
    tau_b: float,
    threshold: float,
    norm_error: int,
    inner_iterations: int,
    min_iterations: int,
    max_iterations: int,
    momentum: float,
    chg_momentum_from: int,
    anderson_acceleration: int,
    refresh_anderson_frequency: int,
    lse_mode: bool,
    implicit_differentiation: bool,
    implicit_solver_fun: Callable,
    implicit_solver_ridge_kernel: float,
    implicit_solver_ridge_identity: float,
    implicit_solver_symmetric: bool,
    precondition_fun: Callable[[float], float],
    parallel_dual_updates: bool,
    use_danskin: bool,
    init_dual_a: jnp.ndarray,
    init_dual_b: jnp.ndarray) -> SinkhornOutput:
  """Forks between implicit/backprop exec of Sinkhorn."""

  if implicit_differentiation:
    iteration_fun = _sinkhorn_iterations_implicit
  else:
    iteration_fun = _sinkhorn_iterations

  # By default, use Danskin theorem to differentiate
  # the objective when using implicit_differentiation.
  use_danskin = implicit_differentiation if use_danskin is None else use_danskin

  f, g, errors = iteration_fun(
      tau_a, tau_b, inner_iterations, min_iterations, max_iterations,
      chg_momentum_from, anderson_acceleration, refresh_anderson_frequency,
      lse_mode, implicit_differentiation, implicit_solver_fun,
      implicit_solver_ridge_kernel, implicit_solver_ridge_identity,
      implicit_solver_symmetric, precondition_fun,
      parallel_dual_updates, init_dual_a, init_dual_b, momentum, threshold,
      norm_error, geom, a, b)

  # When differentiating the regularized OT cost, and assuming Sinkhorn has run
  # to convergence, Danskin's (or the enveloppe) theorem
  # https://en.wikipedia.org/wiki/Danskin%27s_theorem
  # states that the resulting OT cost as a function of any of the inputs
  # (``geometry``, ``a``, ``b``) behaves locally as if the dual optimal
  # potentials were frozen and did not vary with those inputs.
  #
  # Notice this is only valid, as when using ``implicit_differentiation`` mode,
  # if the Sinkhorn algorithm outputs potentials that are near optimal.
  # namely when the threshold value is set to a small tolerance.
  #
  # The flag ``use_danskin`` controls whether that assumption is made. By
  # default, that flag is set to the value of ``implicit_differentiation`` if
  # not specified. If you wish to compute derivatives of order 2 and above,
  # set ``use_danskin`` to ``False``.
  reg_ot_cost = ent_reg_cost(geom, a, b, tau_a, tau_b,
                             jax.lax.stop_gradient(f) if use_danskin else f,
                             jax.lax.stop_gradient(g) if use_danskin else g,
                             lse_mode)
  converged = jnp.logical_and(
      jnp.sum(errors == -1) > 0,
      jnp.sum(jnp.isnan(errors)) == 0)

  return SinkhornOutput(f, g, reg_ot_cost, errors, converged)


def _sinkhorn_iterations(
    tau_a: float,
    tau_b: float,
    inner_iterations: int,
    min_iterations: int,
    max_iterations: int,
    chg_momentum_from: int,
    anderson_acceleration: int,
    refresh_anderson_frequency: int,
    lse_mode: bool,
    implicit_differentiation: bool,
    implicit_solver_fun: Callable,
    implicit_solver_ridge_kernel: float,
    implicit_solver_ridge_identity: float,
    implicit_solver_symmetric: bool,
    precondition_fun: Callable[[float], float],
    parallel_dual_updates: bool,
    init_dual_a: jnp.ndarray,
    init_dual_b: jnp.ndarray,
    momentum: float,
    threshold: float,
    norm_error: Sequence[int],
    geom: geometry.Geometry,
    a: jnp.ndarray,
    b: jnp.ndarray) -> Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray]:
  r"""A jit'able Sinkhorn loop.

  For a detailed explanation of args, see parent function ``sinkhorn``
  Args:
    tau_a: float, ratio lam/(lam+eps) between KL divergence regularizer to first
      marginal and itself + epsilon regularizer used in the unbalanced
      formulation.
    tau_b: float, ratio lam/(lam+eps) between KL divergence regularizer to first
      marginal and itself + epsilon regularizer used in the unbalanced
      formulation.
    inner_iterations: (int32) the Sinkhorn error is not recomputed at each
      iteration but every inner_num_iter instead.
    min_iterations: (int32) the minimum number of Sinkhorn iterations.
    max_iterations: (int32) the maximum number of Sinkhorn iterations.
    chg_momentum_from: int, # of iterations after which momentum is computed
    anderson_acceleration: int, memory size for anderson acceleration.
    refresh_anderson_frequency: int, used every iterations to refresh.
    lse_mode: True for log-sum-exp computations, False for kernel
      multiplication.
    implicit_differentiation: if True, do not backprop through the Sinkhorn
      loop, but use the implicit function theorem on the fixed point optimality
      conditions.
    implicit_solver_fun: see ``solve_implicit_system``
    implicit_solver_ridge_kernel: see ``solve_implicit_system``
    implicit_solver_ridge_identity: see ``solve_implicit_system``
    implicit_solver_symmetric: see ``solve_implicit_system``
    precondition_fun: preconditioning function to stabilize FOC system.
    parallel_dual_updates: updates potentials or scalings in parallel if True,
      sequentially (in Gauss-Seidel fashion) if False.
    init_dual_a: optional initialization for potentials/scalings w.r.t. first
      marginal (``a``) of reg-OT problem.
    init_dual_b: optional initialization for potentials/scalings w.r.t. second
      marginal (``b``) of reg-OT problem.
    momentum: float, a float between ]0,2[
    threshold: (float) the relative threshold on the Sinkhorn error to stop the
      Sinkhorn iterations.
    norm_error: t-uple of int, p-norms of marginal / target errors to track
    geom: a Geometry object.
    a: jnp.ndarray<float>[num_a,] or jnp.ndarray<float>[batch,num_a] weights.
    b: jnp.ndarray<float>[num_b,] or jnp.ndarray<float>[batch,num_b] weights.

  Returns:
    f: potential
    g: potential
    errors: ndarray of errors
  """
  # Initializing solutions
  f_u, g_v = init_dual_a, init_dual_b

  # Delete arguments not used in forward pass.
  del implicit_solver_fun, implicit_solver_ridge_kernel
  del implicit_solver_ridge_identity, implicit_solver_symmetric
  del precondition_fun

  # Defining the Sinkhorn loop, by setting initializations, body/cond.
  errors = -jnp.ones(
      (np.ceil(max_iterations / inner_iterations).astype(int), len(norm_error)))
  const = (geom, a, b, threshold)

  def cond_fn(iteration, const, state):
    threshold = const[-1]
    errors = state[0]
    err = errors[iteration // inner_iterations - 1, 0]

    return jnp.logical_or(iteration == 0,
                          jnp.logical_and(jnp.isfinite(err), err > threshold))

  def get_momentum(errors, idx):
    """momentum formula, https://arxiv.org/pdf/2012.12562v1.pdf, p.7 and (5)."""
    error_ratio = jnp.minimum(errors[idx - 1, -1] / errors[idx - 2, -1], .99)
    power = 1.0 / inner_iterations
    return 2.0 / (1.0 + jnp.sqrt(1.0 - error_ratio**power))

  def anderson_extrapolation(xs, fxs, ridge_identity=1e-2):
    """Computes Anderson extrapolation from past observations."""
    # Remove -inf values to instantiate quadratic problem. All others
    # remain since they might be caused by a valid issue.
    fxs_clean = jnp.nan_to_num(fxs, nan=jnp.nan, posinf=jnp.inf, neginf=0.0)
    xs_clean = jnp.nan_to_num(xs, nan=jnp.nan, posinf=jnp.inf, neginf=0.0)
    residuals = fxs_clean - xs_clean
    gram_matrix = jnp.matmul(residuals.T, residuals)
    gram_matrix /= jnp.linalg.norm(gram_matrix)

    # Solve linear system to obtain weights
    weights = jax.scipy.sparse.linalg.cg(
        gram_matrix + ridge_identity * jnp.eye(xs.shape[1]),
        jnp.ones(xs.shape[1]))[0]
    weights /= jnp.sum(weights)

    # Recover linear combination and return it with NaN (caused
    # by 0 weights leading to -jnp.inf potentials, mixed with weights
    # coefficiences of different signs), disambiguated to -inf.
    combination = jnp.sum(fxs * weights[None, :], axis=1)
    return jnp.where(jnp.isfinite(combination), combination, -jnp.inf)

  def anderson_update(iteration, f_u, old_f_u_s, old_mapped_f_u_s):
    # Anderson acceleration always happens in potentials (not scalings) space,
    # regardless of the lse_mode setting. If the iteration count is large
    # enough, and update_anderson is True, the update below will output a
    # potential variable.

    trigger_update = jnp.logical_and(
        iteration > anderson_acceleration,
        iteration % refresh_anderson_frequency == 0)

    f_u = jnp.where(
        trigger_update,
        anderson_extrapolation(old_f_u_s, old_mapped_f_u_s),
        f_u)

    # If the interpolation was triggered, we store it in memory
    # Otherwise we add the previous value (converting it to potential form if
    # it was initially stored in scaling form).

    old_f_u_s = jnp.where(
        trigger_update,
        jnp.concatenate((old_f_u_s[:, 1:], f_u[:, None]), axis=1),
        jnp.concatenate(
            (old_f_u_s[:, 1:],
             (f_u if lse_mode
              else geom.potential_from_scaling(f_u))[:, None]),
            axis=1))

    # If update was triggered, ensure a scaling is returned, since the result
    # from the extrapolation was outputted in potential form.
    f_u = jnp.where(
        trigger_update,
        f_u if lse_mode else geom.scaling_from_potential(f_u),
        f_u)
    return f_u, old_f_u_s

  def body_fn(iteration, const, state, compute_error):
    """Carries out sinkhorn iteration.

    Depending on lse_mode, these iterations can be either in:
      - log-space for numerical stability.
      - scaling space, using standard kernel-vector multiply operations.

    Args:
      iteration: iteration number
      const: tuple of constant parameters that do not change throughout the
        loop, here the geometry and the marginals a, b.
      state: error log, potential/scaling variables updated in the loop, and
        history for Anderson acceleration if selected.
      compute_error: flag to indicate this iteration computes/stores an error

    Returns:
      state variables, i.e. errors and updated f_u, g_v potentials + history.
    """
    geom, a, b, _ = const
    errors, f_u, g_v, old_f_u_s, old_mapped_f_u_s = state

    # compute momentum term if needed, using previously seen errors.
    w = jax.lax.stop_gradient(
        jnp.where(
            iteration >= jnp.where(chg_momentum_from == 0, jnp.inf,
                                   chg_momentum_from),
            get_momentum(errors, chg_momentum_from // inner_iterations),
            momentum))

    # Sinkhorn updates using momentum or Anderson acceleration,
    # in either scaling or potential form.

    # When running updates in parallel (Gauss-Seidel mode), old_g_v will be
    # used to update f_u, rather than the latest g_v computed in this loop.
    if parallel_dual_updates:
      old_g_v = g_v

    # When using Anderson acceleration, first update the dual variable f_u with
    # previous updates (if iteration count sufficiently large), then record
    # new iterations in array.
    if anderson_acceleration:
      f_u, old_f_u_s = anderson_update(
          iteration, f_u, old_f_u_s, old_mapped_f_u_s)

    # In lse_mode, run additive updates.
    if lse_mode:
      new_g_v = tau_b * geom.update_potential(
          f_u, g_v, jnp.log(b), iteration, axis=0)
      g_v = (1.0 - w) * jnp.where(jnp.isfinite(g_v), g_v, 0.0) + w * new_g_v
      new_f_u = tau_a * geom.update_potential(
          f_u,
          old_g_v if parallel_dual_updates else g_v,
          jnp.log(a),
          iteration,
          axis=1)
      f_u = (1.0 - w) * jnp.where(jnp.isfinite(f_u), f_u, 0.0) + w * new_f_u
    # In kernel mode, run multiplicative updates.
    else:
      new_g_v = geom.update_scaling(f_u, b, iteration, axis=0)**tau_b
      g_v = jnp.where(g_v > 0, g_v, 1)**(1.0 - w) * new_g_v**w
      new_f_u = geom.update_scaling(
          old_g_v if parallel_dual_updates else g_v, a, iteration,
          axis=1)**tau_a
      f_u = jnp.where(f_u > 0, f_u, 1)**(1.0 - w) * new_f_u**w

    # When using Anderson acceleration, refresh latest update.
    if anderson_acceleration:
      old_mapped_f_u_s = jnp.concatenate(
          (old_mapped_f_u_s[:, 1:],
           (f_u if lse_mode else geom.potential_from_scaling(f_u))[:, None]),
          axis=1)

    # re-computes error if compute_error is True, else set it to inf.
    err = jnp.where(
        jnp.logical_and(compute_error, iteration >= min_iterations),
        marginal_error(geom, a, b, tau_a, tau_b, f_u, g_v, norm_error,
                       lse_mode), jnp.inf)

    errors = errors.at[iteration // inner_iterations, :].set(err)
    return errors, f_u, g_v, old_f_u_s, old_mapped_f_u_s

  # Run the Sinkhorn loop. choose either a standard fixpoint_iter loop if
  # differentiation is implicit, otherwise switch to the backprop friendly
  # version of that loop if unrolling to differentiate.

  if implicit_differentiation:
    fix_point = fixed_point_loop.fixpoint_iter
  else:
    fix_point = fixed_point_loop.fixpoint_iter_backprop

  # Initialize log matrix used in Anderson acceleration with nan values.
  # these values will be replaced by actual iteration values.
  if anderson_acceleration:
    old_f_u_s = jnp.ones(
        (geom.shape[0], anderson_acceleration)) * jnp.nan
    old_mapped_f_u_s = old_f_u_s
  else:
    old_f_u_s, old_mapped_f_u_s = None, None

  errors, f_u, g_v, _, _ = fix_point(
      cond_fn, body_fn, min_iterations, max_iterations, inner_iterations, const,
      (errors, f_u, g_v, old_f_u_s, old_mapped_f_u_s))

  f = f_u if lse_mode else geom.potential_from_scaling(f_u)
  g = g_v if lse_mode else geom.potential_from_scaling(g_v)

  return f, g, errors[:, 0]


def _sinkhorn_iterations_taped(
    tau_a: float,
    tau_b: float,
    inner_iterations: int,
    min_iterations: int,
    max_iterations: int,
    chg_momentum_from: int,
    anderson_acceleration: int,
    refresh_anderson_frequency: int,
    lse_mode: bool,
    implicit_differentiation: bool,
    implicit_solver_fun: Callable,
    implicit_solver_ridge_kernel: float,
    implicit_solver_ridge_identity: float,
    implicit_solver_symmetric: bool,
    precondition_fun: Optional[Callable[[float], float]],
    parallel_dual_updates: bool,
    init_dual_a: jnp.ndarray,
    init_dual_b: jnp.ndarray,
    momentum: float,
    threshold: float,
    norm_error: Sequence[int],
    geom: geometry.Geometry,
    a: jnp.ndarray,
    b: jnp.ndarray):
  """Runs forward pass of the Sinkhorn algorithm storing side information."""
  f, g, errors = _sinkhorn_iterations(
      tau_a, tau_b, inner_iterations, min_iterations, max_iterations,
      chg_momentum_from, anderson_acceleration, refresh_anderson_frequency,
      lse_mode, implicit_differentiation,
      implicit_solver_fun,
      implicit_solver_ridge_kernel,
      implicit_solver_ridge_identity,
      implicit_solver_symmetric,
      precondition_fun,
      parallel_dual_updates, init_dual_a, init_dual_b, momentum,
      threshold, norm_error, geom, a, b)
  return (f, g, errors), (f, g, geom, a, b)


def _sinkhorn_iterations_implicit_bwd(
    tau_a, tau_b, inner_iterations, min_iterations, max_iterations,
    chg_momentum_from, anderson_acceleration, refresh_anderson_frequency,
    lse_mode, implicit_differentiation, implicit_solver_fun,
    implicit_solver_ridge_kernel, implicit_solver_ridge_identity,
    implicit_solver_symmetric, precondition_fun,
    parallel_dual_updates, res, gr
) -> Tuple[Any, Any, Any, Any, geometry.Geometry, jnp.ndarray, jnp.ndarray]:
  """Runs Sinkhorn in backward mode, using implicit differentiation.

  Args:
    tau_a: float
    tau_b: float.
    inner_iterations: iters
    min_iterations: minimum number of Sinkhorn iterations.
    max_iterations: maximum number of Sinkhorn iterations.
    chg_momentum_from: int
    anderson_acceleration: int
    refresh_anderson_frequency: int
    lse_mode: True for log-sum-exp computations, False for kernel
      multiplication.
    implicit_differentiation: implicit or backprop.
    implicit_solver_fun: see ``solve_implicit_system``
    implicit_solver_ridge_kernel: see ``solve_implicit_system``
    implicit_solver_ridge_identity: see ``solve_implicit_system``
    implicit_solver_symmetric: see ``solve_implicit_system``
    precondition_fun: function to apply to the two blocks of the first
      order condition.
    parallel_dual_updates: update sequence.
    res: residual data sent from fwd pass, used for computations below. In this
      case consists in the output itself, as well as inputs against which we
      wish to differentiate.
    gr: gradients w.r.t outputs of fwd pass, here w.r.t size f, g, errors. Note
      that differentiability w.r.t. errors is not handled, and only f, g is
      considered.

  Returns:
    a tuple of gradients: PyTree for geom, one jnp.ndarray for each of a and b.
  """
  del inner_iterations, min_iterations, max_iterations
  del chg_momentum_from, anderson_acceleration, refresh_anderson_frequency
  del implicit_differentiation, parallel_dual_updates

  f, g, geom, a, b = res
  # Ignores gradients info with respect to 'errors' output.
  gr = gr[0], gr[1]

  # Applies first part of vjp to gr: inverse part of implicit function theorem.
  vjp_gr = solve_implicit_system(gr, geom, a, b, f, g, tau_a, tau_b, lse_mode,
                                 precondition_fun,
                                 implicit_solver_fun,
                                 implicit_solver_ridge_kernel,
                                 implicit_solver_ridge_identity,
                                 implicit_solver_symmetric)

  # Instantiates vjp of first order conditions of the objective, as a
  # function of geom, a and b parameters (against which we differentiate)

  foc_geom_a_b = lambda geom, a, b: first_order_conditions(
      geom, a, b, f, g, tau_a, tau_b, lse_mode, precondition_fun)

  # Carries pullback onto original inputs, here geom, a and b.
  _, pull_geom_a_b = jax.vjp(foc_geom_a_b, geom, a, b)
  g_geom, g_a, g_b = pull_geom_a_b(vjp_gr)

  # First gradients are for init_a, init_b, momentum, threshold and
  # norm_errors (see jax.custom_vjp definition): those are set to None.
  return None, None, None, None, None, g_geom, g_a, g_b


# Sets threshold, norm_errors, geom, a and b to be differentiable, as those are
# non static. Only differentiability w.r.t. geom, a and b will be used.
_sinkhorn_iterations_implicit = functools.partial(
    jax.custom_vjp, nondiff_argnums=range(16))(
        _sinkhorn_iterations)
_sinkhorn_iterations_implicit.defvjp(_sinkhorn_iterations_taped,
                                     _sinkhorn_iterations_implicit_bwd)


def marginal_error(
    geom: geometry.Geometry,
    a: jnp.ndarray,
    b: jnp.ndarray,
    tau_a: float,
    tau_b: float,
    f_u: jnp.ndarray,
    g_v: jnp.ndarray,
    norm_error: int,
    lse_mode: bool) -> jnp.ndarray:
  """Conputes marginal error, the stopping criterion used to terminate Sinkhorn.

  Args:
    geom: a Geometry object.
    a: jnp.ndarray<float>[num_a,] or jnp.ndarray<float>[batch,num_a] weights.
    b: jnp.ndarray<float>[num_b,] or jnp.ndarray<float>[batch,num_b] weights.
    tau_a: float, ratio lam/(lam+eps) between KL divergence regularizer to first
      marginal and itself + epsilon regularizer used in the unbalanced
      formulation.
    tau_b: float, ratio lam/(lam+eps) between KL divergence regularizer to first
      marginal and itself + epsilon regularizer used in the unbalanced
      formulation.
    f_u: jnp.ndarray, potential or scaling
    g_v: jnp.ndarray, potential or scaling
    norm_error: int, p-norm used to compute error.
    lse_mode: True if log-sum-exp operations, False if kernel vector producs.

  Returns:
    a positive number quantifying how far from convergence the algorithm stands.

  """
  if tau_a == 1.0 and tau_b == 1.0:
    err = geom.error(f_u, g_v, b, 0, norm_error, lse_mode)
  else:
    # In the unbalanced case, we compute the norm of the gradient.
    # the gradient is equal to the marginal of the current plan minus
    # the gradient of < z, rho_z(exp^(-h/rho_z) -1> where z is either a or b
    # and h is either f or g. Note this is equal to z if rho_z → inf, which
    # is the case when tau_z → 1.0
    if lse_mode:
      grad_a = grad_of_marginal_fit(a, f_u, tau_a, geom.epsilon)
      grad_b = grad_of_marginal_fit(b, g_v, tau_b, geom.epsilon)
    else:
      grad_a = grad_of_marginal_fit(a, geom.potential_from_scaling(f_u), tau_a,
                                    geom.epsilon)
      grad_b = grad_of_marginal_fit(b, geom.potential_from_scaling(g_v), tau_b,
                                    geom.epsilon)
    err = geom.error(f_u, g_v, grad_a, 1, norm_error, lse_mode)
    err += geom.error(f_u, g_v, grad_b, 0, norm_error, lse_mode)
  return err


def ent_reg_cost(
    geom: geometry.Geometry,
    a: jnp.ndarray,
    b: jnp.ndarray,
    tau_a: float,
    tau_b: float,
    f: jnp.ndarray,
    g: jnp.ndarray,
    lse_mode: bool) -> jnp.ndarray:
  r"""Computes objective of regularized OT given dual solutions ``f``, ``g``.

  The objective is evaluated for dual solution ``f`` and ``g``, using inputs
  ``geom``, ``a`` and ``b``, in addition to parameters ``tau_a``, ``tau_b``.
  Situations where ``a`` or ``b`` have zero coordinates are reflected in
  minus infinity entries in their corresponding dual potentials. To avoid NaN
  that may result when multiplying 0's by infinity values, ``jnp.where`` is
  used to cancel these contributions.

  Args:
    geom: a Geometry object.
    a: jnp.ndarray<float>[num_a,] or jnp.ndarray<float>[batch,num_a] weights.
    b: jnp.ndarray<float>[num_b,] or jnp.ndarray<float>[batch,num_b] weights.
    tau_a: float, ratio lam/(lam+eps) between KL divergence regularizer to first
      marginal and itself + epsilon regularizer used in the unbalanced
      formulation.
    tau_b: float, ratio lam/(lam+eps) between KL divergence regularizer to first
      marginal and itself + epsilon regularizer used in the unbalanced
      formulation.
    f: jnp.ndarray, potential
    g: jnp.ndarray, potential
    lse_mode: bool, whether to compute total mass in lse or kernel mode.

  Returns:
    a float, the regularized transport cost.
  """
  supp_a = a > 0
  supp_b = b > 0
  if tau_a == 1.0:
    div_a = jnp.sum(
        jnp.where(supp_a, a * (f - geom.potential_from_scaling(a)), 0.0))
  else:
    rho_a = geom.epsilon * (tau_a / (1 - tau_a))
    div_a = -jnp.sum(
        jnp.where(supp_a,
                  a * phi_star(-(f - geom.potential_from_scaling(a)), rho_a),
                  0.0))

  if tau_b == 1.0:
    div_b = jnp.sum(
        jnp.where(supp_b, b * (g - geom.potential_from_scaling(b)), 0.0))
  else:
    rho_b = geom.epsilon * (tau_b / (1 - tau_b))
    div_b = -jnp.sum(
        jnp.where(supp_b,
                  b * phi_star(-(g - geom.potential_from_scaling(b)), rho_b),
                  0.0))

  # Using https://arxiv.org/pdf/1910.12958.pdf (24)
  if lse_mode:
    total_sum = jnp.sum(geom.marginal_from_potentials(f, g))
  else:
    total_sum = jnp.sum(
        geom.marginal_from_scalings(
            geom.scaling_from_potential(f), geom.scaling_from_potential(g)))
  return div_a + div_b + geom.epsilon * (jnp.sum(a) * jnp.sum(b) - total_sum)


def grad_of_marginal_fit(c, h, tau, epsilon):
  """Computes grad of terms linked to marginals in objective.

  Computes gradient w.r.t. f ( or g) of terms in
  https://arxiv.org/pdf/1910.12958.pdf, left-hand-side of Eq. 15
  (terms involving phi_star)

  Args:
    c: jnp.ndarray, first target marginal (either a or b in practice)
    h: jnp.ndarray, potential (either f or g in practice)
    tau: float, strength (in ]0,1]) of regularizer w.r.t. marginal
    epsilon: regularization

  Returns:
    a vector of the same size as c or h
  """
  if tau == 1.0:
    return c
  else:
    rho = epsilon * tau / (1 - tau)
    return jnp.where(c > 0, c * derivative_phi_star(-h, rho), 0.0)


def phi_star(h: jnp.ndarray, rho: float) -> jnp.ndarray:
  """Legendre transform of KL, https://arxiv.org/pdf/1910.12958.pdf p.9."""
  return rho * (jnp.exp(h / rho) - 1)


def derivative_phi_star(f: jnp.ndarray, rho: float) -> jnp.ndarray:
  """Derivative of Legendre transform of KL, see phi_star."""
  return jnp.exp(f / rho)


def second_derivative_phi_star(f: jnp.ndarray, rho: float) -> jnp.ndarray:
  """Second Derivative of Legendre transform of KL, see phi_star."""
  return jnp.exp(f / rho) / rho


def diag_jacobian_of_marginal_fit(c, h, tau, epsilon, derivative):
  """Computes grad of terms linked to marginals in objective.

  Computes second derivative w.r.t. f ( or g) of terms in
  https://arxiv.org/pdf/1910.12958.pdf, left-hand-side of Eq. 32
  (terms involving phi_star)

  Args:
    c: jnp.ndarray, first target marginal (either a or b in practice)
    h: jnp.ndarray, potential (either f or g in practice)
    tau: float, strength (in ]0,1]) of regularizer w.r.t. marginal
    epsilon: regularization
    derivative: Callable

  Returns:
    a vector of the same size as c or h
  """
  if tau == 1.0:
    return 0
  else:
    rho = epsilon * tau / (1 - tau)
    # here no minus sign because we are taking derivative w.r.t -h
    return jnp.where(c > 0,
                     c * second_derivative_phi_star(-h, rho) * derivative(
                         c * derivative_phi_star(-h, rho)),
                     0.0)


def get_transport_functions(geom, lse_mode):
  """Instantiates useful functions from geometry depending on lse_mode."""
  if lse_mode:
    marginal_a = lambda f, g: geom.marginal_from_potentials(f, g, 1)
    marginal_b = lambda f, g: geom.marginal_from_potentials(f, g, 0)
    app_transport = geom.apply_transport_from_potentials
  else:
    marginal_a = lambda f, g: geom.marginal_from_scalings(
        geom.scaling_from_potential(f), geom.scaling_from_potential(g), 1)
    marginal_b = lambda f, g: geom.marginal_from_scalings(
        geom.scaling_from_potential(f), geom.scaling_from_potential(g), 0)
    app_transport = lambda f, g, z, axis: geom.apply_transport_from_scalings(
        geom.scaling_from_potential(f), geom.scaling_from_potential(g), z, axis)
  return marginal_a, marginal_b, app_transport


def solve_implicit_system(
    gr: Tuple[np.ndarray],
    geom: geometry.Geometry,
    a: np.ndarray,
    b: np.ndarray,
    f: np.ndarray,
    g: np.ndarray,
    tau_a: float,
    tau_b: float,
    lse_mode: bool,
    precondition_fun: Callable[[float], float],
    implicit_solver_fun: Callable,
    ridge_kernel: float,
    ridge_identity: float,
    symmetric: bool):
  r"""Applies minus inverse of [hessian of ``reg_ot_cost`` w.r.t ``f``, ``g``].

  This function is used to carry out implicit differentiation of ``sinkhorn``
  outputs, notably optimal potentials ``f`` and ``g``. That differentiation
  requires solving a linear system, using (and inverting) the Jacobian of
  (preconditioned) first-order conditions w.r.t. the reg-OT problem.

  Given a ``precondition_fun``, written here for short as :math:`h`,
  the first order conditions for the dual energy
  :math:`E(K, \epsilon, a, b, f, g) :=- <a,\phi_a^{*}(-f)> + <b, \phi_b^{*}(-g)> - \langle\exp^{f/\epsilon}, K
    \exp^{g/\epsilon}>`

  form the basis of the Sinkhorn algorithm. To differentiate optimal solutions
  to that problem, we exploit the fact that :math:`h(\nabla E = 0)` and
  differentiate that identity to recover variations (Jacobians) of optimal
  solutions :math:`f^\star, g^\star$` as a function of changes in the inputs.
  The Jacobian of :math:`h(\nabla_{f,g} E = 0)` is a linear operator which, if
  it were to be instantiated as a matrix, would be of size
  :math:`(n+m) \times (n+m)`. When :math:`h` is the identity, that matrix is the
  Hessian of :math:`E`, is symmetric and negative-definite
  (:math:`E` is concave) and is structured as :math:`[A, B; B^T, D]`. More
  generally, for other functions :math:`h`, the Jacobian of these preconditioned
  first order conditions is no longer symmetric (except if ``a==b``), and
  has now a structure as :math:`[A, B; C, D]`. That system can
  be still inverted more generic solvers. By default, :math:`h = \epsilon \log`,
  as proposed in https://arxiv.org/pdf/2002.03229.pdf.

  In both cases :math:`A` and :math:`D` are diagonal matrices, equal to the row and
  column marginals respectively, multiplied by the derivatives of :math:`h`
  evaluated at those marginals, corrected (if handling the unbalanced case)
  by the second derivative of the part of the objective that ties potentials to
  the marginals (terms in ``phi_star``). When :math:`h` is the identity,
  :math:`B` and :math:`B^T` are equal respectively to the OT matrix and its
  transpose, i.e. :math:`n \times m` and :math:`m \times n` matrices.
  When :math:`h` is not the identity, :math:`B` (resp. :math:`C`) is equal
  to the OT matrix (resp. its transpose), rescaled on the left by the
  application elementwise of :math:`h'` to the row (respectively column)
  marginal sum of the transport.

  Note that we take great care in not instantiatiating these transport
  matrices, to rely instead on calls to the ``app_transport`` method from the
  ``Geometry`` object ``geom`` (which will either use potentials or scalings,
  depending on ``lse_mode``)

  The Jacobian's diagonal + off-diagonal blocks structure allows to exploit
  Schur complements. Depending on the sizes involved, it is better to
  instantiate the Schur complement of the first or of the second diagonal block.

  In either case, the Schur complement is rank deficient, with a 0 eigenvalue
  for the vector of ones in the balanced case, which is why we add a ridge on
  that subspace to enforce solutions have zero sum.

  The Schur complement can also be rank deficient if two lines or columns of T
  are colinear. This will typically happen it two rows or columns of the cost
  or kernel matrix are numerically close. To avoid this, we add a more global
  ``ridge_identity * z`` regularizer to achieve better conditioning.

  These linear systems are solved using the user defined ``implicit_solver_fun``,
  which is set by default to ``cg``. When the system is symmetric (as detected
  by the corresponding flag ``symmetric``), ``cg`` is applied directly. When it
  is not, normal equations are used (i.e. the Schur complement is multiplied by
  its transpose before solving the system).

  Args:
    gr: 2-uple, (vector of size ``n``, vector of size ``m``).
    geom: Geometry object.
    a: marginal.
    b: marginal.
    f: potential, w.r.t marginal a.
    g: potential, w.r.t marginal b.
    tau_a: float, ratio lam/(lam+eps), ratio of regularizers, first marginal.
    tau_b: float, ratio lam/(lam+eps), ratio of regularizers, second marginal.
    lse_mode: bool, log-sum-exp mode if True, kernel else.
    precondition_fun: preconditioning function to stabilize FOC implicit system.
    implicit_solver_fun: Callable, should return (solution, ...)
    ridge_kernel: promotes zero-sum solutions. only used if tau_a = tau_b = 1.0
    ridge_identity: handles rank deficient transport matrices (this happens
      typically when rows/cols in cost/kernel matrices are colinear, or,
      equivalently when two points from either measure are close).
    symmetric: flag used to figure out whether the linear system solved in the
      implicit function theorem is symmetric or not. This happens when either
      ``a == b`` or the precondition_fun is the identity. False by default, and,
      at the moment, needs to be set manually by the user in the more favorable
      case where the system is guaranteed to be symmetric.

  Returns:
    A tuple of two vectors, of the same size as ``gr``.
  """
  marginal_a, marginal_b, app_transport = get_transport_functions(
      geom, lse_mode)
  # elementwise vmap apply of derivative of precondition_fun. No vmapping
  # can be problematic here.
  derivative = jax.vmap(jax.grad(precondition_fun))

  n, m = geom.shape

  vjp_fg = lambda z: app_transport(
      f, g, z * derivative(marginal_b(f, g)), axis=1) / geom.epsilon
  vjp_gf = lambda z: app_transport(
      f, g, z * derivative(marginal_a(f, g)), axis=0) / geom.epsilon

  if not symmetric:
    vjp_fgt = lambda z: app_transport(
        f, g, z, axis=0) * derivative(marginal_b(f, g)) / geom.epsilon
    vjp_gft = lambda z: app_transport(
        f, g, z, axis=1) * derivative(marginal_a(f, g)) / geom.epsilon

  diag_hess_a = (
      marginal_a(f, g) * derivative(marginal_a(f, g)) / geom.epsilon +
      diag_jacobian_of_marginal_fit(a, f, tau_a, geom.epsilon, derivative))
  diag_hess_b = (
      marginal_b(f, g) * derivative(marginal_b(f, g)) / geom.epsilon +
      diag_jacobian_of_marginal_fit(b, g, tau_b, geom.epsilon, derivative))

  n, m = geom.shape
  # Remove ridge on kernel space if problem is balanced.
  ridge_kernel = jnp.where(tau_a == 1.0 and tau_b == 1.0, ridge_kernel, 0.0)

  # Forks on using Schur complement of either A or D, depending on size.
  if n > m:  #  if n is bigger, run m x m linear system.
    inv_vjp_ff = lambda z: z / diag_hess_a
    vjp_gg = lambda z: z * diag_hess_b
    schur_ = lambda z: vjp_gg(z) - vjp_gf(inv_vjp_ff(vjp_fg(z)))
    g0, g1 = vjp_gf(inv_vjp_ff(gr[0])), gr[1]

    if symmetric:
      schur = lambda z: (schur_(z) + ridge_kernel * jnp.sum(z)
                         + ridge_identity * z)
    else:
      schur_t = lambda z: vjp_gg(z) - vjp_fgt(inv_vjp_ff(vjp_gft(z)))
      g0, g1 = schur_t(g0), schur_t(g1)
      schur = lambda z: (
          schur_t(schur_(z)) + ridge_kernel * jnp.sum(z) + ridge_identity * z)

    sch_f = implicit_solver_fun(schur, g0)[0]
    sch_g = implicit_solver_fun(schur, g1)[0]
    vjp_gr_f = inv_vjp_ff(gr[0] + vjp_fg(sch_f) - vjp_fg(sch_g))
    vjp_gr_g = -sch_f + sch_g
  else:
    vjp_ff = lambda z: z * diag_hess_a
    inv_vjp_gg = lambda z: z / diag_hess_b
    schur_ = lambda z: vjp_ff(z) - vjp_fg(inv_vjp_gg(vjp_gf(z)))
    g0, g1 = vjp_fg(inv_vjp_gg(gr[1])), gr[0]

    if symmetric:
      schur = lambda z: (schur_(z) + ridge_kernel * jnp.sum(z)
                         + ridge_identity * z)
    else:
      schur_t = lambda z: vjp_ff(z) - vjp_gft(inv_vjp_gg(vjp_fgt(z)))
      g0, g1 = schur_t(g0), schur_t(g1)
      schur = lambda z: (schur_t(schur_(z)) + ridge_kernel * jnp.sum(z)
                         + ridge_identity * z)

    sch_g = implicit_solver_fun(schur, g0)[0]
    sch_f = implicit_solver_fun(schur, g1)[0]
    vjp_gr_g = inv_vjp_gg(gr[1] + vjp_gf(sch_g) - vjp_gf(sch_f))
    vjp_gr_f = -sch_g + sch_f

  return jnp.concatenate((-vjp_gr_f, -vjp_gr_g))


def first_order_conditions(
    geom: geometry.Geometry,
    a: jnp.ndarray,
    b: jnp.ndarray,
    f: jnp.ndarray,
    g: jnp.ndarray,
    tau_a: float,
    tau_b: float,
    lse_mode: bool,
    precondition_fun: Optional[Callable[[float], float]]):
  r"""Computes vector of first order conditions for the reg-OT problem.

  The output of this vector should be close to zero at optimality.
  Upon completion of the Sinkhorn forward pass, its norm (using the norm
  parameter defined using ``norm_error``) should be below the threshold
  parameter.

  This error will be itself assumed to be close to zero when using implicit
  differentiation.

  Args:
    geom: a geometry object
    a: jnp.ndarray, first marginal
    b: jnp.ndarray, second marginal
    f: jnp.ndarray, first potential
    g: jnp.ndarray, second potential
    tau_a: float, ratio lam/(lam+eps), ratio of regularizers, first marginal
    tau_b: float, ratio lam/(lam+eps), ratio of regularizers, second marginal
    lse_mode: bool
    precondition_fun: elementwise to apply on both sides of FOC.

  Returns:
    a jnp.ndarray of size (size of ``n + m``) quantifying deviation to
    optimality for variables ``f`` and ``g``.
  """
  marginal_a, marginal_b, _ = get_transport_functions(geom, lse_mode)
  grad_a = grad_of_marginal_fit(a, f, tau_a, geom.epsilon)
  grad_b = grad_of_marginal_fit(b, g, tau_b, geom.epsilon)
  return jnp.concatenate((
      jnp.where(a > 0,
                precondition_fun(marginal_a(f, g)) - precondition_fun(grad_a),
                0.0),
      jnp.where(b > 0,
                precondition_fun(marginal_b(f, g)) - precondition_fun(grad_b),
                0.0)))
