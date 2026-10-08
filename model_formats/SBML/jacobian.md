# SBML: Jacobian tasks

What `JacobianFull` and `JacobianReduced` compute when the model's language is
SBML (KiSAO:0000812).  These rules are for SBML models; other modeling
languages need rules of their own (see the same file in their folders).

## What the matrix holds

* The Jacobian is d(dx_i/dt)/dx_j, evaluated at the model's state as given:
  its initial values, or the end state of an earlier task that produced it.
* x is the value of a species by its SBML id: its concentration, or its amount
  if the species has `hasOnlySubstanceUnits="true"`.  With different
  compartment sizes, concentration-based and amount-based Jacobians differ, so
  this choice is part of the definition.
* Compartment sizes must be constant; a model whose compartments change size
  (by a rule or an event) has no well-defined Jacobian in this sense.

## Which species, in which order

* "Species" means the non-boundary species (those with
  `boundaryCondition="false"`), in the order of the SBML `listOfSpecies`.
* `JacobianFull` is species x species in that order, with the species ids as
  the labels of both dimensions.

## JacobianReduced

* The reduced matrix is taken over the independent species only; the species
  that a conservation relation makes dependent are dropped.
* Which species of a conservation relation is dropped is a choice of the
  simulator, so the labels of the reduced matrix can differ between simulators
  for the same model.
* To be determined: define the independent set (for example, the last species
  of each relation is the dependent one), or leave it open.  Until then, a
  consumer must read the labels, not assume an order.

## Open questions

* Whether concentration or amount is the stated choice above for every
  simulator, or an option of the task.
* How a model with algebraic rules or events is treated.
