# Generated from math.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .mathParser import mathParser
else:
    from mathParser import mathParser

# This class defines a complete generic visitor for a parse tree produced by mathParser.

class mathVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by mathParser#start.
    def visitStart(self, ctx:mathParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#expr.
    def visitExpr(self, ctx:mathParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#logical.
    def visitLogical(self, ctx:mathParser.LogicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#relational.
    def visitRelational(self, ctx:mathParser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#relop.
    def visitRelop(self, ctx:mathParser.RelopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#additive.
    def visitAdditive(self, ctx:mathParser.AdditiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#multiplicative.
    def visitMultiplicative(self, ctx:mathParser.MultiplicativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#unaryOp.
    def visitUnaryOp(self, ctx:mathParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#unaryPower.
    def visitUnaryPower(self, ctx:mathParser.UnaryPowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#power.
    def visitPower(self, ctx:mathParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#numberAtom.
    def visitNumberAtom(self, ctx:mathParser.NumberAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#referenceAtom.
    def visitReferenceAtom(self, ctx:mathParser.ReferenceAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#callAtom.
    def visitCallAtom(self, ctx:mathParser.CallAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#identAtom.
    def visitIdentAtom(self, ctx:mathParser.IdentAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#arrayAtom.
    def visitArrayAtom(self, ctx:mathParser.ArrayAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#parenAtom.
    def visitParenAtom(self, ctx:mathParser.ParenAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathParser#arglist.
    def visitArglist(self, ctx:mathParser.ArglistContext):
        return self.visitChildren(ctx)



del mathParser