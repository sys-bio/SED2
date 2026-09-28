// Generated from math.g4 by ANTLR 4.13.2
package org.sedml.libsed2.antlr;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link mathParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface mathVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link mathParser#start}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStart(mathParser.StartContext ctx);
	/**
	 * Visit a parse tree produced by {@link mathParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpr(mathParser.ExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link mathParser#logical}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLogical(mathParser.LogicalContext ctx);
	/**
	 * Visit a parse tree produced by {@link mathParser#relational}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelational(mathParser.RelationalContext ctx);
	/**
	 * Visit a parse tree produced by {@link mathParser#relop}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelop(mathParser.RelopContext ctx);
	/**
	 * Visit a parse tree produced by {@link mathParser#additive}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAdditive(mathParser.AdditiveContext ctx);
	/**
	 * Visit a parse tree produced by {@link mathParser#multiplicative}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultiplicative(mathParser.MultiplicativeContext ctx);
	/**
	 * Visit a parse tree produced by the {@code unaryOp}
	 * labeled alternative in {@link mathParser#unary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnaryOp(mathParser.UnaryOpContext ctx);
	/**
	 * Visit a parse tree produced by the {@code unaryPower}
	 * labeled alternative in {@link mathParser#unary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnaryPower(mathParser.UnaryPowerContext ctx);
	/**
	 * Visit a parse tree produced by {@link mathParser#power}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPower(mathParser.PowerContext ctx);
	/**
	 * Visit a parse tree produced by the {@code numberAtom}
	 * labeled alternative in {@link mathParser#atom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumberAtom(mathParser.NumberAtomContext ctx);
	/**
	 * Visit a parse tree produced by the {@code referenceAtom}
	 * labeled alternative in {@link mathParser#atom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReferenceAtom(mathParser.ReferenceAtomContext ctx);
	/**
	 * Visit a parse tree produced by the {@code callAtom}
	 * labeled alternative in {@link mathParser#atom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCallAtom(mathParser.CallAtomContext ctx);
	/**
	 * Visit a parse tree produced by the {@code identAtom}
	 * labeled alternative in {@link mathParser#atom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIdentAtom(mathParser.IdentAtomContext ctx);
	/**
	 * Visit a parse tree produced by the {@code arrayAtom}
	 * labeled alternative in {@link mathParser#atom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArrayAtom(mathParser.ArrayAtomContext ctx);
	/**
	 * Visit a parse tree produced by the {@code parenAtom}
	 * labeled alternative in {@link mathParser#atom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParenAtom(mathParser.ParenAtomContext ctx);
	/**
	 * Visit a parse tree produced by {@link mathParser#arglist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArglist(mathParser.ArglistContext ctx);
}