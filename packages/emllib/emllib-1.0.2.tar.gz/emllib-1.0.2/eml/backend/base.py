#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Backend(object):
    """ CP Solver Wrapper """
    def __init__(self):
        super(Backend, self).__init__()

    def const_eps(self):
        raise NotImplementedError('This method should be implemented in subclasses')

    def var_cont(self, mdl, lb, ub, name=None):
        raise NotImplementedError('This method should be implemented in subclasses')

    def var_bin(self, mdl, name=None):
        raise NotImplementedError('This method should be implemented in subclasses')

    def xpr_scalprod(self, mdl, coefs, terms):
        raise NotImplementedError('This method should be implemented in subclasses')

    def xpr_sum(self, mdl, terms):
        raise NotImplementedError('This method should be implemented in subclasses')

    def xpr_eq(self, mdl, left, right):
        raise NotImplementedError('This method should be implemented in subclasses')

    def cst_eq(self, mdl, left, right, name=None):
        raise NotImplementedError('This method should be implemented in subclasses')

    def cst_leq(self, mdl, left, right, name=None):
        raise NotImplementedError('This method should be implemented in subclasses')

    def cst_geq(self, mdl, left, right, name=None):
        return self.cst_leq(mdl, right, left)

    def cst_indicator(self, mdl, trigger, cst, name=None):
        raise NotImplementedError('This method should be implemented in subclasses')

    def get_obj(self, mdl):
        raise NotImplementedError('This method should be implemented in subclasses')

    def set_obj(self, mdl, sense, xpr):
        raise NotImplementedError('This method should be implemented in subclasses')

    def solve(self, mdl, timelimit):
        raise NotImplementedError('This method should be implemented in subclasses')

    def new_model(self, name=None):
        raise NotImplementedError('This method should be implemented in subclasses')

    # def update_lb(self, bkd, mdl, ml, lb):
    #     raise NotImplementedError('This method should be implemented in subclasses')

    # def update_ub(self, bkd, mdl, ml, ub):
    #     raise NotImplementedError('This method should be implemented in subclasses')