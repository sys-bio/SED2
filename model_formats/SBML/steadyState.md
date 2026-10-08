# SBML: SteadyState

What a `SteadyState` task finds when the model's language is SBML.

## Result

* The task finds a state in which dx_i/dt = 0 for the non-boundary species
  (see `jacobian.md` for which species, and in which order).
* The search starts from the model's state as given (its initial values, or
  the end state of an earlier task).
* When there is more than one steady state, which one is found is
  simulator-dependent: it is the one the simulator's root finder reaches from
  the starting state.

## Output variables

* `time` is not a valid output variable of a steady state: it has no value
  there.
* To be determined: the other legal output variables (species, global
  parameters and reactions by SBML id, as for `labels.md`).

## When there is none

* When no steady state is found, the task fails.  There is no partial result.
